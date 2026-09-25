import {
  ArrowLeft,
  Calendar,
  Users,
  DollarSign,
  Bookmark,
  Check,
  Lightbulb,
} from 'lucide-react';

const TripDetailsView = ({ trip, onBack }) => {
  if (!trip) return null;

  return (
    <div className="trip-details-page-container">
      {/* Back button */}
      <button
        className="back-nav-link-btn"
        onClick={onBack}
        aria-label="Back to Saved Trips"
      >
        <ArrowLeft size={16} />
        <span>Back to Saved Trips</span>
      </button>

      {/* Hero Summary Card */}
      <div className="trip-hero-split-card">
        <div className="hero-split-image-box">
          {trip.image ? (
            <img
              src={trip.image}
              alt={trip.destination}
              className="hero-split-img"
            />
          ) : (
            <div
              style={{
                width: '100%',
                height: '100%',
                minHeight: '220px',
                background:
                  'linear-gradient(135deg, #0B1F33 0%, #0E7490 100%)',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                color: '#ffffff',
                padding: '2rem',
                textAlign: 'center',
              }}
            >
              <Bookmark size={36} style={{ marginBottom: '0.5rem', opacity: 0.9 }} />
              <span style={{ fontSize: '1.2rem', fontWeight: 600 }}>
                {trip.destination}
              </span>
              <span
                style={{
                  fontSize: '0.85rem',
                  opacity: 0.8,
                  marginTop: '0.25rem',
                }}
              >
                AI Generated Itinerary
              </span>
            </div>
          )}
        </div>

        <div className="hero-split-info-box">
          <h1 className="hero-destination-title">{trip.destination}</h1>

          {/* Meta row */}
          <div className="trip-meta-row">
            <span className="trip-meta-item">
              <Calendar size={16} className="meta-icon" />
              <span>{trip.days} days</span>
            </span>
            <span className="trip-meta-item">
              <Users size={16} className="meta-icon" />
              <span>{trip.travelers} travelers</span>
            </span>
            <span className="trip-meta-item">
              <DollarSign size={16} className="meta-icon" />
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

          {/* Description */}
          <p className="hero-split-description">{trip.description}</p>

          {/* Created date */}
          <div className="trip-created-date">
            Created on {trip.createdAt || 'Sep 18, 2026'}
          </div>
        </div>
      </div>

      {/* Main 2-column layout: Itinerary timeline on left, Highlights & Tips on right */}
      <div className="itinerary-grid-layout">
        {/* Left Column: Itinerary Timeline */}
        <div className="itinerary-timeline-column">
          <div className="itinerary-column-header">
            <Bookmark size={20} className="itinerary-header-icon" />
            <h2 className="itinerary-column-title">
              Your {trip.days}-Day Itinerary
            </h2>
          </div>

          <div className="timeline-container">
            {trip.itinerary && trip.itinerary.length > 0 ? (
              trip.itinerary.map((item) => (
                <div className="timeline-row-item" key={item.day}>
                  {/* Timeline node */}
                  <div className="timeline-left-node">
                    <div className="timeline-day-badge">Day {item.day}</div>
                    <div className="timeline-stem-line" />
                  </div>

                  {/* Day Content Card */}
                  <div className="timeline-card-box">
                    <div className="timeline-card-text">
                      <h4 className="timeline-day-title">{item.title}</h4>
                      <ul className="timeline-bullets-list">
                        {item.bullets &&
                          item.bullets.map((bullet, bIdx) => (
                            <li key={bIdx} className="timeline-bullet-item">
                              <span className="bullet-dot">•</span>
                              <span>{bullet.replace(/^[•\s-]+/, '')}</span>
                            </li>
                          ))}
                      </ul>
                    </div>

                    {item.image && (
                      <div className="timeline-card-image-box">
                        <img
                          src={item.image}
                          alt={item.title}
                          className="timeline-day-thumb"
                          loading="lazy"
                        />
                      </div>
                    )}
                  </div>
                </div>
              ))
            ) : (
              <p className="no-itinerary-note">
                No detailed itinerary schedule found.
              </p>
            )}
          </div>
        </div>

        {/* Right Column: Highlights & Travel Tips */}
        <div className="itinerary-sidebar-column">
          {/* Highlights Card */}
          <div className="sidebar-card trip-highlights-card">
            <div className="sidebar-card-header">
              <Bookmark size={18} className="sidebar-header-blue-icon" />
              <h3 className="sidebar-card-title">Trip Highlights</h3>
            </div>
            <ul className="highlights-list">
              {trip.highlights && trip.highlights.length > 0 ? (
                trip.highlights.map((highlight, hIdx) => (
                  <li key={hIdx} className="highlight-item">
                    <Check size={16} className="check-icon" />
                    <span>{highlight}</span>
                  </li>
                ))
              ) : (
                <>
                  <li className="highlight-item">
                    <Check size={16} className="check-icon" />
                    <span>Tailored for {trip.travelers} traveler(s)</span>
                  </li>
                  <li className="highlight-item">
                    <Check size={16} className="check-icon" />
                    <span>{trip.travelStyle} travel style curation</span>
                  </li>
                  <li className="highlight-item">
                    <Check size={16} className="check-icon" />
                    <span>Personalized daily schedule for {trip.destination}</span>
                  </li>
                </>
              )}
            </ul>
          </div>

          {/* Travel Tips Card */}
          <div className="sidebar-card travel-tips-card">
            <div className="sidebar-card-header">
              <Lightbulb size={18} className="sidebar-header-yellow-icon" />
              <h3 className="sidebar-card-title">Travel Details</h3>
            </div>
            <ul className="tips-list">
              {trip.travelTips && trip.travelTips.length > 0 ? (
                trip.travelTips.map((tip, tIdx) => (
                  <li key={tIdx} className="tip-item">
                    <span className="tip-bullet">•</span>
                    <span>{tip}</span>
                  </li>
                ))
              ) : (
                <>
                  <li className="tip-item">
                    <span className="tip-bullet">•</span>
                    <span>Duration: {trip.days} days</span>
                  </li>
                  <li className="tip-item">
                    <span className="tip-bullet">•</span>
                    <span>
                      Estimated Budget:{' '}
                      {trip.formattedBudget ||
                        `$ ${Number(trip.budget).toLocaleString()}`}
                    </span>
                  </li>
                  <li className="tip-item">
                    <span className="tip-bullet">•</span>
                    <span>Status: {trip.status || 'Active'}</span>
                  </li>
                </>
              )}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TripDetailsView;
