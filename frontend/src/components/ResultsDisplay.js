import React from 'react';
import { ClipLoader } from 'react-spinners';
import CVGraph from './CVGraph';
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

  if (!results) {
    return null;
  }

  const isCV = results.is_cv_analysis || results.graphs;

  return (
    <div className="results-container">
      <h2>{isCV ? '🔬 CV Analysis Results' : 'Prediction Results'}</h2>
      
      <div className="results-info">
        {results.task_type && <p><strong>Task Type:</strong> {results.task_type}</p>}
        <p><strong>Training Dataset:</strong> {results.training_dataset}</p>
        <p><strong>Test Samples:</strong> {results.test_samples}</p>
        {isCV && results.best_model && <p><strong>Best Model:</strong> {results.best_model}</p>}
        {isCV && results.best_dopant && <p><strong>Recommended Dopant:</strong> {results.best_dopant}</p>}
        {isCV && results.capacitance && <p><strong>Specific Capacitance:</strong> {parseFloat(results.capacitance.toFixed(2))} F/g</p>}
        {isCV && results.energy_density !== undefined && <p><strong>Energy Density:</strong> {parseFloat(results.energy_density.toFixed(2))} Wh/kg</p>}
        {isCV && results.power_density !== undefined && <p><strong>Power Density:</strong> {parseFloat(results.power_density.toFixed(2))} W/kg</p>}
      </div>

      {!isCV && <CVGraph predictions={Object.values(results.models || {}).flatMap(m => m.predictions || [])} />}

      {isCV && results.graphs && <PredictionGraphs results={results} />}

      {isCV && results.table ? (
        <div className="cv-table">
          <h3>Model Performance Comparison</h3>
          <table>
            <thead>
              <tr>
                <th>Model</th>
                <th>R² Score</th>
                <th>RMSE</th>
                <th>Capacitance (F/g)</th>
                <th>Best Concentration</th>
              </tr>
            </thead>
            <tbody>
              {results.table.map((row, idx) => (
                <tr key={idx}>
                  <td>{row.model}</td>
                  <td>{parseFloat(row.r2.toFixed(4))}</td>
                  <td>{parseFloat(row.rmse.toFixed(4))}</td>
                  <td>{parseFloat(row.capacitance.toFixed(2))}</td>
                  <td>{parseFloat(row.best_concentration.toFixed(4))}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : !isCV && results.models ? (
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
      ) : null}
    </div>
  );
}

export default ResultsDisplay;
