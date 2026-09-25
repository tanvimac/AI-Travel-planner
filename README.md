# 🌍 AI Travel Planner

An intelligent, multi-agent AI travel planning application that designs personalized travel itineraries tailored to destination, dates, budget, travel style, and interests.

Powered by **FastAPI**, **PostgreSQL**, **Google Gemini SDK (`google-genai`)**, and **React + Vite**.

---

## 🚀 Features

- **Multi-Agent Architecture**:
  - **Destination Agent**: Researches destination highlights, cultural tips, and seasonal guidance.
  - **Hotel Agent**: Suggests lodging recommendations tailored to budget and style.
  - **Food Agent**: Recommends top local culinary spots, restaurants, and cuisine specialties.
  - **Activity Agent**: Crafts day-by-day activity outlines matching travelers' interests.
  - **Budget Agent**: Computes categorized financial estimates (flights, accommodation, food, activities).
  - **Itinerary Agent**: Synthesizes all intelligence into a cohesive, day-by-day plan with markdown and structured JSON.
- **Concurrent Processing**: Independent agents run in parallel via `ThreadPoolExecutor` for fast turnaround.
- **Resilient AI Pipeline**: Intelligent retry back-off for Google Gemini `503 UNAVAILABLE` and `429 RESOURCE_EXHAUSTED` quotas with automated delay extraction.
- **Agent Fault Isolation**: Sectional fallbacks ensure trips still complete successfully even if a single agent encounters external service limits.
- **Modern UI**: Intuitive, responsive React interface built with Lucide icons and Vite.

---

## 🏗️ Architecture

```
[ Frontend (React + Vite) ]
          │
          ▼  POST /api/plan
[ FastAPI Backend ] ───► [ PostgreSQL (Trips & Itineraries) ]
          │
     Background Task
          │
          ▼
   [ Orchestrator ]
    ├──► DestinationAgent ──┐
    ├──► HotelAgent       ──┤
    ├──► FoodAgent        ──┼─► Concurrently executed via Gemini Flash
    ├──► ActivityAgent    ──┤
    └──► BudgetAgent      ──┘
          │
          ▼
    [ ItineraryAgent ]  ─────► Final Synthesis (Structured JSON + Markdown)
```

---

## 🛠️ Tech Stack

- **Backend**: Python 3.11+, FastAPI, SQLAlchemy, PostgreSQL (`psycopg2-binary`), `google-genai` SDK
- **Frontend**: React 18, Vite, Lucide React, Modern CSS
- **AI Models**: Google Gemini (`gemini-3.8-flash` or configurable via settings)

---

## 📦 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+ & npm
- PostgreSQL database
- Google Gemini API key ([Google AI Studio](https://aistudio.google.com/))

---

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
```

Edit `backend/.env` with your credentials:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=travel_planner
DB_USER=postgres
DB_PASSWORD=your_password

GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.8-flash
GEMINI_MIN_INTERVAL=1.0
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

Start the backend server:

```bash
uvicorn main:app --reload --port 8000
```

> **Note**: Database tables (`trips`, `itineraries`) are created and verified automatically on startup via the FastAPI lifespan hook.

---

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment variables
cp .env.example .env
```

Ensure `frontend/.env` has:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Start the development server:

```bash
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

---

## 📡 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | API root check |
| `GET` | `/health` | Health check endpoint |
| `GET` | `/api/test` | Diagnostic test route |
| `GET` | `/api/db-test` | Test PostgreSQL database connectivity |
| `POST` | `/api/plan` | Create a new trip planning request (runs agents in background) |
| `GET` | `/api/trips/{id}` | Fetch trip status and generated itinerary |

---

## 🧪 Verification & Testing

The backend includes test scripts in `backend/tmp/`:

```bash
# Verify database connection
python backend/tmp/setup_db.py

# Verify Gemini model generation
python backend/tmp/destination_test.py

# Verify rate-limit retry logic
python backend/tmp/test_gemini_retry.py

# Verify agent fault isolation
python backend/tmp/test_agent_isolation.py

# Verify full end-to-end trip pipeline
python backend/tmp/verify_pipeline.py
```

---

## 📄 License

This project is licensed under the MIT License.
