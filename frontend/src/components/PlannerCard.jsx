import React from 'react';
import { MapPin, Calendar, Users, Wallet, Sparkles, Compass, Navigation, ArrowRight, Loader2 } from 'lucide-react';
import NumberInput from './NumberInput';
import TravelStyleSelector from './TravelStyleSelector';
import '../index.css';

function PlannerCard({
  destination,
  setDestination,
  days,
  setDays,
  travelers,
  setTravelers,
  budget,
  setBudget,
  travelStyle,
  setTravelStyle,
  interests,
  setInterests,
  travelStyles,
  handleStyleSelect,
  handleSubmit,
  isLoading,
}) {
  return (
    <section className="search-widget-card">
      <div className="widget-header">
        <div className="widget-title-group">
          <Compass size={24} className="widget-icon" />
          <div>
            <h2 className="widget-title">Where do you want to go?</h2>
            <p className="widget-subtitle">Enter your trip details to generate your itinerary</p>
          </div>
        </div>
      </div>
      <form onSubmit={handleSubmit} className="travel-form">
        <div className="form-row">
          {/* Destination */}
          <div className="field-group full-width">
            <label className="field-label" htmlFor="destination-field">
              <MapPin className="field-label-icon" /> Destination
            </label>
            <div className="input-container">
              <MapPin className="input-icon" size={20} />
              <input
                id="destination-field"
                className="travel-input"
                type="text"
                placeholder="e.g. Paris, Tokyo, Bali, Switzerland"
                value={destination}
                onChange={(e) => setDestination(e.target.value)}
                required
              />
            </div>
          </div>
          {/* Days */}
          <NumberInput
            id="days-field"
            label="Duration (Days)"
            value={days}
            setValue={setDays}
            min={1}
            icon={Calendar}
          />
          {/* Travelers */}
          <NumberInput
            id="travelers-field"
            label="Travelers"
            value={travelers}
            setValue={setTravelers}
            min={1}
            icon={Users}
          />
          {/* Budget */}
          <div className="field-group">
            <label className="field-label" htmlFor="budget-field">
              <Wallet className="field-label-icon" /> Budget (₹)
            </label>
            <div className="input-container">
              <Wallet className="input-icon" size={20} />
              <input
                id="budget-field"
                className="travel-input"
                type="number"
                min="0"
                placeholder="e.g. 50000"
                value={budget}
                onChange={(e) => setBudget(e.target.value)}
                required
              />
            </div>
          </div>
          {/* Travel Style */}
          <div className="field-group">
            <label className="field-label" htmlFor="travel-style-field">
              <Sparkles className="field-label-icon" /> Travel Style
            </label>
            <div className="input-container">
              <Sparkles className="input-icon" size={20} />
              <select
                id="travel-style-field"
                className="travel-input travel-select"
                value={travelStyle}
                onChange={(e) => setTravelStyle(e.target.value)}
              >
                <option value="Budget">Budget</option>
                <option value="Mid-range">Mid-range</option>
                <option value="Luxury">Luxury</option>
              </select>
            </div>
          </div>
        </div>
        {/* Travel Style & Interests chips */}
        <div className="travel-style-section">
          <label className="field-label" htmlFor="interests-field">
            <Compass className="field-label-icon" /> Travel Style &amp; Interests
          </label>
          <TravelStyleSelector
            travelStyles={travelStyles}
            interests={interests}
            handleStyleSelect={handleStyleSelect}
          />
          <div className="input-container" style={{ marginTop: '0.5rem' }}>
            <Compass className="input-icon" size={20} />
            <input
              id="interests-field"
              className="travel-input"
              type="text"
              placeholder="e.g. food, beaches, culture, adventure"
              value={interests}
              onChange={(e) => setInterests(e.target.value)}
            />
          </div>
        </div>
        <button type="submit" className="plan-btn" disabled={isLoading}>
          {isLoading ? (
            <>
              <Loader2 className="spinner" size={22} />
              <span>Creating Your Journey...</span>
            </>
          ) : (
            <>
              <Navigation size={20} />
              <span>✨ Create My Trip</span>
              <ArrowRight className="btn-arrow-icon" size={18} />
            </>
          )}
        </button>
      </form>
    </section>
  );
}

export default PlannerCard;
