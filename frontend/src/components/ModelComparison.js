import React, { useState, useEffect } from 'react';
import '../styles/ModelComparison.css';
import PerformanceChart from './PerformanceChart';
import PredictionPlot from './PredictionPlot';

const ModelComparison = ({ results }) => {
  const [selectedModel, setSelectedModel] = useState(null);

  useEffect(() => {
    if (results?.models) {
      const models = Object.keys(results.models).filter(m => results.models[m].success);
      if (models.length > 0) {
        setSelectedModel(models[0]);
      }
    }
  }, [results]);

  if (!results || !results.models) {
    return <div className="loading">Loading results...</div>;
  }

  const models = Object.entries(results.models).filter(([_, r]) => r.success);
  const selectedModelData = selectedModel && results.models[selectedModel];

  // Prepare comparison data for chart
  const comparisonData = {
    models: models.map(([name]) => name),
    r2Scores: models.map(([name]) => results.models[name].metrics.r2_score),
    rmseValues: models.map(([name]) => results.models[name].metrics.rmse),
    maeValues: models.map(([name]) => results.models[name].metrics.mae)
  };

  return (
    <div className="model-comparison">
      <h2>📈 Model Results & Comparison</h2>

      {/* Best Model Highlight */}
      {results.best_model && (
        <div className="best-model-card">
          <h3>🏆 Best Model</h3>
          <p className="best-model-name">{results.best_model.name}</p>
          <p className="best-model-score">R² Score: {results.best_model.r2_score.toFixed(4)}</p>
        </div>
      )}

      {/* Comparison Charts */}
      <div className="charts-section">
        <h3>Performance Comparison</h3>
        <div className="charts-grid">
          <div className="chart-container">
            <h4>R² Score Comparison</h4>
            <PerformanceChart
              labels={comparisonData.models}
              data={comparisonData.r2Scores}
              title="R² Score"
              color="rgb(75, 192, 192)"
              type="bar"
            />
          </div>
          <div className="chart-container">
            <h4>RMSE Comparison</h4>
            <PerformanceChart
              labels={comparisonData.models}
              data={comparisonData.rmseValues}
              title="RMSE"
              color="rgb(255, 99, 132)"
              type="bar"
            />
          </div>
        </div>
      </div>

      {/* Model Selection Tabs */}
      <div className="model-tabs">
        <h3>Select Model for Details</h3>
        <div className="tabs">
          {models.map(([name]) => (
            <button
              key={name}
              className={`tab ${selectedModel === name ? 'active' : ''}`}
              onClick={() => setSelectedModel(name)}
            >
              {name}
            </button>
          ))}
        </div>
      </div>

      {/* Selected Model Details */}
      {selectedModelData && (
        <div className="model-details">
          <h3>{selectedModel} - Detailed Results</h3>

          {/* Metrics */}
          <div className="metrics-grid">
            <div className="metric-card">
              <h4>R² Score</h4>
              <p className="metric-value">{selectedModelData.metrics.r2_score.toFixed(4)}</p>
              <p className="metric-label">Model Accuracy</p>
            </div>
            <div className="metric-card">
              <h4>RMSE</h4>
              <p className="metric-value">{selectedModelData.metrics.rmse.toFixed(4)}</p>
              <p className="metric-label">Root Mean Squared Error</p>
            </div>
            <div className="metric-card">
              <h4>MAE</h4>
              <p className="metric-value">{selectedModelData.metrics.mae.toFixed(4)}</p>
              <p className="metric-label">Mean Absolute Error</p>
            </div>
            <div className="metric-card">
              <h4>Best Capacitance</h4>
              <p className="metric-value">{selectedModelData.best_capacitance.toFixed(2)} F/g</p>
              <p className="metric-label">Optimal Prediction</p>
            </div>
          </div>

          {/* Sample Details */}
          <div className="sample-info">
            <p><strong>Training Samples:</strong> {selectedModelData.metrics.train_samples}</p>
            <p><strong>Test Samples:</strong> {selectedModelData.metrics.test_samples}</p>
          </div>

          {/* Actual vs Predicted Plot */}
          <div className="plot-section">
            <h4>Actual vs Predicted Values</h4>
            <PredictionPlot
              actual={selectedModelData.predictions.actual}
              predicted={selectedModelData.predictions.predicted}
              modelName={selectedModel}
            />
          </div>

          {/* Capacitance Profile */}
          {selectedModelData.capacitance_profile && (
            <div className="capacitance-section">
              <h4>Capacitance Profile</h4>
              <p>Best Concentration: {selectedModelData.best_concentration.toFixed(2)}</p>
              <p>Best Capacitance: {selectedModelData.best_capacitance.toFixed(2)} F/g</p>
            </div>
          )}

          {/* Feature Importance */}
          {selectedModelData.feature_importance && (
            <div className="importance-section">
              <h4>Feature Importance</h4>
              <div className="importance-bars">
                {Object.entries(selectedModelData.feature_importance)
                  .sort(([, a], [, b]) => b - a)
                  .map(([feature, importance]) => (
                    <div key={feature} className="importance-bar">
                      <label>{feature}</label>
                      <div className="bar-container">
                        <div
                          className="bar"
                          style={{ width: `${importance * 100}%` }}
                        ></div>
                      </div>
                      <span>{(importance * 100).toFixed(1)}%</span>
                    </div>
                  ))}
              </div>
            </div>
          )}

          {/* Training History */}
          {selectedModelData.training_history && (
            <div className="training-history">
              <h4>Training Information</h4>
              <p>Epochs: {selectedModelData.training_history.epochs}</p>
              <p>Final Loss: {selectedModelData.training_history.final_loss.toFixed(6)}</p>
              <p>Final Validation Loss: {selectedModelData.training_history.final_val_loss.toFixed(6)}</p>
            </div>
          )}
        </div>
      )}

      {/* Error Handling */}
      {models.length === 0 && (
        <div className="error-message">
          ⚠️ Some models failed to train. Check your data and try again.
        </div>
      )}
    </div>
  );
};

export default ModelComparison;

