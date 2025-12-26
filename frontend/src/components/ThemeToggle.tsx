import React from 'react';
import './ThemeToggle.css';

interface ThemeToggleProps {
  onToggle: () => void;
  isDarkMode: boolean;
}

const ThemeToggle: React.FC<ThemeToggleProps> = ({ onToggle, isDarkMode }) => {
  return (
    <label className="switch">
      <input
        type="checkbox"
        className="input__check"
        checked={isDarkMode}
        onChange={onToggle}
      />
      <span className="slider"></span>
    </label>
  );
};

export default ThemeToggle;
