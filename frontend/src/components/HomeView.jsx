import { ArrowRight, Sparkles, Map, Heart, Zap } from 'lucide-react';
import heroFuji from '../assets/hero_fuji.jpg';

const HomeView = ({ onStartPlanning }) => {
  return (
    <div className="home-view-container">
      {/* Hero Banner Card */}
      <section
        className="hero-banner-card"
        style={{ backgroundImage: `url(${heroFuji})` }}
      >
        <div className="hero-content-overlay">
          <span className="hero-eyebrow">YOUR AI-POWERED TRAVEL COMPANION</span>
          <h1 className="hero-headline">Dream. Plan. Explore.</h1>
          <p className="hero-description">
            Tell us where you want to go, and our AI will create a personalized
            travel plan just for you.
          </p>
          <button
            className="hero-cta-btn"
            onClick={onStartPlanning}
            id="hero-create-trip-btn"
          >
            <span>Create Your Trip</span>
            <ArrowRight size={18} />
          </button>
        </div>
      </section>

      {/* 4 Feature Columns Row */}
      <section className="features-columns-row">
        <div className="feature-item-col">
          <div className="feature-icon-wrapper">
            <Sparkles size={24} className="feature-svg-icon" />
          </div>
          <h3 className="feature-item-title">Personalized Itineraries</h3>
          <p className="feature-item-desc">
            Tailored to your interests, style and budget
          </p>
        </div>

        <div className="feature-item-col">
          <div className="feature-icon-wrapper">
            <Map size={24} className="feature-svg-icon" />
          </div>
          <h3 className="feature-item-title">Discover Amazing Places</h3>
          <p className="feature-item-desc">
            From hidden gems to must-see attractions
          </p>
        </div>

        <div className="feature-item-col">
          <div className="feature-icon-wrapper">
            <Heart size={24} className="feature-svg-icon" />
          </div>
          <h3 className="feature-item-title">Your Travel Style</h3>
          <p className="feature-item-desc">
            Adventure, Luxury, Budget — you choose
          </p>
        </div>

        <div className="feature-item-col">
          <div className="feature-icon-wrapper">
            <Zap size={24} className="feature-svg-icon" />
          </div>
          <h3 className="feature-item-title">Powered by AI</h3>
          <p className="feature-item-desc">
            Smart planning for unforgettable trips
          </p>
        </div>
      </section>
    </div>
  );
};

export default HomeView;
