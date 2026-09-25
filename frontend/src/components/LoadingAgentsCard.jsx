import React from 'react';
import { Loader2 } from 'lucide-react';
import './../App.css';

const LoadingAgentsCard = () => (
  <div className="trip-loading-box">
    <Loader2 className="airplane-spinner" size={48} />
    <p>Our AI travel agents are crafting your perfect itinerary…</p>
  </div>
);

export default LoadingAgentsCard;
