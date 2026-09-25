import React from 'react';
import { Globe } from 'lucide-react';

const Hero = () => (
  <section className="travel-hero" style={{ backgroundImage: 'url(/src/assets/hero.jpg)', backgroundSize: 'cover', backgroundPosition: 'center' }}>
    <div className="hero-content">
      <div className="hero-pill-tag">
        <Globe size={14} /> ✦ Multi-Agent AI Travel Planner
      </div>
      <h1 className="hero-title">
        Your Next Adventure,<br />
        <span className="title-highlight">Planned by AI.</span>
      </h1>
      <p className="hero-subtitle">
        Tell us where you want to go, what you love, and your budget. Our AI travel planner creates a personalized journey for you.
      </p>
      <div className="agent-indicators" style={{ marginTop: '1rem', display: 'flex', gap: '0.5rem', flexWrap: 'wrap', justifyContent: 'center', color: 'var(--color-accent)' }}>
        <span>Destination AI</span>
        <span>Hotel AI</span>
        <span>Food AI</span>
        <span>Activity AI</span>
        <span>Budget AI</span>
        <span>Itinerary AI</span>
      </div>
    </div>
  </section>
);

export default Hero;
