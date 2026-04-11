import React from 'react';
import '../styles/OverviewSection.css';

function OverviewSection() {
  return (
    <section id="overview" className="overview">
      <div className="overview-container">
        <h2>Overview</h2>
        <div className="overview-content">
          <p>
            This advanced machine learning model predicts cyclic voltammetry (CV) behavior for ZN/CO substituted BiFe<sub>0</sub>O₃ materials 
            using state-of-the-art deep learning algorithms including XGBoost, TensorFlow, and Random Forest.
          </p>
          <p>
            The model integrates multiple neural network architectures to predict electrochemical properties with high accuracy, 
            supporting materials science research and accelerating the discovery of novel catalytic materials.
          </p>
          <div className="overview-highlights">
            <div className="highlight">
              <h4>🎯 Multi-Model Ensemble</h4>
              <p>Combines XGBoost, TensorFlow Neural Networks, and Random Forest</p>
            </div>
            <div className="highlight">
              <h4>📊 High Accuracy</h4>
              <p>85%+ average accuracy across all models</p>
            </div>
            <div className="highlight">
              <h4>⚡ Fast Predictions</h4>
              <p>Real-time cyclic voltammetry behavior analysis</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default OverviewSection;