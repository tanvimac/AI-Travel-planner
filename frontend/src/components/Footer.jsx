import React from 'react';

const Footer = () => (
  <footer className="travel-footer">
    <p>© 2024 Wanderlust AI. All rights reserved.</p>
    <div style={{ marginTop: '0.5rem', display: 'flex', justifyContent: 'center', gap: '1rem' }}>
      <a href="https://github.com" target="_blank" rel="noopener noreferrer" aria-label="GitHub">GitHub</a>
      <a href="https://linkedin.com" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn">LinkedIn</a>
      <a href="https://twitter.com" target="_blank" rel="noopener noreferrer" aria-label="Twitter">Twitter</a>
    </div>
  </footer>
);

export default Footer;
