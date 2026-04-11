import React, { useState } from 'react';
import FileUploader from './FileUploader';
import DatasetSelector from './DatasetSelector';
import '../styles/InferenceSection.css';

function InferenceSection() {
  const [selectedDataset, setSelectedDataset] = useState('');
  const [selectedModel, setSelectedModel] = useState('all');

  return (
    <section id="predict" className="inference">
      <div className="inference-container">
        <h2>🔬 Run Prediction</h2>
        <p className="section-subtitle">Upload your test dataset and select models to run analysis</p>
        
        <div className="inference-content">
          <div className="inference-panel">
            <h3>select Training Dataset</h3>
            <DatasetSelector onSelectDataset={setSelectedDataset} />
          </div>

          <div className="inference-panel">
            <h3>📤 Upload Test Data</h3>
            {selectedDataset ? (
              <FileUploader datasetName={selectedDataset} />
            ) : (
              <div className="placeholder">
                <p>Please select a training dataset first</p>
              </div>
            )}
          </div>

          <div className="inference-panel">
            <h3>🤖 Select Models</h3>
            <div className="model-selector">
              <label>
                <input 
                  type="radio" 
                  value="all" 
                  checked={selectedModel === 'all'}
                  onChange={(e) => setSelectedModel(e.target.value)}
                />
                <span>All Models (Recommended)</span>
              </label>
              <label>
                <input 
                  type="radio" 
                  value="xgb" 
                  checked={selectedModel === 'xgb'}
                  onChange={(e) => setSelectedModel(e.target.value)}
                />
                <span>XGBoost Only</span>
              </label>
              <label>
                <input 
                  type="radio" 
                  value="tensorflow" 
                  checked={selectedModel === 'tensorflow'}
                  onChange={(e) => setSelectedModel(e.target.value)}
                />
                <span>TensorFlow Only</span>
              </label>
              <label>
                <input 
                  type="radio" 
                  value="rf" 
                  checked={selectedModel === 'rf'}
                  onChange={(e) => setSelectedModel(e.target.value)}
                />
                <span>Random Forest Only</span>
              </label>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default InferenceSection;