import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { datasetService } from '../services/api';
import '../styles/DatasetManager.css';

const formatBytes = (bytes = 0) => {
  if (!bytes) return '0 KB';
  const units = ['B', 'KB', 'MB', 'GB'];
  const index = Math.min(Math.floor(Math.log(bytes) / Math.log(1024)), units.length - 1);
  const value = bytes / 1024 ** index;
  return `${value.toFixed(index === 0 ? 0 : 2)} ${units[index]}`;
};

const DatasetManager = ({ selectedDataset, onSelectDataset }) => {
  const [datasets, setDatasets] = useState([]);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [preview, setPreview] = useState(null);
  const [showPreview, setShowPreview] = useState(false);
  const [error, setError] = useState('');

  const selectedDatasetInfo = useMemo(
    () => datasets.find((dataset) => dataset.name === selectedDataset) || null,
    [datasets, selectedDataset]
  );

  const loadDatasets = useCallback(async () => {
    try {
      setLoading(true);
      setError('');
      const response = await datasetService.getDatasets();
      setDatasets(response.datasets || []);
    } catch (loadError) {
      setError(loadError.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadDatasets();
  }, [loadDatasets]);

  const handleDatasetUpload = async (event) => {
    const file = event.target.files?.[0];
    if (!file) return;

    try {
      setUploading(true);
      setError('');
      const response = await datasetService.uploadDataset(file);
      await loadDatasets();

      const uploadedName = response?.dataset?.name || file.name;
      onSelectDataset(uploadedName);
    } catch (uploadError) {
      setError(uploadError.message);
    } finally {
      setUploading(false);
      event.target.value = '';
    }
  };

  const handlePreview = async (datasetName) => {
    try {
      setError('');
      const response = await datasetService.previewDataset(datasetName);
      setPreview(response.data);
      setShowPreview(true);
    } catch (previewError) {
      setError(previewError.message);
    }
  };

  const handleDelete = async (datasetName) => {
    try {
      setError('');
      await datasetService.deleteDataset(datasetName);
      if (datasetName === selectedDataset) {
        onSelectDataset('');
      }
      await loadDatasets();
    } catch (deleteError) {
      setError(deleteError.message);
    }
  };

  return (
    <section className="dataset-manager">
      <div className="dataset-manager__header">
        <div>
          <p className="section-kicker">Step 1</p>
          <h2>Training Dataset Management</h2>
          <p className="dataset-manager__description">
            Store multiple training datasets, switch between them anytime, and keep the testing file
            separate for evaluation only.
          </p>
        </div>

        <button type="button" className="dataset-manager__refresh" onClick={loadDatasets} disabled={loading}>
          {loading ? 'Refreshing...' : 'Refresh list'}
        </button>
      </div>

      <div className="dataset-manager__controls">
        <div className="dataset-manager__select-card">
          <label htmlFor="training-dataset-select" className="dataset-manager__label">
            Select Training Dataset
          </label>
          <select
            id="training-dataset-select"
            className="dataset-manager__select"
            value={selectedDataset}
            onChange={(event) => onSelectDataset(event.target.value)}
            disabled={loading || datasets.length === 0}
          >
            <option value="">Choose a stored dataset</option>
            {datasets.map((dataset) => (
              <option key={dataset.name} value={dataset.name}>
                {dataset.name}
              </option>
            ))}
          </select>
          <p className="dataset-manager__helper">
            Example: BiFeO3_dataset.xlsx, MnO2_dataset.xlsx, Graphene_dataset.xlsx
          </p>

          {selectedDatasetInfo && (
            <div className="dataset-manager__selected-meta">
              <span>{selectedDatasetInfo.rows} rows</span>
              <span>{selectedDatasetInfo.cols_count} columns</span>
              <span>Target: {selectedDatasetInfo.target_column || 'Auto-detect'}</span>
            </div>
          )}
        </div>

        <div className="dataset-manager__upload-card">
          <h3>Upload & Store New Training Dataset</h3>
          <label htmlFor="training-dataset-upload" className="dataset-manager__upload-label">
            {uploading ? 'Uploading dataset...' : 'Choose .xlsx or .csv file'}
          </label>
          <input
            id="training-dataset-upload"
            type="file"
            accept=".xlsx,.csv"
            onChange={handleDatasetUpload}
            disabled={uploading}
            className="dataset-manager__upload-input"
          />
          <p className="dataset-manager__helper">Stored datasets will appear in the dropdown automatically.</p>
        </div>
      </div>

      {error && <div className="dataset-manager__error">{error}</div>}

      <div className="dataset-manager__library">
        <div className="dataset-manager__library-header">
          <h3>Stored Dataset Library</h3>
          <span>{datasets.length} dataset(s)</span>
        </div>

        {loading ? (
          <div className="dataset-manager__empty">Loading available datasets...</div>
        ) : datasets.length === 0 ? (
          <div className="dataset-manager__empty">
            No stored training datasets yet. Upload a dataset to begin.
          </div>
        ) : (
          <div className="dataset-manager__list">
            {datasets.map((dataset) => (
              <article
                key={dataset.name}
                className={`dataset-card ${selectedDataset === dataset.name ? 'dataset-card--active' : ''}`}
              >
                <div className="dataset-card__content">
                  <div className="dataset-card__title-row">
                    <h4>{dataset.name}</h4>
                    {selectedDataset === dataset.name && <span className="dataset-card__badge">Selected</span>}
                  </div>

                  <div className="dataset-card__meta">
                    <span>{dataset.rows} rows</span>
                    <span>{dataset.cols_count} cols</span>
                    <span>{formatBytes(dataset.size)}</span>
                  </div>

                  <p className="dataset-card__target">
                    Target column: <strong>{dataset.target_column || 'Auto-detect on training'}</strong>
                  </p>

                  <p className="dataset-card__columns">
                    Columns: {dataset.columns?.length ? dataset.columns.join(', ') : 'Unavailable'}
                  </p>
                </div>

                <div className="dataset-card__actions">
                  <button type="button" className="btn btn-select" onClick={() => onSelectDataset(dataset.name)}>
                    Use for Training
                  </button>
                  <button type="button" className="btn btn-preview" onClick={() => handlePreview(dataset.name)}>
                    Preview
                  </button>
                  <button type="button" className="btn btn-delete" onClick={() => handleDelete(dataset.name)}>
                    Delete
                  </button>
                </div>
              </article>
            ))}
          </div>
        )}
      </div>

      {showPreview && preview && (
        <div className="modal-overlay" onClick={() => setShowPreview(false)}>
          <div className="modal-content" onClick={(event) => event.stopPropagation()}>
            <button type="button" className="close-btn" onClick={() => setShowPreview(false)}>
              ✕
            </button>

            <h3>{preview.name}</h3>
            <div className="preview-summary">
              <div className="preview-summary__item">
                <span>Rows</span>
                <strong>{preview.shape?.rows || 0}</strong>
              </div>
              <div className="preview-summary__item">
                <span>Columns</span>
                <strong>{preview.shape?.columns || 0}</strong>
              </div>
              <div className="preview-summary__item">
                <span>Numeric features</span>
                <strong>{preview.numeric_columns?.length || 0}</strong>
              </div>
            </div>

            <div className="preview-section">
              <h4>Sample Data</h4>
              <div className="table-wrapper">
                <table className="preview-table">
                  <thead>
                    <tr>
                      {preview.columns?.map((column) => (
                        <th key={column}>{column}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {preview.preview?.map((row, rowIndex) => (
                      <tr key={`row-${rowIndex}`}>
                        {preview.columns?.map((column) => (
                          <td key={`${rowIndex}-${column}`}>{String(row[column] ?? '')}</td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      )}
    </section>
  );
};

export default DatasetManager;
