import React, { useState } from 'react';
import { predictionService } from '../services/api';
import '../styles/PredictionEngine.css';

const PredictionEngine = ({ selectedDataset, onPredictionComplete }) => {
  const [testFile, setTestFile] = useState(null);
  const [selectedModel, setSelectedModel] = useState('all');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    const files = e.dataTransfer.files;
    if (files && files[0]) {
      const file = files[0];
      if (file.name.endsWith('.xlsx') || file.name.endsWith('.csv')) {
        setTestFile(file);
        setError('');
      } else {
        setError('⚠️ Please upload .xlsx or .csv files only');
      }
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (file.name.endsWith('.xlsx') || file.name.endsWith('.csv')) {
        setTestFile(file);
        setError('');
      } else {
        setError('⚠️ Please upload .xlsx or .csv files only');
      }
    }
  };

  const handleStartPrediction = async () => {
    if (!selectedDataset) {
      setError('⚠️ Please select a training dataset from Dataset Management first');
      return;
    }

    if (!testFile) {
      setError('⚠️ Please upload a test dataset');
      return;
    }

    setLoading(true);
    setError('');

    try {
      console.log('Starting prediction with:', {
        dataset: selectedDataset,
        testFile: testFile.name,
        model: selectedModel
      });

      const results = await predictionService.predict(
        selectedDataset,
        testFile,
        selectedModel
      );

      console.log('Prediction successful:', results);
      onPredictionComplete(results);
    } catch (err) {
      const errorMessage = err.message || 'An error occurred during prediction';
      console.error('Prediction error:', errorMessage);
      setError(`❌ ${errorMessage}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="prediction-engine">
      <div className="prediction-container">
        <h2>🤖 Run Prediction</h2>
        <p className="section-subtitle">Upload your test dataset and select models to run predictions</p>

        <div className="prediction-content">
          {/* Step 1: Upload Test Dataset */}
          <div className="prediction-step">
            <h3>Step 1: Upload Test Dataset</h3>
            <div
              className={`file-upload-area ${dragActive ? 'active' : ''} ${testFile ? 'has-file' : ''}`}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
            >
              <input
                type="file"
                accept=".xlsx,.csv"
                onChange={handleFileChange}
                className="file-input"
                id="test-file-input"
              />
              <label htmlFor="test-file-input" className="upload-label">
                {testFile ? (
                  <div className="file-selected">
                    <span className="file-icon">✓</span>
                    <span className="file-name">{testFile.name}</span>
                    <span className="file-size">({(testFile.size / 1024).toFixed(2)} KB)</span>
                  </div>
                ) : (
                  <div className="upload-prompt">
                    <span className="upload-icon">📁</span>
                    <span className="upload-text">Drag & drop or click to upload</span>
                    <span className="upload-hint">Supported: .xlsx, .csv (Max 50MB)</span>
                  </div>
                )}
              </label>
            </div>
          </div>

          {/* Step 2: Select Model */}
          <div className="prediction-step">
            <h3>Step 2: Select Model</h3>
            <div className="model-selector">
              <label className="model-option">
                <input
                  type="radio"
                  value="all"
                  checked={selectedModel === 'all'}
                  onChange={(e) => setSelectedModel(e.target.value)}
                />
                <span className="option-label">All Models (Recommended)</span>
                <span className="option-desc">Run predictions with ANN, Random Forest, and XGBoost</span>
              </label>
              <label className="model-option">
                <input
                  type="radio"
                  value="ann"
                  checked={selectedModel === 'ann'}
                  onChange={(e) => setSelectedModel(e.target.value)}
                />
                <span className="option-label">Artificial Neural Network (ANN) Only</span>
                <span className="option-desc">Deep learning model for complex patterns</span>
              </label>
              <label className="model-option">
                <input
                  type="radio"
                  value="rf"
                  checked={selectedModel === 'rf'}
                  onChange={(e) => setSelectedModel(e.target.value)}
                />
                <span className="option-label">Random Forest (RF) Only</span>
                <span className="option-desc">Ensemble learning model</span>
              </label>
              <label className="model-option">
                <input
                  type="radio"
                  value="xgb"
                  checked={selectedModel === 'xgb'}
                  onChange={(e) => setSelectedModel(e.target.value)}
                />
                <span className="option-label">XGBoost (XGB) Only</span>
                <span className="option-desc">Gradient boosting for optimal performance</span>
              </label>
            </div>
          </div>

          {/* Error Message */}
          {error && <div className="error-message">{error}</div>}

          {/* Start Prediction Button */}
          <button
            onClick={handleStartPrediction}
            disabled={!selectedDataset || !testFile || loading}
            className={`start-prediction-btn ${loading ? 'loading' : ''}`}
          >
            {loading ? (
              <>
                <span className="spinner"></span>
                Processing...
              </>
            ) : (
              <>
                <span className="play-icon">▶</span>
                Start Prediction
              </>
            )}
          </button>
        </div>
      </div>
    </section>
  );
};

export default PredictionEngine;
