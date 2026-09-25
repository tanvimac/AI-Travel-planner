import '../index.css';

function TravelStyleSelector({ travelStyles, interests, handleStyleSelect }) {
  return (
    <div className="style-chips-container">
      {travelStyles.map((style) => {
        const isSelected = interests.toLowerCase().includes(style.label.toLowerCase());
        return (
          <button
            key={style.label}
            type="button"
            className={`style-chip-btn ${isSelected ? 'active' : ''}`}
            onClick={() => handleStyleSelect(style.label)}
          >
            <span>{style.icon}</span>
            <span>{style.label}</span>
          </button>
        );
      })}
    </div>
  );
}

export default TravelStyleSelector;
