import React, { useState } from 'react';
import FileUploader from './FileUploader';
import DatasetSelector from './DatasetSelector';
import ResultsDisplay from './ResultsDisplay';
import CapacitorMetrics from './CapacitorMetrics';
import { predictionService } from '../services/api';
import '../styles/InferenceSection.css';

function InferenceSection() {
  const [selectedDataset, setSelectedDataset] = useState('');
  const [selectedModel, setSelectedModel] = useState('all');
  const [testFile, setTestFile] = useState(null);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleDatasetSelect = (dataset) => {
    setSelectedDataset(dataset);
  };

  const handleFileSelect = (file) => {
    setTestFile(file);
  };

  const handlePredict = async () => {
    if (!selectedDataset) {
      setError('⚠️ Please select a training dataset');
      return;
    }

    if (!testFile) {
      setError('⚠️ Please upload a test file');
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
      
      const response = await predictionService.predict(
        selectedDataset,
        testFile,
        selectedModel
      );
      
      console.log('Prediction successful:', response);
      setResults(response);
    } catch (err) {
      const errorMessage = err.message || (err.response?.data?.detail) || 'An error occurred during prediction';
      console.error('Prediction error:', errorMessage);
      setError(`❌ ${errorMessage}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section id="predict" className="inference">
      <div className="inference-container">
        <h2>🔬 Run Prediction</h2>
        <p className="section-subtitle">Upload your test dataset and select models to run analysis</p>
        
        <div className="inference-content">
          <div className="inference-panel">
            <h3>📊 Select Training Dataset</h3>
            <DatasetSelector onDatasetSelect={handleDatasetSelect} onUploadSuccess={() => {}} />
          </div>

          <div className="inference-panel">
            <h3>📤 Upload Test Data</h3>
            {selectedDataset ? (
              <FileUploader onFileSelect={handleFileSelect} label="Upload Test Dataset" />
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
                  value="tnn" 
                  checked={selectedModel === 'tnn'}
                  onChange={(e) => setSelectedModel(e.target.value)}
                />
                <span>Tensor Neural Network (TNN) Only</span>
              </label>
              <label>
                <input 
                  type="radio" 
                  value="ann" 
                  checked={selectedModel === 'ann'}
                  onChange={(e) => setSelectedModel(e.target.value)}
                />
                <span>Artificial Neural Network (ANN) Only</span>
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

          <button 
            onClick={handlePredict}
            disabled={!selectedDataset || !testFile || loading}
            className="submit-button"
          >
            {loading ? '⏳ Processing...' : '🚀 Run Prediction'}
          </button>

          {error && <div className="error-message">{error}</div>}

          {results && (
            <div className="results-container">
              <h3>📈 Prediction Results</h3>
              <ResultsDisplay results={results} loading={loading} error={error} />
              <CapacitorMetrics results={results} />
            </div>
          )}
        </div>
      </div>
    </section>
  );
}

export default InferenceSection;
