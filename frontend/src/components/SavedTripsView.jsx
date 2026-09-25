import {
  Bookmark,
  Calendar,
  Users,
  DollarSign,
  ArrowRight,
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
                {trip.image ? (
                  <img
                    src={trip.image}
                    alt={trip.destination}
                    className="trip-thumbnail-img"
                    loading="lazy"
                  />
                ) : (
                  <div
                    style={{
                      width: '100%',
                      height: '100%',
                      background:
                        'linear-gradient(135deg, #0B1F33 0%, #0E7490 100%)',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      color: '#ffffff',
                    }}
                  >
                    <Bookmark size={24} />
                  </div>
                )}
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
                  {trip.status && (
                    <span
                      style={{
                        padding: '0.2rem 0.5rem',
                        borderRadius: '6px',
                        fontSize: '0.75rem',
                        fontWeight: 600,
                        textTransform: 'capitalize',
                        backgroundColor:
                          trip.status === 'completed'
                            ? '#DCFCE7'
                            : trip.status === 'pending'
                            ? '#FEF3C7'
                            : '#FEE2E2',
                        color:
                          trip.status === 'completed'
                            ? '#166534'
                            : trip.status === 'pending'
                            ? '#92400E'
                            : '#991B1B',
                      }}
                    >
                      {trip.status}
                    </span>
                  )}
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
