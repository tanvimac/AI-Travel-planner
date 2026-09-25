import React from 'react';
import { MapPin, Calendar, Users, Wallet, Sparkles, Compass, Navigation } from 'lucide-react';

const TripSummaryCard = ({ data }) => (
  <div className="trip-ticket-card">
    <div className="ticket-header">
      <div className="ticket-header-left">
        <div className="ticket-plane-badge">
          <Navigation size={20} />
        </div>
        <div>
          <h3 className="ticket-title">Your Trip is Being Prepared ✈️</h3>
        </div>
      </div>
      <span className="ticket-tag">{data.status}</span>
    </div>
    <div className="ticket-body">
      <div className="ticket-details-grid">
        <div className="ticket-detail-item">
          <div className="detail-icon-box"><MapPin size={22} /></div>
          <div className="detail-content">
            <span className="detail-label">Destination</span>
            <span className="detail-val detail-val-highlight">{data.destination}</span>
          </div>
        </div>
        <div className="ticket-detail-item">
          <div className="detail-icon-box"><Calendar size={22} /></div>
          <div className="detail-content">
            <span className="detail-label">Duration</span>
            <span className="detail-val">{data.days} {data.days === 1 ? 'Day' : 'Days'}</span>
          </div>
        </div>
        <div className="ticket-detail-item">
          <div className="detail-icon-box"><Users size={22} /></div>
          <div className="detail-content">
            <span className="detail-label">Travelers</span>
            <span className="detail-val">{data.travelers} {data.travelers === 1 ? 'Person' : 'People'}</span>
          </div>
        </div>
        <div className="ticket-detail-item">
          <div className="detail-icon-box"><Wallet size={22} /></div>
          <div className="detail-content">
            <span className="detail-label">Estimated Budget</span>
            <span className="detail-val">₹{Number(data.budget).toLocaleString('en-IN')}</span>
          </div>
        </div>
        {data.travelStyle && (
          <div className="ticket-detail-item">
            <div className="detail-icon-box"><Sparkles size={22} /></div>
            <div className="detail-content">
              <span className="detail-label">Travel Style</span>
              <span className="detail-val">{data.travelStyle}</span>
            </div>
          </div>
        )}
        {data.interests && (
          <div className="ticket-detail-item" style={{ width: '100%' }}>
            <div className="detail-icon-box"><Compass size={22} /></div>
            <div className="detail-content" style={{ width: '100%' }}>
              <span className="detail-label">Travel Style & Interests</span>
              <div className="ticket-interests-tags">
                {data.interests.split(',').map((t, i) => (
                  <span key={i} className="interest-tag-item">{t.trim()}</span>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  </div>
);

export default TripSummaryCard;
