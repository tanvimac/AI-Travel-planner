"""
Test suite verifying all API endpoints, database integration, and responses.
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_endpoints():
    print("Testing GET /...")
    res = client.get("/")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    print("  -> Passed:", res.json())

    print("Testing GET /health...")
    res = client.get("/health")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    assert res.json().get("status") == "healthy"
    print("  -> Passed:", res.json())

    print("Testing GET /api/db-test...")
    res = client.get("/api/db-test")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    assert res.json().get("status") == "success"
    print("  -> Passed:", res.json()["database"]["status"])

    print("Testing GET /api/trips...")
    res = client.get("/api/trips")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    trips = res.json()
    assert isinstance(trips, list), "Expected list of trips"
    print(f"  -> Passed: {len(trips)} trips fetched from database")
    if trips:
        first_trip = trips[0]
        assert "status" in first_trip, "Trip must contain 'status' field!"
        print(f"  -> First trip: id={first_trip['id']}, dest={first_trip['destination']}, status={first_trip['status']}")

        print(f"Testing GET /api/trips/{first_trip['id']}...")
        detail_res = client.get(f"/api/trips/{first_trip['id']}")
        assert detail_res.status_code == 200
        detail = detail_res.json()
        assert detail["id"] == first_trip["id"]
        print(f"  -> Passed: trip {detail['id']} detail loaded (has_itinerary={detail.get('itinerary') is not None})")

    print("Testing POST /api/plan...")
    plan_payload = {
        "destination": "Zurich, Switzerland",
        "days": 4,
        "travelers": 2,
        "budget": 6000.0,
        "interests": "alps, fondue, trains",
        "travelStyle": "Mid-range"
    }
    plan_res = client.post("/api/plan", json=plan_payload)
    assert plan_res.status_code == 200, f"Expected 200, got {plan_res.status_code}: {plan_res.text}"
    plan_data = plan_res.json()
    assert "id" in plan_data, "Response must include trip id"
    assert plan_data["status"] == "pending", "Initial trip status must be pending"
    print(f"  -> Passed: Created new trip ID {plan_data['id']} with status={plan_data['status']}")

    print("\nALL API ENDPOINTS VERIFIED SUCCESSFULLY!")

if __name__ == "__main__":
    test_endpoints()
