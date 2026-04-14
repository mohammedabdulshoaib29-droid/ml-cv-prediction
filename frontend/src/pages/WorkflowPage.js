import React from 'react';
import { trainModels } from '../services/api';
import DatasetManager from '../components/DatasetManager';
import PredictionEngine from '../components/PredictionEngine';
import ResultsSection from '../components/ResultsSection';
import PageHeader from '../components/app/PageHeader';
import SectionCard from '../components/app/SectionCard';
import '../styles/workflow-page.css';

const MODEL_OPTIONS = [
  { value: 'all', label: 'Compare All Models' },
  { value: 'ann', label: 'ANN' },
  { value: 'rf', label: 'Random Forest' },
  { value: 'xgb', label: 'XGBoost' },
];

const getModelLabel = (modelType) =>
  MODEL_OPTIONS.find((option) => option.value === modelType)?.label || 'Compare All Models';

const getStatusToneClass = (status) => {
  if (status?.error) {
    return 'workflow-inline-status workflow-inline-status--error';
  }

  if (status?.success) {
    return 'workflow-inline-status workflow-inline-status--success';
  }

  return 'workflow-inline-status';
};

const getStatusText = (status, idleText) => {
  if (status?.loading) {
    return status.message || 'In progress...';
  }

  if (status?.error) {
    return status.error;
  }

  if (status?.success) {
    return status.message || 'Completed successfully.';
  }

  return idleText;
};

function WorkflowPage({
  selectedDataset,
  setSelectedDataset,
  selectedModelType,
  setSelectedModelType,
  latestResults,
  setLatestResults,
  trainingStatus,
  setTrainingStatus,
  predictionStatus,
  setPredictionStatus,
}) {
  const handleTrain = async () => {
    if (!selectedDataset) {
      setTrainingStatus({
        loading: false,
        success: false,
        error: 'Please choose a training dataset before starting model training.',
        message: '',
      });
      return;
    }

    setTrainingStatus({
      loading: true,
      success: false,
      error: '',
      message: 'Training models with your selected dataset...',
    });

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

  const summaryItems = [
    {
      label: 'Selected dataset',
      value: selectedDataset || 'No dataset selected yet',
    },
    {
      label: 'Model choice',
      value: getModelLabel(selectedModelType),
    },
    {
      label: 'Training status',
      value: getStatusText(trainingStatus, 'Not started'),
      toneClass: getStatusToneClass(trainingStatus),
    },
    {
      label: 'Prediction status',
      value: getStatusText(predictionStatus, 'Not started'),
      toneClass: getStatusToneClass(predictionStatus),
    },
  ];

  return (
    <div className="page-layout workflow-page">
      <PageHeader
        eyebrow="Guided Workflow"
        title="Upload data, train models, and predict results on one simple page"
        description="Follow these four steps from top to bottom. First choose your training dataset, then train a model, upload a test file for prediction, and review the latest results below."
      />

      <div className="workflow-hero-grid">
        <SectionCard
          title="Quick summary"
          subtitle="A simple snapshot of where your workflow stands right now."
        >
          <div className="workflow-summary">
            <div className="workflow-summary__grid">
              {summaryItems.map((item) => (
                <div key={item.label} className="workflow-summary__item">
                  <span>{item.label}</span>
                  <strong className={item.toneClass}>{item.value}</strong>
                </div>
              ))}
            </div>
          </div>
        </SectionCard>
      </div>

      <div className="workflow-step-grid">
        <SectionCard
          title="Step 1: Choose your training dataset"
          subtitle="Upload a new file or select one you already stored."
        >
          <p className="workflow-step-label">Step 1</p>
          <p className="supporting-text">
            Start by picking the dataset you want to use for model training. This becomes the main
            dataset for the rest of the workflow.
          </p>
          <DatasetManager
            selectedDataset={selectedDataset}
            onSelectDataset={setSelectedDataset}
          />
        </SectionCard>

        <SectionCard
          title="Step 2: Train a model"
          subtitle="Choose a model option and start training with one click."
        >
          <p className="workflow-step-label">Step 2</p>
          <p className="supporting-text">
            Select whether you want to compare all available models or run a specific model type.
          </p>

          <div className="responsive-grid responsive-grid--two">
            <label className="form-field">
              <span className="form-field__label">Training dataset</span>
              <input
                className="form-input"
                value={selectedDataset || 'No dataset selected'}
                readOnly
              />
            </label>

            <label className="form-field">
              <span className="form-field__label">Model type</span>
              <select
                className="form-input"
                value={selectedModelType}
                onChange={(event) => setSelectedModelType(event.target.value)}
              >
                {MODEL_OPTIONS.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </label>
          </div>

          <div className="workflow-train-actions">
            <button
              type="button"
              className="primary-button"
              onClick={handleTrain}
              disabled={!selectedDataset || trainingStatus.loading}
            >
              {trainingStatus.loading ? 'Training...' : 'Train Model'}
            </button>
            <span className={getStatusToneClass(trainingStatus)}>
              {getStatusText(trainingStatus, 'Training has not started yet.')}
            </span>
          </div>
        </SectionCard>

        <SectionCard
          title="Step 3: Upload test data and run prediction"
          subtitle="Use a separate test file to generate predicted results."
        >
          <p className="workflow-step-label">Step 3</p>
          <p className="supporting-text">
            After training, upload your test dataset and run prediction. Your latest prediction
            status will update automatically.
          </p>
          <PredictionEngine
            selectedDataset={selectedDataset}
            onPredictionComplete={(results) => {
              setLatestResults(results);
              setPredictionStatus({
                loading: false,
                success: true,
                error: '',
                message: results?.message || 'Prediction completed successfully.',
              });
            }}
          />
          {!predictionStatus.success && (predictionStatus.loading || predictionStatus.error || predictionStatus.message) ? (
            <p className={getStatusToneClass(predictionStatus)}>
              {getStatusText(predictionStatus, 'Prediction has not started yet.')}
            </p>
          ) : null}
        </SectionCard>

        <SectionCard
          title="Step 4: Review the latest results"
          subtitle="See the newest metrics, comparisons, and prediction outputs."
        >
          <p className="workflow-step-label">Step 4</p>
          <p className="supporting-text">
            Once training or prediction finishes, the latest available results will appear here.
          </p>
          <ResultsSection results={latestResults} hasResults={Boolean(latestResults)} />
        </SectionCard>
      </div>
    </div>
  );
}

export default WorkflowPage;