import { AlertCircle } from 'lucide-react';
import './ErrorCard.css'; // optional styling, will use existing classes

const ErrorCard = ({ error, onRetry }) => (
  <div className="trip-loading-box" style={{ backgroundColor: '#FFF5F5', borderColor: '#FCA5A5' }}>
    <AlertCircle className="airplane-spinner" size={48} color="#EF4444" />
    <p>{error}</p>
    <button onClick={onRetry} className="plan-btn" style={{ marginTop: '1rem', backgroundColor: '#EF4444' }}>
      Try Again
    </button>
  </div>
);

export default ErrorCard;
