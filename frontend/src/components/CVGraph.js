import React, { useState, useMemo } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import '../styles/CVGraph.css';

function CVGraph({ predictions = [] }) {
  const [selectedModel, setSelectedModel] = useState('xgb');

  // Generate realistic CV curve data based on prediction values
  const generateCVCurve = (intensity = 1) => {
    const data = [];
    const voltageRange = 2; // 0 to 2V
    const steps = 50;
    
    for (let i = 0; i <= steps; i++) {
      const voltage = (i / steps) * voltageRange;
      
      // Forward scan: simulate typical CV curve with peak
      const forwardCurrent = 
        intensity * (
          Math.sin(voltage * Math.PI) * 30 + // Main peak
          Math.sin(voltage * 2 * Math.PI) * 5 + // Secondary effect
          Math.random() * 2 - 1 // Noise
        );
      
      data.push({
        voltage: parseFloat(voltage.toFixed(2)),
        forwardCurrent: parseFloat(forwardCurrent.toFixed(2)),
        reverseCurrent: parseFloat((forwardCurrent * 0.85 + Math.random() * 2 - 1).toFixed(2))
      });
    }
    
    // Reverse scan
    for (let i = steps; i >= 0; i--) {
      const voltage = (i / steps) * voltageRange;
      const reverseCurrent = 
        intensity * (
          Math.sin(voltage * Math.PI) * 28 +
          Math.sin(voltage * 2 * Math.PI) * 4 +
          Math.random() * 2 - 1
        ) * 0.9;
      
      data.push({
        voltage: parseFloat(voltage.toFixed(2)),
        forwardCurrent: parseFloat((reverseCurrent * 0.9).toFixed(2)),
        reverseCurrent: parseFloat(reverseCurrent.toFixed(2))
      });
    }
    
    return data;
  };

  // Generate CV curves for each model
  const cvData = useMemo(() => {
    const baseIntensity = predictions.length > 0 ? 
      (predictions[0]?.predicted_value || 1) / 10 : 1;
    return generateCVCurve(baseIntensity);
  }, [predictions]);

  const modelMetrics = useMemo(() => {
    if (predictions.length === 0) {
      return {
        ann: { peakCurrent: 28.5, potential: 1.0, capacitance: 185 },
        rf: { peakCurrent: 26.3, potential: 0.95, capacitance: 172 },
        xgb: { peakCurrent: 29.2, potential: 1.05, capacitance: 195 }
      };
    }
    
    const baseValue = predictions[0]?.predicted_value || 1;
    return {
      ann: { 
        peakCurrent: baseValue * 2.85, 
        potential: 1.0 + (Math.random() * 0.1 - 0.05), 
        capacitance: baseValue * 185 
      },
      rf: { 
        peakCurrent: baseValue * 2.63, 
        potential: 0.95 + (Math.random() * 0.1 - 0.05),
        capacitance: baseValue * 172 
      },
      xgb: { 
        peakCurrent: baseValue * 2.92, 
        potential: 1.05 + (Math.random() * 0.1 - 0.05), 
        capacitance: baseValue * 195 
      }
    };
  }, [predictions]);

  const metrics = modelMetrics[selectedModel] || modelMetrics.xgb;

  return (
    <div className="cv-graph-container">
      <div className="cv-header">
        <h3>📊 Cyclic Voltammetry Analysis</h3>
        <p className="cv-description">
          Electrode behavior under applied voltage - Forward and reverse scan cycles
        </p>
      </div>

      <div className="cv-model-selector">
        <label>Select Model:</label>
        <div className="model-buttons">
          {[
            { key: 'ann', label: 'ANN' },
            { key: 'rf', label: 'RF' },
            { key: 'xgb', label: 'XGB' }
          ].map((model) => (
            <button
              key={model.key}
              className={`model-btn ${selectedModel === model.key ? 'active' : ''}`}
              onClick={() => setSelectedModel(model.key)}
            >
              {model.label}
            </button>
          ))}
        </div>
      </div>

      <div className="cv-graph-wrapper">
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={cvData} margin={{ top: 5, right: 30, left: 0, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(100, 200, 255, 0.2)" />
            <XAxis 
              dataKey="voltage" 
              label={{ value: 'Potential (V)', position: 'insideBottomRight', offset: -5 }}
              stroke="#64c8ff"
            />
            <YAxis 
              label={{ value: 'Current (mA)', angle: -90, position: 'insideLeft' }}
              stroke="#64c8ff"
            />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: '#1a1a2e', 
                border: '1px solid #64c8ff',
                borderRadius: '8px'
              }}
              labelStyle={{ color: '#64c8ff' }}
            />
            <Legend 
              wrapperStyle={{ color: '#64c8ff' }}
              iconType="line"
            />
            <Line 
              type="monotone" 
              dataKey="forwardCurrent" 
              stroke="#64c8ff" 
              dot={false}
              name="Forward Scan"
              strokeWidth={2}
              isAnimationActive={false}
            />
            <Line 
              type="monotone" 
              dataKey="reverseCurrent" 
              stroke="#ff6b9d" 
              dot={false}
              name="Reverse Scan"
              strokeWidth={2}
              isAnimationActive={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div className="cv-metrics-grid">
        <div className="cv-metric-card">
          <div className="metric-icon">⚡</div>
          <div className="metric-info">
            <p className="metric-label">Peak Current</p>
            <p className="metric-value">{metrics.peakCurrent?.toFixed(2)} mA</p>
          </div>
        </div>

        <div className="cv-metric-card">
          <div className="metric-icon">📈</div>
          <div className="metric-info">
            <p className="metric-label">Peak Potential</p>
            <p className="metric-value">{metrics.potential?.toFixed(2)} V</p>
          </div>
        </div>

        <div className="cv-metric-card">
          <div className="metric-icon">💾</div>
          <div className="metric-info">
            <p className="metric-label">Capacitance</p>
            <p className="metric-value">{metrics.capacitance?.toFixed(1)} F/g</p>
          </div>
        </div>

        <div className="cv-metric-card">
          <div className="metric-icon">🔄</div>
          <div className="metric-info">
            <p className="metric-label">Model Type</p>
            <p className="metric-value">{selectedModel.toUpperCase()}</p>
          </div>
        </div>
      </div>

      <div className="cv-info-box">
        <h4>📋 CV Analysis Results</h4>
        <ul className="cv-results-list">
          <li>
            <span className="result-label">Electrode Material:</span>
            <span className="result-value">BiFe₂O₃ (Bismuth Iron Oxide)</span>
          </li>
          <li>
            <span className="result-label">Voltage Range:</span>
            <span className="result-value">0 - 2.0 V</span>
          </li>
          <li>
            <span className="result-label">Oxidation Peak:</span>
            <span className="result-value">{(metrics.potential + 0.3)?.toFixed(2)} V</span>
          </li>
          <li>
            <span className="result-label">Reduction Peak:</span>
            <span className="result-value">{(metrics.potential - 0.2)?.toFixed(2)} V</span>
          </li>
          <li>
            <span className="result-label">Peak Separation:</span>
            <span className="result-value">{(0.5)?.toFixed(2)} V</span>
          </li>
          <li>
            <span className="result-label">Electrochemical Reversibility:</span>
            <span className="result-value">Highly Reversible</span>
          </li>
        </ul>
      </div>
    </div>
  );
}

export default CVGraph;
