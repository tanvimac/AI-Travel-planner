/**
 * API Service for AI Travel Planner
 * Centralizes all communication with FastAPI backend.
 * Uses VITE_API_BASE_URL environment variable with fallback to http://127.0.0.1:8000.
 */

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

export async function fetchHealth() {
  const res = await fetch(`${API_BASE_URL}/health`);
  if (!res.ok) throw new Error(`Health check failed: ${res.statusText}`);
  return res.json();
}

export async function createTripPlan(payload) {
  const res = await fetch(`${API_BASE_URL}/api/plan`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const errorBody = await res.json().catch(() => ({}));
    throw new Error(
      errorBody.detail || `Failed to create trip plan (${res.status})`
    );
  }
  return res.json(); // { id: number, status: 'pending' }
}

export async function fetchAllTrips() {
  const res = await fetch(`${API_BASE_URL}/api/trips`);
  if (!res.ok) {
    throw new Error(`Failed to fetch trips (${res.status})`);
  }
  return res.json();
}

export async function fetchTripById(tripId) {
  const res = await fetch(`${API_BASE_URL}/api/trips/${tripId}`);
  if (!res.ok) {
    throw new Error(`Failed to fetch trip ${tripId} (${res.status})`);
  }
  return res.json();
}

/**
 * Polls trip status until it reaches 'completed' or 'failed', or times out.
 * @param {number} tripId 
 * @param {function} onPoll - Callback receiving intermediate trip status
 * @param {number} intervalMs - Polling interval in ms (default 2000)
 * @param {number} maxAttempts - Maximum polling attempts (default 60 = 2 minutes)
 */
export async function pollTripUntilReady(
  tripId,
  onPoll = () => {},
  intervalMs = 2000,
  maxAttempts = 60
) {
  let attempts = 0;
  while (attempts < maxAttempts) {
    attempts++;
    await new Promise((r) => setTimeout(r, intervalMs));
    try {
      const trip = await fetchTripById(tripId);
      onPoll(trip, attempts);
      if (trip.status === 'completed') {
        return trip;
      }
      if (trip.status === 'failed') {
        throw new Error(
          'AI Travel planning encountered an issue while generating the itinerary. Please try again.'
        );
      }
    } catch (err) {
      if (err.message && err.message.includes('AI Travel planning')) {
        throw err;
      }
      // Transient network error during polling, continue polling
      console.warn(`Polling attempt ${attempts} warning:`, err);
    }
  }
  throw new Error('Trip planning timed out. Please check Saved Trips shortly.');
}

/**
 * Normalizes backend trip data to match frontend view expectations.
 */
export function normalizeTrip(backendTrip) {
  if (!backendTrip) return null;

  const itin = backendTrip.itinerary || {};
  const itinData = itin.data || {};
  const rawDays = itinData.days || [];

  // Transform raw days into displayable format
  const normalizedItinerary = rawDays.map((d) => ({
    day: d.day,
    title: d.title || `Day ${d.day}: ${backendTrip.destination}`,
    bullets: Array.isArray(d.plan)
      ? d.plan
      : typeof d.plan === 'string'
      ? [d.plan]
      : Array.isArray(d.activities)
      ? d.activities
      : ['Activities and sightseeing planned.'],
    image: null,
  }));

  const createdDate = backendTrip.created_at
    ? new Date(backendTrip.created_at).toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
      })
    : 'Recently';

  return {
    id: backendTrip.id,
    destination: backendTrip.destination,
    days: backendTrip.days,
    travelers: backendTrip.travelers,
    budget: backendTrip.budget,
    formattedBudget: `$ ${Number(backendTrip.budget).toLocaleString()}`,
    travelStyle: backendTrip.travelStyle || 'Mid-range',
    status: backendTrip.status || 'pending',
    tags: backendTrip.interests
      ? backendTrip.interests.split(',').map((s) => s.trim()).filter(Boolean)
      : [],
    createdAt: createdDate,
    title: itin.title || `Itinerary for ${backendTrip.destination}`,
    description:
      itin.summary ||
      `A customized ${backendTrip.days}-day trip to ${backendTrip.destination} for ${backendTrip.travelers} traveler(s).`,
    rawMarkdown: itin.markdown || null,
    itinerary: normalizedItinerary,
    highlights: itinData.highlights || [],
    travelTips: itinData.tips || [],
  };
}
