import React from 'react';
import PageHeader from '../components/app/PageHeader';
import SectionCard from '../components/app/SectionCard';
import ResultsSection from '../components/ResultsSection';
import { trainModels } from '../services/api';

const MODEL_OPTIONS = [
  { value: 'all', label: 'Compare All Models' },
  { value: 'ann', label: 'ANN' },
  { value: 'rf', label: 'Random Forest' },
  { value: 'xgb', label: 'XGBoost' },
];

function ModelTrainingPage(props) {
  const {
    selectedDataset,
    selectedModelType,
    setSelectedModelType,
    setLatestResults,
    trainingStatus,
    setTrainingStatus,
  } = props;

  const handleTrain = async () => {
    if (!selectedDataset) {
      setTrainingStatus({
        loading: false,
        success: false,
        error: 'Select a dataset before training.',
        message: '',
      });
      return;
    }

    setTrainingStatus({ loading: true, success: false, error: '', message: 'Training in progress...' });

    try {
      const results = await trainModels({
        datasetName: selectedDataset,
        modelType: selectedModelType,
      });

      setLatestResults(results);
      setTrainingStatus({
        loading: false,
        success: true,
        error: '',
        message: results?.message || 'Training completed successfully.',
      });
    } catch (error) {
      setTrainingStatus({
        loading: false,
        success: false,
        error: error?.message || 'Training failed.',
        message: '',
      });
    }
  };

  return (
    <div className="page-layout">
      <PageHeader
        eyebrow="Model Development"
        title="Model Training"
        description="Run a single model or compare all available regressors on the selected BiFe2O3 dataset."
        actions={
          <button type="button" className="primary-button" onClick={handleTrain}>
            Start Training
          </button>
        }
      />

      <div className="responsive-grid responsive-grid--two">
        <SectionCard title="Training Configuration" subtitle="Choose the dataset and model strategy.">
          <div className="form-stack">
            <div>
              <label className="form-label">Selected dataset</label>
              <div className="info-pill">{selectedDataset || 'No dataset selected'}</div>
            </div>
            <div>
              <label className="form-label" htmlFor="model-type-select">
                Model type
              </label>
              <select
                id="model-type-select"
                className="form-select"
                value={selectedModelType}
                onChange={(event) => setSelectedModelType(event.target.value)}
              >
                {MODEL_OPTIONS.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </div>
            <div className="status-box">
              <strong>Status:</strong> {trainingStatus.loading ? 'Running...' : trainingStatus.message || 'Idle'}
              {trainingStatus.error ? <p className="status-box__error">{trainingStatus.error}</p> : null}
            </div>
          </div>
        </SectionCard>

        <SectionCard title="Training Notes" subtitle="Expected outcomes from a successful training cycle.">
          <ul className="feature-list">
            <li>Compare R² and RMSE across ANN, Random Forest, and XGBoost.</li>
            <li>Persist the latest model results for dashboard review.</li>
            <li>Use the best model for later prediction tasks.</li>
          </ul>
        </SectionCard>
      </div>

      <SectionCard title="Training Results" subtitle="Latest model outputs and comparisons.">
        <ResultsSection results={props.latestResults} loading={trainingStatus.loading} error={trainingStatus.error} />
      </SectionCard>
    </div>
  );
}

export default ModelTrainingPage;