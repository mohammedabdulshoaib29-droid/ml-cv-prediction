import React from 'react';
import '../styles/ComponentsSection.css';

function ComponentsSection() {
  const components = [
    {
      title: "Tensor Neural Network (TNN)",
      description: "Advanced deep learning model with tensor operations",
      features: [
        "Tensor-based computations",
        "Efficient matrix operations",
        "Optimized gradient descent"
      ]
    },
    {
      title: "Artificial Neural Network (ANN)",
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