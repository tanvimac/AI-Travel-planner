import { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import HomeView from './components/HomeView';
import CreateTripView from './components/CreateTripView';
import SavedTripsView from './components/SavedTripsView';
import TripDetailsView from './components/TripDetailsView';
import {
  fetchAllTrips,
  fetchTripById,
  normalizeTrip,
} from './services/api';
import './App.css';
import './index.css';

function App() {
  // Navigation view: 'home' | 'create' | 'saved' | 'details'
  const [currentView, setCurrentView] = useState('home');

  // Initialize trips state
  const [trips, setTrips] = useState(() => {
    try {
      const stored = localStorage.getItem('ai_travel_trips');
      if (stored) {
        const parsed = JSON.parse(stored);
        if (Array.isArray(parsed) && parsed.length > 0) {
          return parsed;
        }
      }
    } catch (e) {
      console.error('Error loading stored trips:', e);
    }
    return [];
  });

  // Selected trip for details view
  const [selectedTrip, setSelectedTrip] = useState(() => trips[0] || null);

  // Sync trips to localStorage as offline cache
  useEffect(() => {
    try {
      if (trips && trips.length > 0) {
        localStorage.setItem('ai_travel_trips', JSON.stringify(trips));
      }
    } catch (e) {
      console.error('Error saving trips to localStorage:', e);
    }
  }, [trips]);

  // Fetch real trips from backend on mount
  useEffect(() => {
    const fetchBackendTrips = async () => {
      try {
        const backendData = await fetchAllTrips();
        if (Array.isArray(backendData) && backendData.length > 0) {
          const normalized = backendData.map(normalizeTrip);
          setTrips(normalized);
          setSelectedTrip((prev) => prev || normalized[0]);
        }
      } catch (err) {
        console.warn('Backend fetch notice (using cached trips):', err);
      }
    };
    fetchBackendTrips();
  }, []);

  const handleStartPlanning = () => {
    setCurrentView('create');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleTripCreated = (readyTrip) => {
    const normalized = normalizeTrip(readyTrip);
    setTrips((prev) => [
      normalized,
      ...prev.filter((t) => t.id !== normalized.id),
    ]);
    setSelectedTrip(normalized);
    setCurrentView('details');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleSelectTrip = async (trip) => {
    // If details/itinerary are not yet populated, fetch full trip by ID
    if (!trip.itinerary || trip.itinerary.length === 0) {
      try {
        const fullTrip = await fetchTripById(trip.id);
        const normalized = normalizeTrip(fullTrip);
        setSelectedTrip(normalized);
        setTrips((prev) =>
          prev.map((t) => (t.id === normalized.id ? normalized : t))
        );
      } catch (err) {
        console.warn('Failed to fetch full trip details, using summary:', err);
        setSelectedTrip(trip);
      }
    } else {
      setSelectedTrip(trip);
    }
    setCurrentView('details');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleBackToSaved = () => {
    setCurrentView('saved');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleBackToHome = () => {
    setCurrentView('home');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="travel-planner-app">
      {/* Sticky top Navigation Bar */}
      <Navbar currentView={currentView} setView={setCurrentView} />

      {/* Main Body depending on currentView */}
      <main className="main-content-area">
        {currentView === 'home' && (
          <HomeView onStartPlanning={handleStartPlanning} />
        )}

        {currentView === 'create' && (
          <CreateTripView
            onBackHome={handleBackToHome}
            onTripCreated={handleTripCreated}
          />
        )}

        {currentView === 'saved' && (
          <SavedTripsView
            trips={trips}
            onSelectTrip={handleSelectTrip}
            onNewTrip={() => setCurrentView('create')}
          />
        )}

        {currentView === 'details' && (
          <TripDetailsView
            trip={selectedTrip || trips[0]}
            onBack={handleBackToSaved}
          />
        )}
      </main>
    </div>
  );
}

export default App;