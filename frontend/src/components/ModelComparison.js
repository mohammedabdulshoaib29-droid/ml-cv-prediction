import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line } from 'recharts';
import '../styles/ModelComparison.css';

const ModelComparison = ({ results }) => {
  if (!results || !results.models) {
    return null;
  }

  // Prepare data for comparison chart
  const comparisonData = Object.entries(results.models).map(([modelName, data]) => ({
    name: modelName.toUpperCase(),
    accuracy: data.accuracy ? parseFloat(data.accuracy.toFixed(4)) : 0,
    rmse: data.rmse ? parseFloat(data.rmse.toFixed(4)) : 0,
    mae: data.mae ? parseFloat(data.mae.toFixed(4)) : 0,
  }));

  // Prepare data for predictions visualization
  const predictionData = [];
  const allPredictions = Object.entries(results.models)[0]?.[1]?.all_predictions || [];
  
  if (allPredictions.length > 0) {
    allPredictions.slice(0, 20).forEach((_, idx) => {
      const point = { index: idx };
      Object.entries(results.models).forEach(([modelName, data]) => {
        if (data.all_predictions && data.all_predictions[idx] !== undefined) {
          point[modelName] = parseFloat(data.all_predictions[idx].toFixed(4));
        }
      });
      predictionData.push(point);
    });
  }

  return (
    <div className="model-comparison-container">
      <div className="comparison-section">
        <h2>Model Performance Comparison</h2>
        
        <ResponsiveContainer width="100%" height={350}>
          <BarChart data={comparisonData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="accuracy" fill="#8884d8" name="Accuracy" />
            <Bar dataKey="rmse" fill="#82ca9d" name="RMSE" />
            <Bar dataKey="mae" fill="#ffc658" name="MAE" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {predictionData.length > 0 && (
        <div className="predictions-section">
          <h2>Predictions Comparison (First 20 samples)</h2>
          <ResponsiveContainer width="100%" height={350}>
            <LineChart data={predictionData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="index" />
              <YAxis />
              <Tooltip />
              <Legend />
              {Object.keys(results.models).map((modelName, idx) => (
                <Line
                  key={modelName}
                  type="monotone"
                  dataKey={modelName}
                  stroke={['#8884d8', '#82ca9d', '#ffc658'][idx]}
                  connectNulls
                />
              ))}
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}

      {results.feature_importance && (
        <div className="feature-importance-section">
          <h2>Feature Importance</h2>
          <div className="feature-importance-grid">
            {Object.entries(results.feature_importance).map(([modelName, importance]) => (
              <div key={modelName} className="feature-importance-box">
                <h4>{modelName.toUpperCase()}</h4>
                <ul>
                  {Array.isArray(importance) && importance.slice(0, 5).map(([feature, value], idx) => (
                    <li key={idx}>
                      {feature}: <strong>{parseFloat(value.toFixed(4))}</strong>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ModelComparison;
