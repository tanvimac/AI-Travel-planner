import React, { useState } from 'react';
import {
  MapPin,
  Calendar,
  Users,
  Wallet,
  Compass,
  Sparkles,
  Loader2,
  CheckCircle2,
  Navigation,
  ArrowRight,
  Menu,
  X,
  Globe,
} from 'lucide-react';
import './App.css';
import './index.css';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import PlannerCard from './components/PlannerCard';
import LoadingAgentsCard from './components/LoadingAgentsCard';
import TripSummaryCard from './components/TripSummaryCard';
import ItineraryPlaceholder from './components/ItineraryPlaceholder';
import AgentsSection from './components/AgentsSection';
import HowItWorks from './components/HowItWorks';
import SampleItinerary from './components/SampleItinerary';
import FeaturesSection from './components/FeaturesSection';
import Footer from './components/Footer';
import ErrorCard from './components/ErrorCard';

function App() {
  const [destination, setDestination] = useState('');
  const [days, setDays] = useState('');
  const [travelers, setTravelers] = useState(1);
  const [budget, setBudget] = useState('');
  const [travelStyle, setTravelStyle] = useState('Mid-range');
  const [interests, setInterests] = useState('');
  const [responseData, setResponseData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const travelStyles = [
    { label: 'Culture', icon: '🏛️' },
    { label: 'Beaches', icon: '🏖️' },
    { label: 'Food & Wine', icon: '🍜' },
    { label: 'Adventure', icon: '⛰️' },
    { label: 'Relaxation', icon: '🌴' },
    { label: 'Luxury', icon: '✨' },
  ];

  const handleStyleSelect = (styleLabel) => {
    if (!interests) {
      setInterests(styleLabel);
    } else if (interests.toLowerCase().includes(styleLabel.toLowerCase())) {
      const updated = interests
        .split(',')
        .map((s) => s.trim())
        .filter((s) => s.toLowerCase() !== styleLabel.toLowerCase())
        .join(', ');

      setInterests(updated);
    } else {
      setInterests(`${interests}, ${styleLabel}`);
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    setResponseData(null);
    setError(null);
    setIsLoading(true);

    const travelData = {
      destination,
      days: Number(days),
      travelers: Number(travelers),
      budget: Number(budget),
      interests,
      travelStyle,
    };

    const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

    try {
      // Create the trip
      const response = await fetch(`${apiBaseUrl}/api/plan`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(travelData),
      });

      if (!response.ok) {
        throw new Error('Failed to create trip');
      }

      const data = await response.json();
      const tripId = data.id;

      // Check the trip status until the background agents finish
      const checkTripStatus = async () => {
        try {
          const tripResponse = await fetch(
            `${apiBaseUrl}/api/trips/${tripId}`
          );

          if (!tripResponse.ok) {
            throw new Error('Failed to check trip status');
          }

          const tripData = await tripResponse.json();

          if (tripData.status === 'completed') {
            setResponseData(tripData);
            setIsLoading(false);
            return;
          }

          if (tripData.status === 'failed') {
            throw new Error('Trip generation failed');
          }

          // Still processing — check again after 3 seconds
          setTimeout(checkTripStatus, 3000);
        } catch (err) {
          console.error('Trip status error:', err);
          setError('Failed to generate itinerary. Please try again.');
          setIsLoading(false);
        }
      };

      await checkTripStatus();
    } catch (err) {
      console.error('Error:', err);
      setError('Failed to generate itinerary. Please try again.');
      setIsLoading(false);
    }
  };

  const handleRetry = () => {
    handleSubmit(new Event('submit'));
  };

  return (
    <div className="app-container">
      <Navbar />

      <Hero />

      <main className="main-wrapper">
        <PlannerCard
          destination={destination}
          setDestination={setDestination}
          days={days}
          setDays={setDays}
          travelers={travelers}
          setTravelers={setTravelers}
          budget={budget}
          setBudget={setBudget}
          travelStyle={travelStyle}
          setTravelStyle={setTravelStyle}
          interests={interests}
          setInterests={setInterests}
          travelStyles={travelStyles}
          handleStyleSelect={handleStyleSelect}
          handleSubmit={handleSubmit}
          isLoading={isLoading}
        />

        <HowItWorks />

        <SampleItinerary />

        {isLoading && <LoadingAgentsCard />}

        {error && <ErrorCard error={error} onRetry={handleRetry} />}

        {responseData && !isLoading && (
          <>
            <TripSummaryCard data={responseData} />

            {responseData.status === 'completed' &&
              responseData.itinerary && (
                <div className="trip-ticket-card itinerary-result-card">
                  <div className="ticket-header">
                    <div className="ticket-header-left">
                      <div className="ticket-plane-badge">
                        <CheckCircle2 size={20} />
                      </div>

                      <div>
                        <h3 className="ticket-title">
                          {responseData.itinerary.title ||
                            'Your AI Itinerary'}
                        </h3>

                        <p className="ticket-subtitle">
                          Your personalized journey is ready ✨
                        </p>
                      </div>
                    </div>

                    <span className="ticket-tag completed-tag">
                      completed
                    </span>
                  </div>

                  <div className="ticket-body">
                    {responseData.itinerary.summary && (
                      <p className="ticket-alert-msg">
                        {responseData.itinerary.summary}
                      </p>
                    )}

                    {responseData.itinerary.data?.days?.map((day) => (
                      <div
                        className="itinerary-day-card"
                        key={day.day}
                      >
                        <div className="itinerary-day-number">
                          Day {day.day}
                        </div>

                        <div className="itinerary-day-content">
                          <p>{day.plan}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

            {responseData.status === 'pending' && (
              <ItineraryPlaceholder />
            )}
          </>
        )}

        <AgentsSection />

        <FeaturesSection />

        <Footer />
      </main>
    </div>
  );
}

export default App;