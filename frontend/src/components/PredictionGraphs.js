import React, { useState } from 'react';
import {
  LineChart, Line, BarChart, Bar,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  Cell, PieChart, Pie
} from 'recharts';
import '../styles/PredictionGraphs.css';

const PredictionGraphs = ({ results }) => {
  const [activeTab, setActiveTab] = useState('comparison');

  if (!results || (!results.models && !results.graphs)) {
    return null;
  }

  const hasGraphs = results.graphs && typeof results.graphs === 'object';

  const COLORS = ['#64c8ff', '#00d4ff', '#4db8ff', '#5ac5ff', '#4080ff'];

  const prepareComparisonData = () => {
    const firstModel = Object.values(results.models)[0];
    if (!firstModel || !firstModel.all_predictions) return [];
    return firstModel.all_predictions.slice(0, 50).map((pred, idx) => ({
      index: `S${idx + 1}`,
      predicted: parseFloat(pred.toFixed(2))
    }));
  };

  return (
    <div className="prediction-graphs">
      <h3>📊 Visualization &amp; Analysis</h3>
      
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
      </div>

      <div className="graph-content">
        {hasGraphs && activeTab === 'cv-graphs' && (
          <div className="graph-container">
            <h4>📊 Concentration vs Capacitance - All Models</h4>
            <div className="cv-graphs-grid">
              {Object.entries(results.graphs).map(([modelName, graphData]) => {
                const chartData = (graphData?.x && graphData?.y) ? 
                  graphData.x.map((concentration, idx) => ({
                    concentration: parseFloat(concentration.toFixed(2)),
                    capacitance: parseFloat((graphData.y[idx] || 0).toFixed(2))
                  })) : [];
                
                return (
                  <div key={modelName} className="model-cv-graph">
                    <h5>{modelName === 'ANN' ? '🧠 ANN' : modelName === 'RF' ? '🌲 RF' : '⚡ XGB'}</h5>
                    <ResponsiveContainer width="100%" height={350}>
                      <LineChart data={chartData}>
                        <CartesianGrid strokeDasharray="3 3" stroke="rgba(100, 200, 255, 0.2)" />
                        <XAxis dataKey="concentration" stroke="#aaa" />
                        <YAxis stroke="#aaa" />
                        <Tooltip contentStyle={{ backgroundColor: '#1a1a2e' }} />
                        <Legend />
                        <Line 
                          type="monotone" 
                          dataKey="capacitance" 
                          stroke={modelName === 'ANN' ? '#64c8ff' : modelName === 'RF' ? '#00ff88' : '#ff6b6b'} 
                          dot={false}
                          strokeWidth={3}
                        />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {activeTab === 'comparison' && (
          <div className="graph-container">
            <h4>Prediction Values</h4>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart data={prepareComparisonData()}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(100, 200, 255, 0.2)" />
                <XAxis dataKey="index" stroke="#aaa" />
                <YAxis stroke="#aaa" />
                <Tooltip contentStyle={{ backgroundColor: '#1a1a2e' }} />
                <Legend />
                <Line type="monotone" dataKey="predicted" stroke="#64c8ff" dot={false} strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>
    </div>
  );
};

export default PredictionGraphs;
