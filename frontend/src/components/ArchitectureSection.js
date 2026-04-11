import React from 'react';
import '../styles/ArchitectureSection.css';

function ArchitectureSection() {
  return (
    <section id="architecture" className="architecture">
      <div className="architecture-container">
        <h2>Architecture</h2>
        <p className="section-subtitle">Combined Machine Learning Architecture for Predicting Electrochemical Performance of Supercapacitor Materials</p>
        
        <div className="architecture-diagram">
          <img src="/images/system-architecture.png" alt="Machine Learning Architecture Diagram" className="diagram-image" />
        </div>
      </div>
    </section>
  );
}

export default ArchitectureSection;