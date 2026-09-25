
const ItineraryPlaceholder = () => (
  <div className="trip-ticket-card">
    <div className="ticket-header">
      <div className="ticket-header-left">
        <div className="ticket-plane-badge">
          <span role="img" aria-label="hourglass">⏳</span>
        </div>
        <div>
          <h3 className="ticket-title">Your itinerary is on its way!</h3>
        </div>
      </div>
      <span className="ticket-tag">pending</span>
    </div>
    <div className="ticket-body">
      <p className="ticket-alert-msg">
        We are still processing your request. Please stay tuned – the AI agents are busy crafting your perfect trip.
      </p>
    </div>
  </div>
);

export default ItineraryPlaceholder;
