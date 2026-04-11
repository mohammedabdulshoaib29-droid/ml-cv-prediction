import React, { useEffect, useState } from 'react';
import { datasetService } from '../services/api';
import '../styles/DatasetSelector.css';

const DatasetSelector = ({ onDatasetSelect, onUploadSuccess }) => {
  const [datasets, setDatasets] = useState([]);
  const [selectedDataset, setSelectedDataset] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [uploadFile, setUploadFile] = useState(null);
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    loadDatasets();
  }, []);

  const loadDatasets = async () => {
    try {
      setLoading(true);
      const data = await datasetService.getDatasets();
      setDatasets(data);
      setError('');
    } catch (err) {
      setError('Failed to load datasets');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDatasetSelect = (e) => {
    const datasetName = e.target.value;
    setSelectedDataset(datasetName);
    onDatasetSelect(datasetName);
  };

  const handleUploadChange = (e) => {
    setUploadFile(e.target.files[0]);
  };

  const handleUploadDataset = async () => {
    if (!uploadFile) {
      setError('Please select a file to upload');
      return;
    }

    try {
      setUploading(true);
      await datasetService.uploadDataset(uploadFile);
      setError('');
      setUploadFile(null);
      document.getElementById('file-input').value = '';
      await loadDatasets();
      onUploadSuccess();
    } catch (err) {
      setError('Failed to upload dataset');
      console.error(err);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="dataset-selector-container">
      <div className="selector-section">
        <h3>Training Dataset</h3>
        {loading ? (
          <p>Loading datasets...</p>
        ) : (
          <>
            <select
              value={selectedDataset}
              onChange={handleDatasetSelect}
              className="dataset-dropdown"
            >
              <option value="">-- Select Training Dataset --</option>
              {datasets.map((dataset) => (
                <option key={dataset.name} value={dataset.name}>
                  {dataset.name}
                </option>
              ))}
            </select>
            <p className="dataset-count">{datasets.length} datasets available</p>
          </>
        )}
      </div>

      <div className="upload-section">
        <h3>Upload New Training Dataset</h3>
        <div className="upload-group">
          <input
            id="file-input"
            type="file"
            accept=".xlsx,.xls,.csv"
            onChange={handleUploadChange}
            disabled={uploading}
          />
          <button
            onClick={handleUploadDataset}
            disabled={!uploadFile || uploading}
            className="upload-btn"
          >
            {uploading ? 'Uploading...' : 'Upload Dataset'}
          </button>
        </div>
        <p className="file-info">Supported formats: .xlsx, .xls, .csv</p>
      </div>

      {error && <div className="error-message">{error}</div>}
    </div>
  );
};

export default DatasetSelector;
