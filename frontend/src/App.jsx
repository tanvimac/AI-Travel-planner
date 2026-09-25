import { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import HomeView from './components/HomeView';
import CreateTripView from './components/CreateTripView';
import SavedTripsView from './components/SavedTripsView';
import TripDetailsView from './components/TripDetailsView';
import {
  INITIAL_SAVED_TRIPS,
  generateItineraryForTrip,
} from './data/tripsData';
import './App.css';
import './index.css';

function App() {
  // Navigation view: 'home' | 'create' | 'saved' | 'details'
  const [currentView, setCurrentView] = useState('home');

  // Initialize trips from localStorage or seed dataset
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
    return INITIAL_SAVED_TRIPS;
  });

  // Selected trip for details view
  const [selectedTrip, setSelectedTrip] = useState(() => trips[0] || null);

  // Sync trips to localStorage
  useEffect(() => {
    try {
      localStorage.setItem('ai_travel_trips', JSON.stringify(trips));
    } catch (e) {
      console.error('Error saving trips to localStorage:', e);
    }
  }, [trips]);

  // Optionally fetch saved trips from backend on mount
  useEffect(() => {
    const fetchBackendTrips = async () => {
      try {
        const apiBaseUrl =
          import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';
        const res = await fetch(`${apiBaseUrl}/api/trips`);
        if (res.ok) {
          const backendData = await res.json();
          if (Array.isArray(backendData) && backendData.length > 0) {
            console.log('Fetched trips from backend:', backendData);
          }
        }
      } catch (err) {
        console.warn('Backend fetch notice:', err);
      }
    };
    fetchBackendTrips();
  }, []);

  const handleStartPlanning = () => {
    setCurrentView('create');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleTripCreated = (formData) => {
    const newTrip = generateItineraryForTrip(formData);
    setTrips((prev) => [newTrip, ...prev]);
    setSelectedTrip(newTrip);
    setCurrentView('details');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleSelectTrip = (trip) => {
    setSelectedTrip(trip);
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