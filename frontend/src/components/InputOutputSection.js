import React from 'react';
import '../styles/InputOutputSection.css';

function InputOutputSection() {
  return (
    <section className="input-output">
      <div className="io-container">
        <h2>Model Input & Output Specification</h2>
        
        <div className="io-content">
          <div className="io-section">
            <h3>📥 Inputs</h3>
            <div className="inputs-list">
              <div className="input-item">
                <span className="icon">📄</span>
                <div>
                  <h4>Training Dataset (.xlsx / .csv)</h4>
                  <p>Cyclic voltammetry measurements with labeled behavioral data</p>
                </div>
              </div>
              <div className="input-item">
                <span className="icon">📊</span>
                <div>
                  <h4>Test Dataset (.xlsx / .csv)</h4>
                  <p>CV data for prediction without labels</p>
                </div>
              </div>
              <div className="input-item">
                <span className="icon">⚙️</span>
                <div>
                  <h4>Model Selection</h4>
                  <p>Choose: All models, XGBoost, Artificial Neural Network (ANN), or Random Forest</p>
                </div>
              </div>
            </div>
          </div>

          <div className="arrow-separator">→</div>

          <div className="io-section">
            <h3>📤 Outputs</h3>
            <div className="outputs-list">
              <div className="output-item">
                <span className="icon">🎯</span>
                <div>
                  <h4>Predictions</h4>
                  <p>Binary or continuous CV behavior classification</p>
                </div>
              </div>
              <div className="output-item">
                <span className="icon">📈</span>
                <div>
                  <h4>Performance Metrics</h4>
                  <p>Accuracy, Precision, Recall, RMSE, MAE</p>
                </div>
              </div>
              <div className="output-item">
                <span className="icon">🔍</span>
                <div>
                  <h4>Feature Importance</h4>
                  <p>Key features driving the predictions</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default InputOutputSection;