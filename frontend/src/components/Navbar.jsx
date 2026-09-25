import React from 'react';
import { Plane } from 'lucide-react';

const Navbar = ({ currentView, setView }) => {
  return (
    <header className="site-header">
      <div className="header-container">
        {/* Brand / Logo */}
        <button
          className="brand-link"
          onClick={() => setView('home')}
          aria-label="Go to Home"
        >
          <div className="brand-plane-icon">
            <Plane size={22} className="plane-svg" />
          </div>
          <span className="brand-title">AI Travel Planner</span>
        </button>

        {/* Navigation items on right */}
        <nav className="header-nav">
          <button
            className={`nav-text-btn ${currentView === 'home' ? 'active' : ''}`}
            onClick={() => setView('home')}
          >
            Home
          </button>

          <button
            className={`nav-text-btn ${currentView === 'saved' ? 'active' : ''}`}
            onClick={() => setView('saved')}
          >
            Saved Trips
          </button>

          {currentView === 'home' ? (
            <button
              className="create-trip-pill-btn"
              onClick={() => setView('create')}
            >
              Create Trip
            </button>
          ) : (
            <div
              className="user-avatar-badge"
              title="Profile"
              onClick={() => setView('saved')}
            >
              <img
                src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=150&q=80"
                alt="User Profile Avatar"
                className="user-avatar-img"
              />
            </div>
          )}
        </nav>
      </div>
    </header>
  );
};

export default Navbar;
