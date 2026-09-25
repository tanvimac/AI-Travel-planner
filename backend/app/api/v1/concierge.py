import logging
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.orm import Session
from google import genai

from app.db.database import get_db
from app.core.config import settings
from app.core.gemini_retry import gemini_generate
from app.core.deps import get_optional_current_user
from app.db.models.user import User
from app.db.models.trip import Trip
from app.db.models.concierge import AIConversation, AIMessage
from app.schemas.v1_schemas import ConciergeChatRequest
from app.core.errors import NotFoundException

logger = logging.getLogger("concierge_api")
router = APIRouter(prefix="/concierge", tags=["AI Concierge"])


def _generate_fallback_concierge_response(message: str, trip: Optional[Trip] = None) -> str:
    """Intelligent fallback concierge guidance when LLM provider is busy or offline."""
    dest = trip.destination if trip else "your destination"
    low = message.lower()

    if any(w in low for w in ["pack", "weather", "clothes", "rain"]):
        return f"For traveling to {dest}, I recommend packing comfortable walking shoes, a light weather-resistant jacket, versatile layers, and an international power adapter. Check local forecasts 48 hours prior to departure for any sudden weather changes."
    elif any(w in low for w in ["eat", "food", "restaurant", "dinner", "lunch"]):
        return f"In {dest}, prioritize authentic local neighborhoods and small eateries rather than main tourist corridors. Try regional signature dishes and consider making reservations for peak weekend dinner slots."
    elif any(w in low for w in ["safety", "scam", "safe", "emergency"]):
        return f"General safety tips for {dest}: keep digital copies of your passport and reservations, use official transit or registered taxis, and avoid keeping all payment cards in one place. Emergency services can usually be contacted at 112 or local emergency numbers."
    elif any(w in low for w in ["flight", "airport", "transit", "train"]):
        return f"When navigating {dest}, look into multi-day transit passes or contact-less metro payment. For departures, arrive at the airport at least 2 hours early for domestic flights and 3 hours for international flights."
    else:
        return f"As your personal AI Concierge for {dest}, I am here to help optimize your itinerary, suggest attractions, and provide local tips. Could you specify which aspect of your journey you'd like advice on (e.g. dining, attractions, budget, or transit)?"


@router.post("/chat")
def chat_with_concierge(
    payload: ConciergeChatRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    """Interactive conversational travel concierge powered by AI orchestrator."""
    trip = None
    if payload.trip_id:
        trip = db.query(Trip).filter(Trip.id == payload.trip_id).first()

    # Find or create conversation
    conversation = None
    if payload.conversation_id:
        conversation = db.query(AIConversation).filter(AIConversation.id == payload.conversation_id).first()

    if not conversation:
        title = f"Concierge for {trip.destination}" if trip else "Travel Concierge"
        conversation = AIConversation(
            trip_id=trip.id if trip else None,
            user_id=current_user.id if current_user else None,
            title=title,
        )
        db.add(conversation)
        db.flush()

    # Save user message
    user_msg = AIMessage(
        conversation_id=conversation.id,
        sender="user",
        content=payload.message.strip(),
        metadata_json={},
    )
    db.add(user_msg)
    db.flush()

    # Build prompt with conversation history context
    history_messages = (
        db.query(AIMessage)
        .filter(AIMessage.conversation_id == conversation.id)
        .order_by(AIMessage.created_at.asc())
        .limit(10)
        .all()
    )

    history_text = "\n".join([f"{m.sender.upper()}: {m.content}" for m in history_messages])

    trip_info = ""
    if trip:
        trip_info = (
            f"Trip Destination: {trip.destination}\n"
            f"Days: {trip.days}, Travelers: {trip.travelers}\n"
            f"Budget: {trip.currency or 'USD'} {trip.budget}\n"
            f"Interests: {trip.interests}\n"
            f"Travel Style: {trip.travel_style}\n"
        )

    prompt = (
        "You are an elite, highly knowledgeable luxury and boutique AI travel concierge. "
        "Provide warm, concise, and actionable recommendations. Do not use generic filler.\n\n"
        f"Trip Context:\n{trip_info}\n"
        f"Recent Conversation:\n{history_text}\n\n"
        "ASSISTANT:"
    )

    reply_content = ""
    try:
        if settings.GEMINI_API_KEY:
            client = genai.Client(api_key=settings.GEMINI_API_KEY)
            response = gemini_generate(
                client=client,
                model=settings.GEMINI_MODEL,
                contents=prompt,
            )
            if response and response.text:
                reply_content = response.text.strip()
    except Exception as exc:
        logger.warning("Gemini concierge generation fallback invoked: %s", exc)

    if not reply_content:
        reply_content = _generate_fallback_concierge_response(payload.message, trip)

    # Save assistant message
    asst_msg = AIMessage(
        conversation_id=conversation.id,
        sender="assistant",
        content=reply_content,
        metadata_json={"model": settings.GEMINI_MODEL},
    )
    db.add(asst_msg)
    db.commit()
    db.refresh(asst_msg)

    return {
        "status": "success",
        "conversation_id": conversation.id,
        "trip_id": conversation.trip_id,
        "message": reply_content,
        "created_at": asst_msg.created_at.isoformat(),
    }


@router.get("/conversations")
def list_conversations(
    trip_id: Optional[int] = Query(None, description="Filter by trip ID"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    """List concierge conversations."""
    query = db.query(AIConversation)
    if trip_id:
        query = query.filter(AIConversation.trip_id == trip_id)
    elif current_user:
        query = query.filter(AIConversation.user_id == current_user.id)

    conversations = query.order_by(AIConversation.updated_at.desc()).all()
    return {
        "status": "success",
        "count": len(conversations),
        "conversations": [
            {
                "id": c.id,
                "title": c.title,
                "trip_id": c.trip_id,
                "created_at": c.created_at.isoformat(),
                "updated_at": c.updated_at.isoformat(),
            }
            for c in conversations
        ],
    }


@router.get("/conversations/{conversation_id}")
def get_conversation_details(
    conversation_id: int = Path(..., description="Conversation ID"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    """Retrieve all messages in a concierge conversation."""
    conversation = db.query(AIConversation).filter(AIConversation.id == conversation_id).first()
    if not conversation:
        raise NotFoundException(message=f"Conversation {conversation_id} not found")

    messages = (
        db.query(AIMessage)
        .filter(AIMessage.conversation_id == conversation_id)
        .order_by(AIMessage.created_at.asc())
        .all()
    )

    return {
        "status": "success",
        "id": conversation.id,
        "title": conversation.title,
        "trip_id": conversation.trip_id,
        "messages": [
            {
                "id": m.id,
                "sender": m.sender,
                "content": m.content,
                "created_at": m.created_at.isoformat(),
            }
            for m in messages
        ],
    }
