import React, { useState } from 'react';
import {
  LineChart, Line,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';
import '../styles/PredictionGraphs.css';

const PredictionGraphs = ({ results }) => {
  const [activeTab, setActiveTab] = useState('cv-graphs');

  if (!results || !results.graphs) {
    return null;
  }

  const hasGraphs = results.graphs && typeof results.graphs === 'object';

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
        {results.recommendations && (
          <button 
            className={`graph-tab ${activeTab === 'recommendations' ? 'active' : ''}`}
            onClick={() => setActiveTab('recommendations')}
          >
            💡 Recommendations
          </button>
        )}
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
                    {chartData.length > 0 ? (
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
                            name="Capacitance (F/g)"
                          />
                        </LineChart>
                      </ResponsiveContainer>
                    ) : (
                      <p className="no-data">No graph data available</p>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {activeTab === 'recommendations' && results.recommendations && (
          <div className="recommendations-container">
            <h4>💡 Model Recommendations</h4>
            <div className="recommendations-list">
              {results.recommendations.map((rec, idx) => (
                <div key={idx} className="recommendation-item">
                  <p>{rec}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default PredictionGraphs;
