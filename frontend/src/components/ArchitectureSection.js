import React from 'react';
import '../styles/ArchitectureSection.css';

function ArchitectureSection() {
  return (
    <section id="architecture" className="architecture">
      <div className="architecture-container">
        <h2>Architecture</h2>
        <p className="section-subtitle">Multi-Model Ensemble Architecture for CV Prediction</p>
        
        <div className="architecture-diagram">
          <div className="diagram-box">
            <h3>📊 Input Data</h3>
            <p>CV Dataset Files</p>
            <p>(Excel, CSV)</p>
          </div>
          
          <div className="arrow">→</div>
          
          <div className="diagram-box">
            <h3>🔄 Preprocessing</h3>
            <p>Feature Extraction</p>
            <p>Normalization</p>
          </div>
          
          <div className="arrow">→</div>
          
          <div className="diagram-box">
            <h3>🤖 Model Ensemble</h3>
            <p>XGBoost</p>
            <p>TensorFlow</p>
            <p>Random Forest</p>
          </div>
          
          <div className="arrow">→</div>
          
          <div className="diagram-box">
            <h3>📈 Output</h3>
            <p>Predictions & Analysis</p>
            <p>Model Comparison</p>
          </div>
        </div>
      </div>
    </section>
  );
}

export default ArchitectureSection;