import { Minus, Plus } from 'lucide-react';
import '../index.css';

function NumberInput({ id, label, value, setValue, min = 1, icon: Icon }) {
  const decrement = () => {
    const newVal = Math.max(min, Number(value) - 1);
    setValue(newVal);
  };
  const increment = () => {
    setValue(Number(value) + 1);
  };

  return (
    <div className="field-group">
      <label className="field-label" htmlFor={id}>
        {Icon && <Icon className="field-label-icon" />} {label}
      </label>
      <div className="input-container number-input">
        <button type="button" className="num-btn decrement" onClick={decrement} aria-label="Decrease {label}">
          <Minus size={16} />
        </button>
        <input
          id={id}
          className="travel-input number-field"
          type="number"
          min={min}
          value={value}
          readOnly
        />
        <button type="button" className="num-btn increment" onClick={increment} aria-label="Increase {label}">
          <Plus size={16} />
        </button>
      </div>
    </div>
  );
}

export default NumberInput;
