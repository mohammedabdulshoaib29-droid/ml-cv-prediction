import React from 'react';
import '../styles/ComponentsSection.css';

function ComponentsSection() {
  const components = [
    {
      title: "Artificial Neural Network (ANN)",
      description: "Deep learning model with multi-layer neural architecture",
      features: [
        "Learns complex non-linear patterns",
        "Multi-hidden layer architecture (128→64→1)",
        "ReLU activation with BatchNormalization"
      ]
    },
    {
      title: "Random Forest (RF)",
      description: "Ensemble of decision trees with voting mechanism",
      features: [
        "Reduced overfitting through ensemble voting",
        "Feature importance extraction",
        "Parallel processing capability"
      ]
    },
    {
      title: "XGBoost (Extreme Gradient Boosting)",
      description: "Sequential boosting with gradient optimization",
      features: [
        "Handles non-linear relationships",
        "Feature importance extraction",
        "Robust to outliers and noise"
      ]
    },
    {
      title: "Data Preprocessing & Evaluation",
      description: "Feature normalization and model evaluation metrics",
      features: [
        "StandardScaler normalization",
        "Accuracy, Precision, Recall",
        "Cross-validation support"
      ]
    }
  ];

  return (
    <section id="models" className="components">
      <div className="components-container">
        <h2>Network Components</h2>
        <p className="section-subtitle">Three Powerful ML Models Working Together</p>
        
        <div className="components-grid">
          {components.map((comp, idx) => (
            <div key={idx} className="component-card">
              <div className="card-number">{idx + 1}</div>
              <h3>{comp.title}</h3>
              <p className="card-description">{comp.description}</p>
              <div className="features">
                <h4>Key Features:</h4>
                <ul>
                  {comp.features.map((feat, i) => (
                    <li key={i}>✓ {feat}</li>
                  ))}
                </ul>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

export default ComponentsSection;