
const HowItWorks = () => (
  <section className="how-it-works" style={{ padding: '2rem', backgroundColor: 'var(--cream)' }}>
    <h2 style={{ fontSize: '2rem', marginBottom: '1rem', color: 'var(--navy)' }}>
      How It Works
    </h2>
    <ol style={{ listStyle: 'decimal inside', lineHeight: '1.6', color: 'var(--navy)' }}>
      <li>Enter your travel preferences in the form above.</li>
      <li>Click “Plan My Trip” to send a request to the AI agents.</li>
      <li>The AI agents collaborate to generate a personalized itinerary.</li>
      <li>Watch the loading animation while the agents work.</li>
      <li>When ready, view the detailed trip summary and itinerary.</li>
    </ol>
  </section>
);

export default HowItWorks;
