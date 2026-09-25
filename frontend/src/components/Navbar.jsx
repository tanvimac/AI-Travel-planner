import React, { useState } from 'react';
import { Navigation, Sparkles, Menu, X } from 'lucide-react';

const Navbar = () => {
  const [mobileOpen, setMobileOpen] = useState(false);
  const toggleMenu = () => setMobileOpen(!mobileOpen);

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <a href="#" className="brand-logo">
          <div className="brand-icon-box">
            <Navigation size={20} />
          </div>
          <span>Wanderlust AI</span>
        </a>
        <div className="nav-links desktop-only">
          <a href="#" className="nav-link">Plan a Trip</a>
          <a href="#" className="nav-link">My Trips</a>
          <a href="#" className="nav-link">About</a>
        </div>
        <div className="nav-right desktop-only">
          <div className="nav-badge">
            <Sparkles size={14} /> AI-Powered
          </div>
          <button className="cta-btn">Explore Now</button>
        </div>
        <button className="mobile-menu-btn mobile-only" onClick={toggleMenu} aria-label="Toggle navigation">
          {mobileOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </div>
      {mobileOpen && (
        <div className="mobile-menu">
          <a href="#" className="nav-link" onClick={toggleMenu}>Plan a Trip</a>
          <a href="#" className="nav-link" onClick={toggleMenu}>My Trips</a>
          <a href="#" className="nav-link" onClick={toggleMenu}>About</a>
          <div className="nav-badge mobile-only">
            <Sparkles size={14} /> AI-Powered
          </div>
          <button className="cta-btn mobile-only">Explore Now</button>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
