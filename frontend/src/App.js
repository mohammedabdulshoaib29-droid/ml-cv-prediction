import React, { useState } from 'react';
import DatasetSelector from './components/DatasetSelector';
import FileUploader from './components/FileUploader';
import ResultsDisplay from './components/ResultsDisplay';
import ModelComparison from './components/ModelComparison';
import { predictionService } from './services/api';
import './App.css';

function App() {
  const [selectedDataset, setSelectedDataset] = useState('');
  const [testFile, setTestFile] = useState(null);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [modelType, setModelType] = useState('all');

  const handleDatasetSelect = (dataset) => {
    setSelectedDataset(dataset);
  };

  const handleFileSelect = (file) => {
    setTestFile(file);
  };

  const handleUploadSuccess = () => {
    // Datasets list will be reloaded in DatasetSelector
  };

  const handlePredict = async () => {
    if (!selectedDataset) {
      setError('Please select a training dataset');
      return;
    }

    if (!testFile) {
      setError('Please upload a test dataset');
      return;
    }

    setLoading(true);
    setError('');
    
    try {
      const response = await predictionService.predict(
        selectedDataset,
        testFile,
        modelType
      );
      setResults(response);
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred during prediction');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>🤖 ML-Based CV Behavior Prediction</h1>
        <p>Advanced Machine Learning for CV Analysis and Behavior Forecasting</p>
      </header>

      <main className="app-main">
        <div className="content-wrapper">
          {/* Left Panel: Input Section */}
          <div className="input-section">
            <section className="panel">
              <DatasetSelector
                onDatasetSelect={handleDatasetSelect}
                onUploadSuccess={handleUploadSuccess}
              />
            </section>

            <section className="panel">
              <FileUploader
                onFileSelect={handleFileSelect}
                label="Upload Test Dataset"
              />
            </section>

            <section className="panel model-selection">
              <h3>Model Selection</h3>
              <div className="radio-group">
                <label>
                  <input
                    type="radio"
                    value="all"
                    checked={modelType === 'all'}
                    onChange={(e) => setModelType(e.target.value)}
                  />
                  All Models (ANN, RF, XGB)
                </label>
                <label>
                  <input
                    type="radio"
                    value="ann"
                    checked={modelType === 'ann'}
                    onChange={(e) => setModelType(e.target.value)}
                  />
                  Neural Network (ANN)
                </label>
                <label>
                  <input
                    type="radio"
                    value="rf"
                    checked={modelType === 'rf'}
                    onChange={(e) => setModelType(e.target.value)}
                  />
                  Random Forest (RF)
                </label>
                <label>
                  <input
                    type="radio"
                    value="xgb"
                    checked={modelType === 'xgb'}
                    onChange={(e) => setModelType(e.target.value)}
                  />
                  XGBoost (XGB)
                </label>
              </div>
            </section>

            <button
              onClick={handlePredict}
              disabled={!selectedDataset || !testFile || loading}
              className="predict-button"
            >
              {loading ? '⏳ Processing...' : '🚀 Run Prediction'}
            </button>

            {error && <div className="error-alert">{error}</div>}
          </div>

          {/* Right Panel: Output Section */}
          <div className="output-section">
            {results && (
              <>
                <section className="panel">
                  <ResultsDisplay results={results} loading={loading} error={error} />
                </section>
                <section className="panel">
                  <ModelComparison results={results} />
                </section>
              </>
            )}
            {!results && !loading && (
              <div className="placeholder">
                <p>📊 Results will appear here after running predictions</p>
              </div>
            )}
          </div>
        </div>
      </main>

      <footer className="app-footer">
        <p>ML Web App © 2024 | Powered by FastAPI & React</p>
      </footer>
    </div>
  );
}

export default App;
