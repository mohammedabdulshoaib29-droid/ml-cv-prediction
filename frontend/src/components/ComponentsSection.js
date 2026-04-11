import React from 'react';
import '../styles/ComponentsSection.css';

function ComponentsSection() {
  const components = [
    {
      title: "XGBoost Gradient Boosting",
      description: "Ensemble method that sequentially builds decision trees",
      features: [
        "Handles non-linear relationships",
        "Feature importance extraction",
        "Robust to outliers"
      ]
    },
    {
      title: "TensorFlow Neural Network",
      description: "Deep learning model with multiple hidden layers",
      features: [
        "Learns complex patterns",
        "Multi-hidden layer architecture",
        "ReLU activation functions"
      ]
    },
    {
      title: "Random Forest Classification",
      description: "Ensemble of decision trees with voting mechanism",
      features: [
        "Reduced overfitting",
        "Parallel processing",
        "Feature interactions"
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