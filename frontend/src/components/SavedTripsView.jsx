import React from 'react';
import {
  Bookmark,
  Calendar,
  Users,
  DollarSign,
  ArrowRight,
  PlusCircle,
} from 'lucide-react';

const SavedTripsView = ({ trips, onSelectTrip, onNewTrip }) => {
  return (
    <div className="saved-trips-page-container">
      {/* Page Title & Subtitle */}
      <div className="saved-page-header">
        <div className="saved-title-row">
          <Bookmark size={24} className="saved-bookmark-icon" />
          <h1 className="saved-page-title">Saved Trips</h1>
        </div>
        <p className="saved-page-subtitle">
          Your past travel plans, all in one place.
        </p>
      </div>

      {/* Trips list */}
      <div className="trips-cards-list">
        {trips && trips.length > 0 ? (
          trips.map((trip) => (
            <div className="trip-item-card" key={trip.id}>
              {/* Left thumbnail image */}
              <div className="trip-thumb-wrapper">
                <img
                  src={trip.image}
                  alt={trip.destination}
                  className="trip-thumbnail-img"
                  loading="lazy"
                />
              </div>

              {/* Middle details */}
              <div className="trip-card-details">
                <h3 className="trip-destination-name">{trip.destination}</h3>

                {/* Meta details row */}
                <div className="trip-meta-row">
                  <span className="trip-meta-item">
                    <Calendar size={15} className="meta-icon" />
                    <span>{trip.days} days</span>
                  </span>
                  <span className="trip-meta-item">
                    <Users size={15} className="meta-icon" />
                    <span>{trip.travelers} travelers</span>
                  </span>
                  <span className="trip-meta-item">
                    <DollarSign size={15} className="meta-icon" />
                    <span>
                      {trip.formattedBudget ||
                        `$ ${Number(trip.budget).toLocaleString()}`}
                    </span>
                  </span>
                </div>

                {/* Tags row */}
                <div className="trip-tags-row">
                  {trip.tags &&
                    trip.tags.map((tag, idx) => (
                      <span className="trip-tag-pill" key={idx}>
                        {tag}
                      </span>
                    ))}
                </div>

                {/* Created timestamp */}
                <div className="trip-created-date">
                  Created on {trip.createdAt || 'Sep 18, 2026'}
                </div>
              </div>

              {/* Right CTA button */}
              <div className="trip-card-action">
                <button
                  className="view-details-btn"
                  onClick={() => onSelectTrip(trip)}
                  id={`view-details-${trip.id}`}
                >
                  <span>View Details</span>
                  <ArrowRight size={15} />
                </button>
              </div>
            </div>
          ))
        ) : (
          <div className="empty-trips-card">
            <p>No saved trips found.</p>
            <button className="create-trip-pill-btn" onClick={onNewTrip}>
              Create Your First Trip
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default SavedTripsView;
