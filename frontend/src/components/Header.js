import React from 'react';
import '../styles/Header.css';

function Header() {
  return (
    <header className="header">
      <div className="header-container">
        <div className="logo">
          <h1>🔬 CV Prediction</h1>
          <p>ZN/CO Substituted BiFe<sub>2</sub>O<sub>3</sub></p>
        </div>
        <nav className="navbar">
          <ul>
            <li><a href="#overview">Overview</a></li>
            <li><a href="#architecture">Architecture</a></li>
            <li><a href="#models">Models</a></li>
            <li><a href="#performance">Performance</a></li>
            <li><a href="#predict" className="live-badge">🔴 Live</a></li>
          </ul>
        </nav>
      </div>
    </header>
  );
}

export default Header;