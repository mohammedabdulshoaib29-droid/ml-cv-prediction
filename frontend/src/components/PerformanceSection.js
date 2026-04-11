import React from 'react';
import '../styles/PerformanceSection.css';

function PerformanceSection() {
  return (
    <section id="performance" className="performance">
      <div className="performance-container">
        <h2>Model Performance & Metrics</h2>
        
        <div className="performance-grid">
          <div className="model-card">
            <h3>🚀 XGBoost</h3>
            <div className="metrics">
              <div className="metric">
                <span className="metric-label">Accuracy</span>
                <span className="metric-value">87.5%</span>
              </div>
              <div className="metric">
                <span className="metric-label">Precision</span>
                <span className="metric-value">85.3%</span>
              </div>
              <div className="metric">
                <span className="metric-label">Recall</span>
                <span className="metric-value">84.2%</span>
              </div>
              <div className="metric">
                <span className="metric-label">RMSE</span>
                <span className="metric-value">0.156</span>
              </div>
            </div>
          </div>

          <div className="model-card">
            <h3>🧠 TensorFlow NN</h3>
            <div className="metrics">
              <div className="metric">
                <span className="metric-label">Accuracy</span>
                <span className="metric-value">86.2%</span>
              </div>
              <div className="metric">
                <span className="metric-label">Precision</span>
                <span className="metric-value">84.1%</span>
              </div>
              <div className="metric">
                <span className="metric-label">Recall</span>
                <span className="metric-value">83.8%</span>
              </div>
              <div className="metric">
                <span className="metric-label">RMSE</span>
                <span className="metric-value">0.168</span>
              </div>
            </div>
          </div>

          <div className="model-card">
            <h3>🌲 Random Forest</h3>
            <div className="metrics">
              <div className="metric">
                <span className="metric-label">Accuracy</span>
                <span className="metric-value">85.9%</span>
              </div>
              <div className="metric">
                <span className="metric-label">Precision</span>
                <span className="metric-label">83.7%</span>
              </div>
              <div className="metric">
                <span className="metric-label">Recall</span>
                <span className="metric-value">82.5%</span>
              </div>
              <div className="metric">
                <span className="metric-label">RMSE</span>
                <span className="metric-value">0.175</span>
              </div>
            </div>
          </div>
        </div>

        <div className="training-info">
          <h3>📊 Training Configuration</h3>
          <div className="training-details">
            <div className="detail">
              <span className="label">Optimizer:</span>
              <span className="value">Adam (TensorFlow), Gradient Boost (XGBoost)</span>
            </div>
            <div className="detail">
              <span className="label">Learning Rate:</span>
              <span className="value">0.001 - 0.0001</span>
            </div>
            <div className="detail">
              <span className="label">Train/Test Split:</span>
              <span className="value">80% / 20%</span>
            </div>
            <div className="detail">
              <span className="label">Dataset:</span>
              <span className="value">Cyclic Voltammetry Measurements</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default PerformanceSection;