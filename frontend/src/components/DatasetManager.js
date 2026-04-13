import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import '../styles/DatasetManager.css';

const DatasetManager = ({ onDatasetSelected }) => {
  const [datasets, setDatasets] = useState([]);
  const [selectedDataset, setSelectedDataset] = useState('');
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [showPreview, setShowPreview] = useState(false);
  const [preview, setPreview] = useState(null);

  const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

  // Load available datasets on mount
  const loadDatasets = useCallback(async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE}/datasets/list`);
      if (response.data.success) {
        setDatasets(response.data.datasets);
      }
    } catch (error) {
      console.error('Error loading datasets:', error);
    } finally {
      setLoading(false);
    }
  }, [API_BASE]);

  useEffect(() => {
    loadDatasets();
  }, [loadDatasets]);

  const handleUploadDataset = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    try {
      setUploading(true);
      const formData = new FormData();
      formData.append('file', file);

      const response = await axios.post(`${API_BASE}/datasets/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      if (response.data.success) {
        loadDatasets();
        alert(`Dataset ${response.data.filename} uploaded successfully!`);
      }
    } catch (error) {
      alert(`Upload failed: ${error.response?.data?.error || error.message}`);
    } finally {
      setUploading(false);
      e.target.value = '';
    }
  };

  const handlePreviewDataset = async (datasetName) => {
    try {
      const response = await axios.get(`${API_BASE}/datasets/preview/${datasetName}`);
      if (response.data.success) {
        setPreview(response.data.data);
        setShowPreview(true);
      }
    } catch (error) {
      console.error('Error loading preview:', error);
    }
  };

  const handleSelectDataset = (datasetName) => {
    setSelectedDataset(datasetName);
    onDatasetSelected(datasetName);
  };

  const handleDeleteDataset = async (datasetName) => {
    if (window.confirm(`Delete ${datasetName}?`)) {
      try {
        const response = await axios.delete(`${API_BASE}/datasets/delete/${datasetName}`);
        if (response.data.success) {
          loadDatasets();
          if (selectedDataset === datasetName) {
            setSelectedDataset('');
            onDatasetSelected('');
          }
        }
      } catch (error) {
        alert(`Delete failed: ${error.message}`);
      }
    }
  };

  return (
    <div className="dataset-manager">
      <h2>📊 Dataset Management</h2>

      {/* Upload Section */}
      <div className="upload-section">
        <h3>Upload Training Dataset</h3>
        <label htmlFor="dataset-upload" className="upload-label">
          {uploading ? 'Uploading...' : 'Click to upload or drag file'}
        </label>
        <input
          id="dataset-upload"
          type="file"
          accept=".xlsx,.csv"
          onChange={handleUploadDataset}
          disabled={uploading}
          className="upload-input"
        />
        <p className="upload-hint">Supported: .xlsx, .csv (Max 50MB)</p>
      </div>

      {/* Dataset Selection */}
      <div className="dataset-selection">
        <h3>Select Training Dataset</h3>
        {loading ? (
          <div className="loading">Loading datasets...</div>
        ) : datasets.length === 0 ? (
          <div className="no-datasets">No datasets available. Upload one to get started!</div>
        ) : (
          <div className="dataset-list">
            {datasets.map((dataset) => (
              <div
                key={dataset.name}
                className={`dataset-item ${selectedDataset === dataset.name ? 'selected' : ''}`}
              >
                <div className="dataset-info">
                  <h4>{dataset.name}</h4>
                  <p>{dataset.rows.toLocaleString()} rows × {dataset.cols_count} columns</p>
                  <p className="columns">Columns: {dataset.columns.join(', ')}</p>
                </div>
                <div className="dataset-actions">
                  <button
                    onClick={() => handleSelectDataset(dataset.name)}
                    className={`btn btn-select ${selectedDataset === dataset.name ? 'active' : ''}`}
                  >
                    {selectedDataset === dataset.name ? '✓ Selected' : 'Select'}
                  </button>
                  <button
                    onClick={() => handlePreviewDataset(dataset.name)}
                    className="btn btn-preview"
                  >
                    Preview
                  </button>
                  <button
                    onClick={() => handleDeleteDataset(dataset.name)}
                    className="btn btn-delete"
                  >
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Preview Modal */}
      {showPreview && preview && (
        <div className="modal-overlay" onClick={() => setShowPreview(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <button className="close-btn" onClick={() => setShowPreview(false)}>✕</button>
            <h3>Dataset Preview: {preview.name}</h3>
            
            <div className="preview-section">
              <h4>Statistics</h4>
              <p>Shape: {preview.shape.rows} rows × {preview.shape.columns} columns</p>
            </div>

            <div className="preview-section">
              <h4>Data Sample</h4>
              <div className="table-wrapper">
                <table className="preview-table">
                  <thead>
                    <tr>
                      {preview.columns.map((col) => (
                        <th key={col}>{col}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {preview.preview.map((row, idx) => (
                      <tr key={idx}>
                        {preview.columns.map((col) => (
                          <td key={`${idx}-${col}`}>{String(row[col]).substring(0, 20)}</td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            <button className="btn btn-primary" onClick={() => setShowPreview(false)}>
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default DatasetManager;
