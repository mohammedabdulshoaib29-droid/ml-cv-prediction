import React, { useState } from 'react';
import {
  LineChart, Line, BarChart, Bar, ScatterChart, Scatter,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  Cell, PieChart, Pie
} from 'recharts';
import '../styles/PredictionGraphs.css';

const PredictionGraphs = ({ results }) => {
  const [activeTab, setActiveTab] = useState('comparison');

  if (!results || (!results.models && !results.graphs)) {
    return null;
  }

  // Check if this is CV analysis with graphs
  const hasGraphs = results.graphs && typeof results.graphs === 'object';

  // Prepare data for actual vs predicted graph
  const prepareComparisonData = () => {
    const firstModel = Object.values(results.models)[0];
    if (!firstModel || !firstModel.all_predictions) return [];

    const predictions = firstModel.all_predictions;
    return predictions.slice(0, 50).map((pred, idx) => ({
      index: `S${idx + 1}`,
      predicted: parseFloat(pred.toFixed(2)),
      order: idx
    }));
  };

  // Prepare data for model comparison (metrics)
  const prepareModelMetricsData = () => {
    return Object.entries(results.models).map(([modelName, data]) => ({
      name: modelName.toUpperCase(),
      accuracy: data.accuracy ? parseFloat(data.accuracy.toFixed(3)) : 0,
      rmse: data.rmse ? 100 - parseFloat(data.rmse.toFixed(3)) : 50,
      r2: data.r2_score ? parseFloat(data.r2_score.toFixed(3)) * 100 : 0
    }));
  };

  // Prepare data for prediction distribution
  const preparePredictionDistribution = () => {
    const firstModel = Object.values(results.models)[0];
    if (!firstModel || !firstModel.all_predictions) return [];

    const predictions = firstModel.all_predictions;
    const min = Math.min(...predictions);
    const max = Math.max(...predictions);
    const binSize = (max - min) / 10;

    const bins = Array(10).fill(0);
    predictions.forEach(pred => {
      const binIndex = Math.min(9, Math.floor((pred - min) / binSize));
      bins[binIndex]++;
    });

    return bins.map((count, idx) => ({
      range: `${(min + idx * binSize).toFixed(1)}-${(min + (idx + 1) * binSize).toFixed(1)}`,
      count: count,
      percentage: ((count / predictions.length) * 100).toFixed(1)
    }));
  };

  // Prepare data for model performance pie chart
  const prepareModelPerformance = () => {
    return Object.entries(results.models).map(([modelName, data]) => ({
      name: modelName.toUpperCase(),
      value: data.accuracy ? parseFloat(data.accuracy.toFixed(3)) * 100 : 50,
      rmse: data.rmse || 0
    }));
  };

  const COLORS = ['#64c8ff', '#00d4ff', '#4db8ff', '#5ac5ff', '#4080ff'];

  return (
    <div className="prediction-graphs">
      <h3>📊 Visualization & Analysis</h3>
      
      <div className="graph-tabs">
        {hasGraphs && (
          <button 
            className={`graph-tab ${activeTab === 'cv-graphs' ? 'active' : ''}`}
            onClick={() => setActiveTab('cv-graphs')}
          >
            🔬 CV Curves
          </button>
        )}
        <button 
          className={`graph-tab ${activeTab === 'comparison' ? 'active' : ''}`}
          onClick={() => setActiveTab('comparison')}
        >
          📈 Predictions
        </button>
        <button 
          className={`graph-tab ${activeTab === 'distribution' ? 'active' : ''}`}
          onClick={() => setActiveTab('distribution')}
        >
          📊 Distribution
        </button>
        <button 
          className={`graph-tab ${activeTab === 'models' ? 'active' : ''}`}
          onClick={() => setActiveTab('models')}
        >
          🎯 Model Comparison
        </button>
        <button 
          className={`graph-tab ${activeTab === 'performance' ? 'active' : ''}`}
          onClick={() => setActiveTab('performance')}
        >
          ⭐ Performance
        </button>
      </div>

      <div className="graph-content">
        {hasGraphs && activeTab === 'cv-graphs' && (
          <div className="graph-container">
            <h4>CV Curve Analysis - All Models</h4>
            <p className="graph-description">
              Cyclic Voltammetry curves for each model with current vs. potential response
            </p>
            <div className="cv-graphs-grid">
              {Object.entries(results.graphs).map(([modelName, graphData]) => (
                <div key={modelName} className="model-cv-graph">
                  <h5>{modelName}</h5>
                  <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={graphData || []}>
                      <CartesianGrid strokeDasharray="3 3" stroke="rgba(100, 200, 255, 0.2)" />
                      <XAxis 
                        dataKey="voltage" 
                        stroke="#aaa"
                        label={{ value: 'Potential (V)', position: 'insideBottomRight', offset: -5 }}
                        tick={{ fontSize: 12 }}
                      />
                      <YAxis 
                        stroke="#aaa"
                        label={{ value: 'Current (mA)', angle: -90, position: 'insideLeft' }}
                        tick={{ fontSize: 12 }}
                      />
                      <Tooltip 
                        contentStyle={{ backgroundColor: '#1a1a2e', border: '1px solid #64c8ff' }}
                        labelStyle={{ color: '#64c8ff' }}
                      />
                      <Legend />
                      <Line 
                        type="monotone" 
                        dataKey="forwardCurrent" 
                        stroke="#64c8ff" 
                        dot={false}
                        strokeWidth={2}
                        name="Forward Scan"
                      />
                      <Line 
                        type="monotone" 
                        dataKey="reverseCurrent" 
                        stroke="#00d4ff" 
                        dot={false}
                        strokeWidth={2}
                        name="Reverse Scan"
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              ))}
            </div>
          </div>
        )}
        {activeTab === 'comparison' && (
          <div className="graph-container">
            <h4>Prediction Values (First 50 Samples)</h4>
            <p className="graph-description">
              Shows the predicted values across test samples. Each point represents one prediction.
            </p>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart data={prepareComparisonData()}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(100, 200, 255, 0.2)" />
                <XAxis 
                  dataKey="index" 
                  stroke="#aaa"
                  tick={{ fontSize: 12 }}
                />
                <YAxis 
                  stroke="#aaa"
                  tick={{ fontSize: 12 }}
                />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#1a1a2e', border: '1px solid #64c8ff' }}
                  labelStyle={{ color: '#64c8ff' }}
                />
                <Legend />
                <Line 
                  type="monotone" 
                  dataKey="predicted" 
                  stroke="#64c8ff" 
                  dot={false}
                  strokeWidth={2}
                  name="Predicted Value"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}

        {activeTab === 'distribution' && (
          <div className="graph-container">
            <h4>Prediction Distribution</h4>
            <p className="graph-description">
              Shows how predictions are distributed across value ranges. Helps identify patterns in model output.
            </p>
            <ResponsiveContainer width="100%" height={400}>
              <BarChart data={preparePredictionDistribution()}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(100, 200, 255, 0.2)" />
                <XAxis 
                  dataKey="range" 
                  stroke="#aaa"
                  angle={-45}
                  textAnchor="end"
                  height={80}
                  tick={{ fontSize: 12 }}
                />
                <YAxis 
                  stroke="#aaa"
                  tick={{ fontSize: 12 }}
                />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#1a1a2e', border: '1px solid #64c8ff' }}
                  labelStyle={{ color: '#64c8ff' }}
                  formatter={(value, name) => [
                    name === 'count' ? `${value} samples` : `${value}%`,
                    name === 'count' ? 'Count' : 'Percentage'
                  ]}
                />
                <Bar dataKey="count" fill="#64c8ff" name="Samples in Range" radius={[8, 8, 0, 0]}>
                  {preparePredictionDistribution().map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}

        {activeTab === 'models' && (
          <div className="graph-container">
            <h4>Model Metrics Comparison</h4>
            <p className="graph-description">
              Compares performance metrics across different models. Higher values indicate better performance.
            </p>
            <ResponsiveContainer width="100%" height={400}>
              <BarChart data={prepareModelMetricsData()}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(100, 200, 255, 0.2)" />
                <XAxis 
                  dataKey="name" 
                  stroke="#aaa"
                  tick={{ fontSize: 12 }}
                />
                <YAxis 
                  stroke="#aaa"
                  tick={{ fontSize: 12 }}
                  label={{ value: 'Score (%)', angle: -90, position: 'insideLeft' }}
                />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#1a1a2e', border: '1px solid #64c8ff' }}
                  labelStyle={{ color: '#64c8ff' }}
                  formatter={(value) => value.toFixed(2)}
                />
                <Legend />
                <Bar dataKey="accuracy" fill="#64c8ff" name="Accuracy" radius={[8, 8, 0, 0]} />
                <Bar dataKey="r2" fill="#4db8ff" name="R² Score" radius={[8, 8, 0, 0]} />
                <Bar dataKey="rmse" fill="#00d4ff" name="1-RMSE" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}

        {activeTab === 'performance' && (
          <div className="graph-container">
            <h4>Model Accuracy Distribution</h4>
            <p className="graph-description">
              Pie chart showing the relative accuracy performance of each model.
            </p>
            <ResponsiveContainer width="100%" height={400}>
              <PieChart>
                <Pie
                  data={prepareModelPerformance()}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, value }) => `${name}: ${value.toFixed(1)}%`}
                  outerRadius={120}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {prepareModelPerformance().map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip 
                  contentStyle={{ backgroundColor: '#1a1a2e', border: '1px solid #64c8ff' }}
                  labelStyle={{ color: '#64c8ff' }}
                  formatter={(value) => `${value.toFixed(2)}%`}
                />
              </PieChart>
            </ResponsiveContainer>
            
            <div className="performance-summary">
              <h5>Model Performance Summary</h5>
              <div className="summary-grid">
                {Object.entries(results.models).map(([modelName, data]) => (
                  <div key={modelName} className="summary-card">
                    <h6>{modelName.toUpperCase()}</h6>
                    <div className="metric-display">
                      {data.accuracy !== undefined && (
                        <div className="metric-item">
                          <span className="metric-label">Accuracy:</span>
                          <span className="metric-value">{(data.accuracy * 100).toFixed(2)}%</span>
                        </div>
                      )}
                      {data.rmse !== undefined && (
                        <div className="metric-item">
                          <span className="metric-label">RMSE:</span>
                          <span className="metric-value">{data.rmse.toFixed(4)}</span>
                        </div>
                      )}
                      {data.r2_score !== undefined && (
                        <div className="metric-item">
                          <span className="metric-label">R² Score:</span>
                          <span className="metric-value">{(data.r2_score * 100).toFixed(2)}%</span>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default PredictionGraphs;
