"""
Comprehensive Phase 2 Backend Verification Suite
Tests all endpoints, health checks, error formats, and security guarantees.
"""

import sys
import uuid
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

passed = 0
failed = 0

def test_endpoint(name: str, fn):
    global passed, failed
    try:
        fn()
        passed += 1
        print(f"  [PASS] {name}")
    except Exception as e:
        failed += 1
        print(f"  [FAIL] {name}: {e}")

print("=== Starting Phase 2 Backend Tests ===")

# --- 1. Health Endpoints ---
print("\n--- Testing Health Endpoints ---")

def test_get_health():
    res = client.get("/health")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.text}"
    data = res.json()
    assert "status" in data
    assert "database" in data
    assert data["database"] == "connected"

def test_get_health_providers():
    res = client.get("/health/providers")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.text}"
    data = res.json()
    assert "providers" in data
    providers = data["providers"]
    for expected in ["weather", "currency", "places", "flights", "hotels", "restaurants", "routes", "ai_orchestrator"]:
        assert expected in providers, f"Missing {expected} in providers health"
    # Ensure no secrets in output
    raw_text = res.text.lower()
    assert "travel_password" not in raw_text
    assert "gemini_api_key" not in raw_text

test_endpoint("GET /health", test_get_health)
test_endpoint("GET /health/providers", test_get_health_providers)

# --- 2. Auth Endpoints ---
print("\n--- Testing Auth Endpoints ---")
test_user_email = f"traveler_{uuid.uuid4().hex[:6]}@example.com"
test_password = "SecurePassword123!"
auth_token = None
user_id = None

def test_register():
    global user_id
    res = client.post("/api/v1/auth/register", json={
        "email": test_user_email,
        "password": test_password,
        "full_name": "Test Traveler",
    })
    assert res.status_code in [201, 200], f"Got {res.status_code}: {res.text}"
    data = res.json()
    assert "id" in data["user"]
    user_id = data["user"]["id"]

def test_login():
    global auth_token
    res = client.post("/api/v1/auth/login", json={
        "email": test_user_email,
        "password": test_password,
    })
    assert res.status_code == 200, f"Got {res.status_code}: {res.text}"
    data = res.json()
    assert "access_token" in data
    auth_token = data["access_token"]

def test_auth_me():
    res = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {auth_token}"})
    assert res.status_code == 200, f"Got {res.status_code}: {res.text}"
    data = res.json()
    assert data["user"]["email"] == test_user_email

def test_auth_preferences():
    res = client.put(
        "/api/v1/auth/preferences",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "home_currency": "EUR",
            "travel_style": "Luxury",
            "interests": "Gastronomy, Art",
        },
    )
    assert res.status_code == 200, f"Got {res.status_code}: {res.text}"
    data = res.json()
    assert data["preferences"]["travel_style"] == "Luxury"

test_endpoint("POST /api/v1/auth/register", test_register)
test_endpoint("POST /api/v1/auth/login", test_login)
test_endpoint("GET /api/v1/auth/me", test_auth_me)
test_endpoint("PUT /api/v1/auth/preferences", test_auth_preferences)

# --- 3. Trips Endpoints ---
print("\n--- Testing Trips Endpoints ---")
created_trip_id = None

def test_create_trip():
    global created_trip_id
    res = client.post(
        "/api/v1/trips",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "destination": "Kyoto, Japan",
            "days": 5,
            "travelers": 2,
            "budget": 4500.0,
            "interests": "Temples, Gardens, Kaiseki",
            "travelStyle": "Mid-range",
            "currency": "USD",
        },
    )
    assert res.status_code in [201, 200], f"Got {res.status_code}: {res.text}"
    data = res.json()
    assert "trip" in data
    created_trip_id = data["trip"]["id"]

def test_list_trips():
    res = client.get("/api/v1/trips", headers={"Authorization": f"Bearer {auth_token}"})
    assert res.status_code == 200, f"Got {res.status_code}: {res.text}"
    data = res.json()
    assert "trips" in data
    assert len(data["trips"]) >= 1

def test_get_trip_detail():
    res = client.get(f"/api/v1/trips/{created_trip_id}", headers={"Authorization": f"Bearer {auth_token}"})
    assert res.status_code == 200, f"Got {res.status_code}: {res.text}"
    data = res.json()
    assert data["trip"]["id"] == created_trip_id

def test_add_traveler():
    res = client.post(
        f"/api/v1/trips/{created_trip_id}/travelers",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "name": "Companion Traveler",
            "email": "companion@example.com",
            "role": "companion",
        },
    )
    assert res.status_code in [201, 200], f"Got {res.status_code}: {res.text}"
    data = res.json()
    assert "traveler_id" in data

test_endpoint("POST /api/v1/trips", test_create_trip)
test_endpoint("GET /api/v1/trips", test_list_trips)
test_endpoint("GET /api/v1/trips/{id}", test_get_trip_detail)
test_endpoint("POST /api/v1/trips/{id}/travelers", test_add_traveler)

# --- 4. Routes Endpoints ---
print("\n--- Testing Routes Endpoints ---")

def test_plan_route():
    res = client.post("/api/v1/routes/plan", json={
        "origin": "Tokyo Station",
        "destination": "Kyoto Station",
        "mode": "transit",
    })
    assert res.status_code == 200, f"Got {res.status_code}: {res.text}"
    data = res.json()
    assert "route" in data
    assert data["route"]["origin"] == "Tokyo Station"

def test_route_history():
    res = client.get("/api/v1/routes/history")
    assert res.status_code == 200, f"Got {res.status_code}: {res.text}"
    data = res.json()
    assert "routes" in data

test_endpoint("POST /api/v1/routes/plan", test_plan_route)
test_endpoint("GET /api/v1/routes/history", test_route_history)

# --- 5. Places Endpoints ---
print("\n--- Testing Places Endpoints ---")

def test_places_search():
    res = client.get("/api/v1/places/search", params={"query": "Kyoto", "limit": 3})
    assert res.status_code == 200, f"Got {res.status_code}: {res.text}"
    data = res.json()
    assert "places" in data
    assert len(data["places"]) > 0

def test_save_place():
    res = client.post(
        "/api/v1/places/saved",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "name": "Fushimi Inari Taisha",
            "trip_id": created_trip_id,
            "notes": "Must visit early morning to avoid crowds",
        },
    )
    assert res.status_code in [201, 200], f"Got {res.status_code}: {res.text}"

def test_get_saved_places():
    res = client.get(
        "/api/v1/places/saved",
        headers={"Authorization": f"Bearer {auth_token}"},
        params={"trip_id": created_trip_id},
    )
    assert res.status_code == 200, f"Got {res.status_code}: {res.text}"
    data = res.json()
    assert len(data["saved_places"]) > 0

test_endpoint("GET /api/v1/places/search", test_places_search)
test_endpoint("POST /api/v1/places/saved", test_save_place)
test_endpoint("GET /api/v1/places/saved", test_get_saved_places)

# --- 6. Weather & Currency Endpoints ---
print("\n--- Testing Weather & Currency Endpoints ---")

def test_weather():
    res = client.get("/api/v1/weather", params={"city": "Kyoto", "days": 3})
    assert res.status_code == 200, f"Got {res.status_code}: {res.text}"
    data = res.json()
    assert "weather" in data
    assert data["weather"]["city"].lower() == "kyoto"

def test_currency_rates():
    res = client.get("/api/v1/currency/rates", params={"base": "USD"})
    assert res.status_code == 200, f"Got {res.status_code}: {res.text}"
    data = res.json()
    assert "rates" in data

def test_currency_convert():
    res = client.post("/api/v1/currency/convert", json={
        "amount": 100.0,
        "from_currency": "USD",
        "to_currency": "EUR",
    })
    assert res.status_code == 200, f"Got {res.status_code}: {res.text}"
    data = res.json()
    assert "converted_amount" in data
    assert data["converted_amount"] > 0

test_endpoint("GET /api/v1/weather", test_weather)
test_endpoint("GET /api/v1/currency/rates", test_currency_rates)
test_endpoint("POST /api/v1/currency/convert", test_currency_convert)

# --- 7. Flights, Hotels & Restaurants Endpoints ---
print("\n--- Testing Flights, Hotels & Restaurants Endpoints ---")

def test_flights_search():
    res = client.get("/api/v1/flights/search", params={"origin": "SFO", "destination": "HND"})
    assert res.status_code == 200, f"Got {res.status_code}: {res.text}"
    data = res.json()
    assert "flights" in data
    assert len(data["flights"]) > 0

def test_flights_reserve():
    res = client.post(
        "/api/v1/flights/reserve",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "trip_id": created_trip_id,
            "airline": "ANA",
            "flight_number": "NH107",
            "departure_airport": "SFO",
            "arrival_airport": "HND",
            "price": 850.0,
            "currency": "USD",
        },
    )
    assert res.status_code in [201, 200], f"Got {res.status_code}: {res.text}"
    data = res.json()
    assert "reservation_id" in data

def test_hotels_search():
    res = client.get("/api/v1/hotels/search", params={"city": "Kyoto"})
    assert res.status_code == 200, f"Got {res.status_code}: {res.text}"
    data = res.json()
    assert "hotels" in data
    assert len(data["hotels"]) > 0

def test_hotels_reserve():
    res = client.post(
        "/api/v1/hotels/reserve",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "trip_id": created_trip_id,
            "name": "Kyoto Machiya Ryokan",
            "city": "Kyoto",
            "price_per_night": 190.0,
            "nights": 4,
            "currency": "USD",
        },
    )
    assert res.status_code in [201, 200], f"Got {res.status_code}: {res.text}"
    data = res.json()
    assert "reservation_id" in data

def test_restaurants_search():
    res = client.get("/api/v1/restaurants/search", params={"city": "Kyoto"})
    assert res.status_code == 200, f"Got {res.status_code}: {res.text}"
    data = res.json()
    assert "restaurants" in data
    assert len(data["restaurants"]) > 0

def test_restaurants_reserve():
    res = client.post(
        "/api/v1/restaurants/reserve",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "trip_id": created_trip_id,
            "name": "Gion Karyo",
            "city": "Kyoto",
            "party_size": 2,
        },
    )
    assert res.status_code in [201, 200], f"Got {res.status_code}: {res.text}"
    data = res.json()
    assert "reservation_id" in data

test_endpoint("GET /api/v1/flights/search", test_flights_search)
test_endpoint("POST /api/v1/flights/reserve", test_flights_reserve)
test_endpoint("GET /api/v1/hotels/search", test_hotels_search)
test_endpoint("POST /api/v1/hotels/reserve", test_hotels_reserve)
test_endpoint("GET /api/v1/restaurants/search", test_restaurants_search)
test_endpoint("POST /api/v1/restaurants/reserve", test_restaurants_reserve)

# --- 8. Transport & Budget Endpoints ---
print("\n--- Testing Transport & Budget Endpoints ---")

def test_transport_options():
    res = client.get("/api/v1/transport/options", params={"origin": "Kansai Airport", "destination": "Kyoto Station"})
    assert res.status_code == 200, f"Got {res.status_code}: {res.text}"
    data = res.json()
    assert "options" in data
    assert len(data["options"]) > 0

def test_transport_book():
    res = client.post(
        "/api/v1/transport/book",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "trip_id": created_trip_id,
            "origin": "Kansai Airport",
            "destination": "Kyoto Station",
            "mode": "train",
            "cost": 30.0,
            "currency": "USD",
        },
    )
    assert res.status_code in [201, 200], f"Got {res.status_code}: {res.text}"

def test_budget_set():
    res = client.post(
        f"/api/v1/budget/{created_trip_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "total_budget": 4500.0,
            "currency": "USD",
            "flights_allocated": 1000.0,
            "accommodation_allocated": 1500.0,
            "food_allocated": 1000.0,
            "activities_allocated": 500.0,
            "transit_allocated": 300.0,
            "misc_allocated": 200.0,
        },
    )
    assert res.status_code == 200, f"Got {res.status_code}: {res.text}"

def test_budget_get():
    res = client.get(f"/api/v1/budget/{created_trip_id}", headers={"Authorization": f"Bearer {auth_token}"})
    assert res.status_code == 200, f"Got {res.status_code}: {res.text}"
    data = res.json()
    assert data["total_budget"] == 4500.0

def test_add_expense():
    res = client.post(
        f"/api/v1/budget/{created_trip_id}/expenses",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "category": "food",
            "amount": 85.0,
            "currency": "USD",
            "description": "Lunch at Nishiki Market",
        },
    )
    assert res.status_code in [201, 200], f"Got {res.status_code}: {res.text}"

test_endpoint("GET /api/v1/transport/options", test_transport_options)
test_endpoint("POST /api/v1/transport/book", test_transport_book)
test_endpoint("POST /api/v1/budget/{id}", test_budget_set)
test_endpoint("GET /api/v1/budget/{id}", test_budget_get)
test_endpoint("POST /api/v1/budget/{id}/expenses", test_add_expense)

# --- 9. Concierge & Replan Endpoints ---
print("\n--- Testing Concierge & Replan Endpoints ---")
conv_id = None

def test_concierge_chat():
    global conv_id
    res = client.post(
        "/api/v1/concierge/chat",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "trip_id": created_trip_id,
            "message": "What should I pack for Kyoto in spring?",
        },
    )
    assert res.status_code == 200, f"Got {res.status_code}: {res.text}"
    data = res.json()
    assert "conversation_id" in data
    assert "message" in data
    conv_id = data["conversation_id"]

def test_concierge_conversations():
    res = client.get(
        "/api/v1/concierge/conversations",
        headers={"Authorization": f"Bearer {auth_token}"},
        params={"trip_id": created_trip_id},
    )
    assert res.status_code == 200, f"Got {res.status_code}: {res.text}"
    data = res.json()
    assert data["count"] > 0

def test_replan_trip():
    res = client.post(
        "/api/v1/replan/",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "trip_id": created_trip_id,
            "change_type": "budget",
            "new_value": 5200.0,
            "reason": "Increased budget for fine dining",
        },
    )
    assert res.status_code == 200, f"Got {res.status_code}: {res.text}"
    data = res.json()
    assert data["trip"]["budget"] == 5200.0

def test_replan_history():
    res = client.get(
        f"/api/v1/replan/history/{created_trip_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert res.status_code == 200, f"Got {res.status_code}: {res.text}"
    data = res.json()
    assert data["events_count"] >= 1

test_endpoint("POST /api/v1/concierge/chat", test_concierge_chat)
test_endpoint("GET /api/v1/concierge/conversations", test_concierge_conversations)
test_endpoint("POST /api/v1/replan/", test_replan_trip)
test_endpoint("GET /api/v1/replan/history/{id}", test_replan_history)

# --- 10. Structured Error Format & Security Verification ---
print("\n--- Testing Structured Error Format & Security ---")

def test_structured_error_404():
    res = client.get("/api/v1/trips/99999999")
    assert res.status_code == 404, f"Expected 404, got {res.status_code}"
    data = res.json()
    assert "error" in data, "Error response must contain top-level 'error' key"
    err = data["error"]
    assert "code" in err, "Error must contain 'code'"
    assert "message" in err, "Error must contain 'message'"
    assert "request_id" in err, "Error must contain 'request_id'"

def test_structured_error_validation_422():
    res = client.post("/api/v1/trips", json={"destination": ""})
    assert res.status_code == 422, f"Expected 422, got {res.status_code}"
    data = res.json()
    assert "error" in data
    assert "code" in data["error"]
    assert "request_id" in data["error"]

def test_security_headers():
    res = client.get("/health")
    assert "X-Request-ID" in res.headers
    assert res.headers.get("X-Content-Type-Options") == "nosniff"
    assert res.headers.get("X-Frame-Options") == "DENY"

test_endpoint("Structured 404 Error Format", test_structured_error_404)
test_endpoint("Structured 422 Validation Error Format", test_structured_error_validation_422)
test_endpoint("Security Headers & Request ID", test_security_headers)

# --- Summary ---
print(f"\n==========================================")
print(f"Results: {passed} PASSED, {failed} FAILED")
print(f"==========================================")

if failed > 0:
    sys.exit(1)
else:
    sys.exit(0)
