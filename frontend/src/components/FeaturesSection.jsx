import React from 'react';
import { Star, Tag, Clock } from 'lucide-react';

const FeaturesSection = () => (
  <section className="features-section" style={{ marginTop: '3rem' }}>
    <h2 style={{ color: 'var(--navy-deep)', fontSize: '2rem', textAlign: 'center', marginBottom: '2rem' }}>
      Why Choose Wanderlust AI?
    </h2>
    <div className="features-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1.5rem' }}>
      <div className="feature-card" style={{ backgroundColor: 'var(--card-bg)', padding: '1.5rem', borderRadius: 'var(--radius-md)', boxShadow: 'var(--shadow-subtle)', textAlign: 'center' }}>
        <Star size={36} color="var(--sunset-orange)" />
        <h3 style={{ marginTop: '0.75rem', fontSize: '1.2rem', color: 'var(--navy-deep)' }}>Personalized Itineraries</h3>
        <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>AI tailors each day to your style, budget, and interests.</p>
      </div>
      <div className="feature-card" style={{ backgroundColor: 'var(--card-bg)', padding: '1.5rem', borderRadius: 'var(--radius-md)', boxShadow: 'var(--shadow-subtle)', textAlign: 'center' }}>
        <Tag size={36} color="var(--sunset-orange)" />
        <h3 style={{ marginTop: '0.75rem', fontSize: '1.2rem', color: 'var(--navy-deep)' }}>Smart Budgeting</h3>
        <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>Optimizes costs while keeping experiences premium.</p>
      </div>
      <div className="feature-card" style={{ backgroundColor: 'var(--card-bg)', padding: '1.5rem', borderRadius: 'var(--radius-md)', boxShadow: 'var(--shadow-subtle)', textAlign: 'center' }}>
        <Clock size={36} color="var(--sunset-orange)" />
        <h3 style={{ marginTop: '0.75rem', fontSize: '1.2rem', color: 'var(--navy-deep)' }}>Instant Planning</h3>
        <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>Get a full itinerary in seconds, not hours.</p>
      </div>
    </div>
  </section>
);

export default FeaturesSection;
