import React from 'react';
import '../styles/HeroSection.css';

function HeroSection() {
  return (
    <section className="hero">
      <div className="hero-content">
        <h1>ML-Based CV Behavior Prediction</h1>
        <p className="subtitle">Advanced Machine Learning for Materials Science Analysis</p>
        <p className="updated">Updated: April 11, 2026 • Cyclic Voltammetry Analysis • Deep Learning Integration</p>
        <button className="cta-button">Explore Model →</button>
      </div>
    </section>
  );
}

export default HeroSection;