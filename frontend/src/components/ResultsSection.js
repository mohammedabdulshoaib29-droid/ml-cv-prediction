import React, { useState } from 'react';
import '../styles/ResultsSection.css';

const ResultsSection = ({ results, onRunAnother }) => {
  const [expandedMetrics, setExpandedMetrics] = useState(null);

  if (!results) {
    return null;
  }

  // Extract results by model type
  const getMetricsForModel = (modelName) => {
    if (results.results && results.results[modelName]) {
      return results.results[modelName];
    }
    return null;
  };

  // Get all model results
  const models = [];
  if (results.results) {
    if (results.results.ann) models.push({ name: 'ANN', key: 'ann', icon: '🧠' });
    if (results.results.rf) models.push({ name: 'Random Forest', key: 'rf', icon: '🌲' });
    if (results.results.xgb) models.push({ name: 'XGBoost', key: 'xgb', icon: '⚡' });
  }

  // Extract predictions data
  const predictions = results.predictions || [];
  const displayedPredictions = predictions.slice(0, 50);

  // Download CSV function
  const handleDownloadCSV = () => {
    if (!predictions || predictions.length === 0) {
      alert('No predictions to download');
      return;
    }

    // Get all unique keys from predictions
    const columns = predictions.length > 0 ? Object.keys(predictions[0]) : [];
    
    // Create CSV content
    let csvContent = columns.join(',') + '\n';
    predictions.forEach(row => {
      const values = columns.map(col => {
        const value = row[col];
        // Escape values that contain commas
        return typeof value === 'string' && value.includes(',') ? `"${value}"` : value;
      });
      csvContent += values.join(',') + '\n';
    });

    // Create blob and download
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `predictions-${Date.now()}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  };

  return (
    <section className="results-section">
      <div className="results-container">
        <div className="results-header">
          <h2>📊 Results</h2>
          <p className="section-subtitle">Prediction analysis and metrics</p>
        </div>

        {/* Metrics Cards */}
        <div className="metrics-grid">
          {models.map((model) => {
            const metrics = getMetricsForModel(model.key);
            if (!metrics) return null;

            return (
              <div key={model.key} className="metrics-card">
                <div className="metrics-header">
                  <h3>{model.icon} {model.name}</h3>
                </div>

                <div className="metrics-body">
                  {metrics.r2 !== undefined && (
                    <div className="metric-item">
                      <span className="metric-label">Accuracy (R²)</span>
                      <span className="metric-value">{(metrics.r2 * 100).toFixed(2)}%</span>
                    </div>
                  )}
                  {metrics.rmse !== undefined && (
                    <div className="metric-item">
                      <span className="metric-label">RMSE</span>
                      <span className="metric-value">{metrics.rmse.toFixed(4)}</span>
                    </div>
                  )}
                  {metrics.mae !== undefined && (
                    <div className="metric-item">
                      <span className="metric-label">MAE</span>
                      <span className="metric-value">{metrics.mae.toFixed(4)}</span>
                    </div>
                  )}
                  {metrics.precision !== undefined && (
                    <div className="metric-item">
                      <span className="metric-label">Precision</span>
                      <span className="metric-value">{(metrics.precision * 100).toFixed(2)}%</span>
                    </div>
                  )}
                  {metrics.recall !== undefined && (
                    <div className="metric-item">
                      <span className="metric-label">Recall</span>
                      <span className="metric-value">{(metrics.recall * 100).toFixed(2)}%</span>
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>

        {/* Predictions Table */}
        <div className="predictions-table-container">
          <h3>Predictions (First 50 rows)</h3>
          {displayedPredictions.length > 0 ? (
            <div className="table-wrapper">
              <table className="predictions-table">
                <thead>
                  <tr>
                    {Object.keys(displayedPredictions[0]).map((key) => (
                      <th key={key}>{key}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {displayedPredictions.map((row, idx) => (
                    <tr key={idx}>
                      {Object.values(row).map((value, colIdx) => (
                        <td key={colIdx}>
                          {typeof value === 'number' ? value.toFixed(4) : String(value).substring(0, 30)}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p className="no-predictions">No predictions available</p>
          )}
          {predictions.length > 50 && (
            <p className="predictions-truncated">
              Showing 50 of {predictions.length} predictions. Download CSV to see all results.
            </p>
          )}
        </div>

        {/* Action Buttons */}
        <div className="results-actions">
          <button onClick={handleDownloadCSV} className="btn btn-download">
            📥 Download Results as CSV
          </button>
          <button onClick={onRunAnother} className="btn btn-run-another">
            🔄 Run Another Prediction
          </button>
        </div>
      </div>
    </section>
  );
};

export default ResultsSection;
