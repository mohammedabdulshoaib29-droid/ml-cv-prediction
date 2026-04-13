import React, { useState } from 'react';
import axios from 'axios';
import '../styles/ModelTrainer.css';
import ModelComparison from './ModelComparison';

const ModelTrainer = ({ selectedDataset }) => {
  const [testFile, setTestFile] = useState(null);
  const [training, setTraining] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState('');

  const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

  const handleTestFileChange = (e) => {
    setTestFile(e.target.files[0]);
    setError('');
  };

  const handleTrainModels = async () => {
    try {
      setError('');
      if (!selectedDataset) {
        setError('Please select a training dataset first');
        return;
      }
      if (!testFile) {
        setError('Please upload a test dataset');
        return;
      }

      setTraining(true);
      
      const formData = new FormData();
      formData.append('train_dataset', selectedDataset);
      formData.append('test_file', testFile);

      const response = await axios.post(`${API_BASE}/models/train`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        timeout: 600000 // 10 minute timeout
      });

      if (response.data.success) {
        setResults(response.data);
      } else {
        setError(response.data.error || 'Training failed');
      }
    } catch (err) {
      console.error('Training error:', err);
      setError(err.response?.data?.error || err.message);
    } finally {
      setTraining(false);
    }
  };

  return (
    <div className="model-trainer">
      <h2>🤖 Model Training</h2>

      {/* Test Dataset Upload */}
      <div className="test-upload-section">
        <h3>Step 1: Upload Test Dataset</h3>
        <label htmlFor="test-file-upload" className="file-label">
          {testFile ? testFile.name : 'Click to upload test dataset'}
        </label>
        <input
          id="test-file-upload"
          type="file"
          accept=".xlsx,.csv"
          onChange={handleTestFileChange}
          disabled={training}
          className="file-input"
        />
      </div>

      {/* Training Status */}
      <div className="training-status">
        {training && (
          <div className="loading-spinner">
            <div className="spinner"></div>
            <p>Training all 3 models... This may take a few minutes.</p>
            <div className="progress-bar">
              <div className="progress-fill"></div>
            </div>
          </div>
        )}

        {error && (
          <div className="error-message">
            ⚠️ {error}
          </div>
        )}
      </div>

      {/* Train Button */}
      <button
        onClick={handleTrainModels}
        disabled={training || !selectedDataset || !testFile}
        className={`btn btn-train ${!selectedDataset || !testFile ? 'disabled' : ''}`}
      >
        {training ? 'Training...' : 'Start Training'}
      </button>

      {/* Results Display */}
      {results && (
        <div className="results-container">
          <ModelComparison results={results} />
        </div>
      )}
    </div>
  );
};

export default ModelTrainer;
