import { useState } from 'react';
import {
  ArrowLeft,
  Briefcase,
  MapPin,
  Calendar,
  Users,
  DollarSign,
  Tag,
  Star,
  Sparkles,
  Loader2,
} from 'lucide-react';

import { createTripPlan, pollTripUntilReady } from '../services/api';

const CreateTripView = ({ onBackHome, onTripCreated }) => {
  const [destination, setDestination] = useState('');
  const [days, setDays] = useState('7');
  const [travelers, setTravelers] = useState('2');
  const [budget, setBudget] = useState('120000');
  const [interests, setInterests] = useState('food, anime, nature, history');
  const [travelStyle, setTravelStyle] = useState('Luxury');
  const [isGenerating, setIsGenerating] = useState(false);
  const [generationStep, setGenerationStep] = useState(0);
  const [errorMessage, setErrorMessage] = useState(null);

  const steps = [
    'Analyzing destination & travel preferences...',
    'Consulting Hotel & Food AI agents...',
    'Curating personalized daily activities...',
    'Optimizing schedule & budget allocations...',
    'Finalizing your customized itinerary ✨',
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!destination.trim()) {
      setErrorMessage('Please enter a destination.');
      return;
    }

    setErrorMessage(null);
    setIsGenerating(true);
    setGenerationStep(0);

    const tripPayload = {
      destination: destination.trim(),
      days: parseInt(days, 10) || 7,
      travelers: parseInt(travelers, 10) || 2,
      budget: parseFloat(budget) || 50000,
      interests: interests.trim(),
      travelStyle,
    };

    const stepInterval = setInterval(() => {
      setGenerationStep((prev) => (prev < steps.length - 1 ? prev + 1 : prev));
    }, 2000);

    try {
      // Step 1: Submit trip to real FastAPI backend
      const planResult = await createTripPlan(tripPayload);

      // Step 2: Poll backend until background agent orchestration completes
      const readyTrip = await pollTripUntilReady(
        planResult.id,
        (_interim, attempt) => {
          setGenerationStep((prev) =>
            Math.min(steps.length - 1, Math.max(prev, Math.floor(attempt / 2)))
          );
        }
      );

      clearInterval(stepInterval);
      setIsGenerating(false);
      onTripCreated(readyTrip);
    } catch (err) {
      clearInterval(stepInterval);
      setIsGenerating(false);
      setErrorMessage(
        err.message || 'Failed to generate itinerary. Please try again.'
      );
    }
  };

  return (
    <div className="create-trip-page-container">
      {/* Back button */}
      <button
        className="back-nav-link-btn"
        onClick={onBackHome}
        aria-label="Back to Home"
      >
        <ArrowLeft size={16} />
        <span>Back to Home</span>
      </button>

      {/* Main Form Card */}
      <div className="create-trip-card">
        {/* Card Header */}
        <div className="create-card-header">
          <div className="briefcase-icon-badge">
            <Briefcase size={22} color="#ffffff" />
          </div>
          <div>
            <h2 className="create-card-title">Create a New Trip</h2>
            <p className="create-card-subtitle">
              Tell us your travel preferences and let our AI plan the perfect trip
              for you.
            </p>
          </div>
        </div>

        {errorMessage && (
          <div
            className="create-error-banner"
            style={{
              padding: '0.85rem 1.25rem',
              marginBottom: '1.25rem',
              backgroundColor: '#FEF2F2',
              border: '1px solid #F87171',
              borderRadius: '8px',
              color: '#B91C1C',
              fontSize: '0.9rem',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
            }}
          >
            <span>⚠️ {errorMessage}</span>
          </div>
        )}

        {/* The Form */}
        <form onSubmit={handleSubmit} className="trip-form">
          <div className="form-grid-2col">
            {/* Destination */}
            <div className="form-group">
              <label className="field-label" htmlFor="destination-input">
                Destination
              </label>
              <div className="field-input-wrapper">
                <MapPin size={18} className="field-icon" />
                <input
                  id="destination-input"
                  type="text"
                  className="styled-text-input"
                  placeholder="e.g. Tokyo, Japan"
                  value={destination}
                  onChange={(e) => setDestination(e.target.value)}
                  required
                />
              </div>
            </div>

            {/* Number of Days */}
            <div className="form-group">
              <label className="field-label" htmlFor="days-select">
                Number of Days
              </label>
              <div className="field-input-wrapper">
                <Calendar size={18} className="field-icon" />
                <select
                  id="days-select"
                  className="styled-select-input"
                  value={days}
                  onChange={(e) => setDays(e.target.value)}
                >
                  <option value="3">3 Days</option>
                  <option value="5">5 Days</option>
                  <option value="7">7 Days</option>
                  <option value="8">8 Days</option>
                  <option value="10">10 Days</option>
                  <option value="14">14 Days</option>
                </select>
              </div>
            </div>

            {/* Number of Travelers */}
            <div className="form-group">
              <label className="field-label" htmlFor="travelers-select">
                Number of Travelers
              </label>
              <div className="field-input-wrapper">
                <Users size={18} className="field-icon" />
                <select
                  id="travelers-select"
                  className="styled-select-input"
                  value={travelers}
                  onChange={(e) => setTravelers(e.target.value)}
                >
                  <option value="1">1 Traveler</option>
                  <option value="2">2 Travelers</option>
                  <option value="3">3 Travelers</option>
                  <option value="4">4 Travelers</option>
                  <option value="5">5+ Travelers</option>
                </select>
              </div>
            </div>

            {/* Budget (USD) */}
            <div className="form-group">
              <label className="field-label" htmlFor="budget-input">
                Budget (USD)
              </label>
              <div className="field-input-wrapper">
                <DollarSign size={18} className="field-icon" />
                <input
                  id="budget-input"
                  type="number"
                  className="styled-text-input"
                  placeholder="e.g. 120000"
                  value={budget}
                  onChange={(e) => setBudget(e.target.value)}
                  min="500"
                  step="500"
                />
              </div>
            </div>

            {/* Interests */}
            <div className="form-group">
              <label className="field-label" htmlFor="interests-input">
                Interests
              </label>
              <div className="field-input-wrapper">
                <Tag size={18} className="field-icon" />
                <input
                  id="interests-input"
                  type="text"
                  className="styled-text-input"
                  placeholder="e.g. food, anime, nature, history"
                  value={interests}
                  onChange={(e) => setInterests(e.target.value)}
                />
              </div>
            </div>

            {/* Travel Style */}
            <div className="form-group">
              <label className="field-label" htmlFor="style-select">
                Travel Style
              </label>
              <div className="field-input-wrapper">
                <Star size={18} className="field-icon" />
                <select
                  id="style-select"
                  className="styled-select-input"
                  value={travelStyle}
                  onChange={(e) => setTravelStyle(e.target.value)}
                >
                  <option value="Luxury">Luxury</option>
                  <option value="Mid-range">Mid-range</option>
                  <option value="Budget">Budget</option>
                  <option value="Adventure">Adventure</option>
                  <option value="Culture">Culture</option>
                  <option value="Relaxation">Relaxation</option>
                </select>
              </div>
            </div>
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            className="generate-trip-btn"
            disabled={isGenerating}
            id="generate-trip-submit-btn"
          >
            {isGenerating ? (
              <>
                <Loader2 size={20} className="spin-icon" />
                <span>Crafting Itinerary...</span>
              </>
            ) : (
              <>
                <Sparkles size={18} />
                <span>Generate My Trip</span>
              </>
            )}
          </button>
        </form>

        {/* Live Generation Progress Overlay / Box */}
        {isGenerating && (
          <div className="generation-progress-box">
            <div className="gen-step-indicator">
              <Sparkles size={16} className="sparkle-blue" />
              <span>{steps[generationStep]}</span>
            </div>
            <div className="gen-progress-track">
              <div
                className="gen-progress-bar"
                style={{
                  width: `${((generationStep + 1) / steps.length) * 100}%`,
                }}
              />
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default CreateTripView;
