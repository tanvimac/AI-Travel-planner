import { MapPin, Globe, Hotel, Coffee, BarChart, Clipboard } from 'lucide-react';
import '../index.css';

function AgentsSection() {
  const agents = [
    { icon: MapPin, name: 'Destination Agent', desc: 'Finds perfect spots' },
    { icon: Hotel, name: 'Stay Scout', desc: 'Curates accommodations' },
    { icon: Coffee, name: 'Food Explorer', desc: 'Recommends local cuisine' },
    { icon: Globe, name: 'Experience Planner', desc: 'Plans activities & tours' },
    { icon: BarChart, name: 'Budget Analyst', desc: 'Optimizes cost' },
    { icon: Clipboard, name: 'Itinerary Architect', desc: 'Creates day‑by‑day plan' },
  ];

  return (
    <section className="agents-section" style={{ marginTop: '3rem' }}>
      <h2 style={{ color: 'var(--navy-deep)', fontSize: '2rem', textAlign: 'center', marginBottom: '1.5rem' }}>
        Meet Your AI Travel Team
      </h2>
      <div className="agents-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1.5rem' }}>
        {agents.map((agent) => (
          <div key={agent.name} className="agent-card" style={{ backgroundColor: 'var(--card-bg)', padding: '1.5rem', borderRadius: 'var(--radius-md)', boxShadow: 'var(--shadow-subtle)', textAlign: 'center', transition: 'transform 0.2s, box-shadow 0.2s' }}>
            <agent.icon size={36} color="var(--sunset-orange)" />
            <h3 style={{ marginTop: '0.75rem', fontSize: '1.1rem', color: 'var(--navy-deep)' }}>{agent.name}</h3>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>{agent.desc}</p>
          </div>
        ))}
      </div>
    </section>
  );
}

export default AgentsSection;
