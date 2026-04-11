import React from 'react';
import { ClipLoader } from 'react-spinners';
import PredictionGraphs from './PredictionGraphs';
import '../styles/ResultsDisplay.css';

const ResultsDisplay = ({ results, loading, error }) => {
  if (loading) {
    return (
      <div className="loading-container">
        <ClipLoader color="#36d7b7" size={50} />
        <p>Processing predictions... This may take a moment.</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-container">
        <h3>⚠️ Error</h3>
        <p>{error}</p>
      </div>
    );
  }

  if (!results || !results.models) {
    return null;
  }

  const downloadCSV = () => {
    let csv = 'Model,Predictions\n';
    Object.entries(results.models).forEach(([modelName, data]) => {
      if (data.all_predictions) {
        csv += `${modelName},${data.all_predictions.join(',')}\n`;
      }
    });

    const element = document.createElement('a');
    element.setAttribute('href', 'data:text/csv;charset=utf-8,' + encodeURIComponent(csv));
    element.setAttribute('download', 'predictions.csv');
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  return (
    <div className="results-container">
      <h2>Prediction Results</h2>
      
      <div className="results-info">
        <p><strong>Task Type:</strong> {results.task_type}</p>
        <p><strong>Training Dataset:</strong> {results.training_dataset}</p>
        <p><strong>Test Samples:</strong> {results.test_samples}</p>
      </div>

      <div className="models-grid">
        {Object.entries(results.models).map(([modelName, data]) => (
          <div key={modelName} className="model-card">
            <h3>{modelName.toUpperCase()}</h3>
            
            {data.accuracy !== undefined && (
              <div className="metric">
                <label>Accuracy:</label>
                <span className="value">{parseFloat(data.accuracy.toFixed(4))}</span>
              </div>
            )}
            
            {data.rmse !== undefined && (
              <div className="metric">
                <label>RMSE:</label>
                <span className="value">{parseFloat(data.rmse.toFixed(4))}</span>
              </div>
            )}
            
            {data.mae !== undefined && (
              <div className="metric">
                <label>MAE:</label>
                <span className="value">{parseFloat(data.mae.toFixed(4))}</span>
              </div>
            )}

            {data.r2_score !== undefined && (
              <div className="metric">
                <label>R² Score:</label>
                <span className="value">{parseFloat(data.r2_score.toFixed(4))}</span>
              </div>
            )}

            {data.predictions && data.predictions.length > 0 && (
              <div className="predictions">
                <label>Sample Predictions (First 10):</label>
                <ul>
                  {data.predictions.map((pred, idx) => (
                    <li key={idx}>{parseFloat(pred.toFixed(4))}</li>
                  ))}
                </ul>
              </div>
            )}

            <div className={`status ${data.training_status === 'trained' ? 'success' : 'error'}`}>
              Status: {data.training_status}
            </div>
          </div>
        ))}
      </div>

      <button onClick={downloadCSV} className="download-btn">
        📥 Download Predictions as CSV
      </button>

      <PredictionGraphs results={results} />
    </div>
  );
};

export default ResultsDisplay;
