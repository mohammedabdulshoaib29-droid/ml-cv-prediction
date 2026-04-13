import React, { useState } from 'react';
import '../styles/CapacitorMetrics.css';

function CapacitorMetrics({ results }) {
  const [activeTab, setActiveTab] = useState('calculator');
  
  // Default CV parameters (can be modified by user)
  const [cvParams, setCvParams] = useState({
    voltage: 1.0,  // Voltage window in V
    mass: 1.0,      // Mass of active material in mg
    scanRate: 10,   // Scan rate in mV/s
    integralArea: 10 // Integral area from CV curve (normalized)
  });

  // Calculate Specific Capacitance (F/g)
  const calculateSpecificCapacitance = () => {
    // Formula: Cs = (Charge / 2) / (Mass * Voltage)
    // Charge can be estimated from integral area
    const charge = cvParams.integralArea * 0.1; // mC/V
    const mass_g = cvParams.mass / 1000; // Convert mg to g
    const specificCapacitance = (charge / 2) / (mass_g * cvParams.voltage);
    return specificCapacitance.toFixed(2);
  };

  // Calculate Energy Density (Wh/kg)
  const calculateEnergyDensity = () => {
    // Formula: E = (1/2 * C * V²) / 3600000 (to convert to Wh/kg)
    const specificCapacitance = parseFloat(calculateSpecificCapacitance());
    const energyDensity = (0.5 * specificCapacitance * cvParams.voltage * cvParams.voltage) / 3.6 / 1000;
    return energyDensity.toFixed(4);
  };

  // Calculate Power Density (W/kg)
  const calculatePowerDensity = () => {
    // Formula: P = (V² * conductivity) / (4 * thickness)
    // Simplified: P = Energy Density / Discharge time
    const energyDensity = parseFloat(calculateEnergyDensity());
    const dischargeTime = 0.001; // Hours (very fast discharge for capacitors)
    const powerDensity = (energyDensity * 3600) / (dischargeTime); // W/kg
    return powerDensity.toFixed(2);
  };

  // Calculate how parameters affect the metrics
  const analyzeImpact = () => {
    return {
      voltage: {
        effect: "Energy Density is proportional to V²",
        change: "↑ Voltage → ↑ Energy Density (quadratic)",
        optimal: "Higher voltages improve energy storage"
      },
      mass: {
        effect: "Specific Capacitance inversely proportional to mass",
        change: "↑ Mass → ↓ Specific Capacitance per gram",
        optimal: "Lower mass = higher specific capacitance"
      },
      scanRate: {
        effect: "Higher scan rates reduce accessible capacitance",
        change: "↑ Scan Rate → ↓ Effective Capacitance",
        optimal: "Slower scan rates for better performance"
      },
      integralArea: {
        effect: "Larger CV curve area indicates higher capacitance",
        change: "↑ Integral Area → ↑ All metrics",
        optimal: "Maximize CV curve area for better performance"
      }
    };
  };

  const handleParamChange = (param, value) => {
    setCvParams({
      ...cvParams,
      [param]: parseFloat(value)
    });
  };

  const impacts = analyzeImpact();

  return (
    <div className="capacitor-metrics">
      <div className="metrics-tabs">
        <button 
          className={`tab-btn ${activeTab === 'calculator' ? 'active' : ''}`}
          onClick={() => setActiveTab('calculator')}
        >
          🔧 Parameter Calculator
        </button>
        <button 
          className={`tab-btn ${activeTab === 'impact' ? 'active' : ''}`}
          onClick={() => setActiveTab('impact')}
        >
          📈 Parameter Impact
        </button>
      </div>

      <div className="metrics-content">
        {activeTab === 'calculator' && (
          <div className="calculator-panel">
            <h3>Adjust CV Parameters</h3>
            <p className="calc-subtitle">Modify these values to see how they affect the supercapacitor metrics</p>
            
            <div className="parameter-grid">
              <div className="param-input">
                <label>Voltage Window (V)</label>
                <div className="input-group">
                  <input
                    type="range"
                    min="0.5"
                    max="3.0"
                    step="0.1"
                    value={cvParams.voltage}
                    onChange={(e) => handleParamChange('voltage', e.target.value)}
                    className="slider"
                  />
                  <input
                    type="number"
                    min="0.5"
                    max="3.0"
                    step="0.1"
                    value={cvParams.voltage}
                    onChange={(e) => handleParamChange('voltage', e.target.value)}
                    className="number-input"
                  />
                </div>
                <p className="param-hint">Higher voltage = more energy storage</p>
              </div>

              <div className="param-input">
                <label>Active Material Mass (mg)</label>
                <div className="input-group">
                  <input
                    type="range"
                    min="0.5"
                    max="5.0"
                    step="0.1"
                    value={cvParams.mass}
                    onChange={(e) => handleParamChange('mass', e.target.value)}
                    className="slider"
                  />
                  <input
                    type="number"
                    min="0.5"
                    max="5.0"
                    step="0.1"
                    value={cvParams.mass}
                    onChange={(e) => handleParamChange('mass', e.target.value)}
                    className="number-input"
                  />
                </div>
                <p className="param-hint">Lower mass = higher specific values</p>
              </div>

              <div className="param-input">
                <label>Scan Rate (mV/s)</label>
                <div className="input-group">
                  <input
                    type="range"
                    min="1"
                    max="100"
                    step="1"
                    value={cvParams.scanRate}
                    onChange={(e) => handleParamChange('scanRate', e.target.value)}
                    className="slider"
                  />
                  <input
                    type="number"
                    min="1"
                    max="100"
                    step="1"
                    value={cvParams.scanRate}
                    onChange={(e) => handleParamChange('scanRate', e.target.value)}
                    className="number-input"
                  />
                </div>
                <p className="param-hint">Slower rates reveal true capacitance</p>
              </div>

              <div className="param-input">
                <label>CV Integral Area (a.u.)</label>
                <div className="input-group">
                  <input
                    type="range"
                    min="1"
                    max="50"
                    step="0.5"
                    value={cvParams.integralArea}
                    onChange={(e) => handleParamChange('integralArea', e.target.value)}
                    className="slider"
                  />
                  <input
                    type="number"
                    min="1"
                    max="50"
                    step="0.5"
                    value={cvParams.integralArea}
                    onChange={(e) => handleParamChange('integralArea', e.target.value)}
                    className="number-input"
                  />
                </div>
                <p className="param-hint">Larger area = higher charge storage</p>
              </div>
            </div>

            <div className="calculated-metrics">
              <h4>Live Calculation Results</h4>
              <div className="metrics-row">
                <div className="metric-box">
                  <span className="label">Specific Capacitance:</span>
                  <span className="value">{calculateSpecificCapacitance()} F/g</span>
                </div>
                <div className="metric-box">
                  <span className="label">Energy Density:</span>
                  <span className="value">{calculateEnergyDensity()} Wh/kg</span>
                </div>
                <div className="metric-box">
                  <span className="label">Power Density:</span>
                  <span className="value">{calculatePowerDensity()} W/kg</span>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'impact' && (
          <div className="impact-analysis">
            <h3>How Parameters Affect Performance</h3>
            <p className="impact-subtitle">Understanding the relationships between CV parameters and supercapacitor metrics</p>
            
            <div className="impact-grid">
              <div className="impact-card">
                <h4>⚙️ Voltage Window</h4>
                <p className="impact-effect">{impacts.voltage.effect}</p>
                <p className="impact-change">{impacts.voltage.change}</p>
                <p className="impact-optimal">💡 {impacts.voltage.optimal}</p>
              </div>

              <div className="impact-card">
                <h4>⚖️ Active Material Mass</h4>
                <p className="impact-effect">{impacts.mass.effect}</p>
                <p className="impact-change">{impacts.mass.change}</p>
                <p className="impact-optimal">💡 {impacts.mass.optimal}</p>
              </div>

              <div className="impact-card">
                <h4>📍 Scan Rate</h4>
                <p className="impact-effect">{impacts.scanRate.effect}</p>
                <p className="impact-change">{impacts.scanRate.change}</p>
                <p className="impact-optimal">💡 {impacts.scanRate.optimal}</p>
              </div>

              <div className="impact-card">
                <h4>📊 CV Curve Area</h4>
                <p className="impact-effect">{impacts.integralArea.effect}</p>
                <p className="impact-change">{impacts.integralArea.change}</p>
                <p className="impact-optimal">💡 {impacts.integralArea.optimal}</p>
              </div>
            </div>

            <div className="impact-summary">
              <h4>Key Insights for Supercapacitor Design</h4>
              <ul>
                <li><strong>Energy Storage:</strong> Increase voltage window and CV integral area for maximum energy density</li>
                <li><strong>Lightweight Design:</strong> Minimize material mass to achieve high specific capacitance values</li>
                <li><strong>Performance Testing:</strong> Use lower scan rates to accurately measure true capacitive behavior</li>
                <li><strong>Material Selection:</strong> Choose materials that produce large CV curves (high integral area)</li>
                <li><strong>Trade-offs:</strong> Balance energy density (voltage) vs. power density (conductivity)</li>
              </ul>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default CapacitorMetrics;
