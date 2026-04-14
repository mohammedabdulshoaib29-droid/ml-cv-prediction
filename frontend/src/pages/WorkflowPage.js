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

  const modelCards = [
    {
      title: 'ANN',
      description: 'Good for learning nonlinear relationships in electrochemical and materials datasets.',
    },
    {
      title: 'Random Forest',
      description: 'Useful for stable tabular predictions and feature-driven comparisons.',
    },
    {
      title: 'XGBoost',
      description: 'Strong gradient-boosted baseline for high-quality regression performance.',
    },
  ];

  const keyHighlights = [
    'Single-page workflow for dataset upload, model training, and prediction.',
    'Supports stored CV training datasets and separate test files for inference.',
    'Compares ANN, Random Forest, and XGBoost in one application.',
    'Surfaces latest metrics, model comparison, and prediction outputs in one place.',
  ];

  const metricsInfo = [
    { label: 'Target output', value: 'Capacitance prediction' },
    { label: 'Supported files', value: 'CV `.csv` and `.xlsx` datasets' },
    { label: 'Training mode', value: 'Internal train/test split' },
    { label: 'Prediction mode', value: 'Stored train data + uploaded test file' },
  ];

  return (
    <div className="page-layout workflow-page">
      <PageHeader
        eyebrow="ML Prediction Workspace"
        title="Train capacitance models and run predictions from one guided page"
        description="This workspace is designed for your capacitor materials ML workflow. Upload or select cyclic voltammetry (CV) training data, compare ANN, Random Forest, and XGBoost, then run predictions on a separate test dataset and review the results immediately."
      />

      <div className="workflow-hero-grid">
        <SectionCard
          title="Platform overview"
          subtitle="A clearer introduction to what this website does and how to use it."
        >
          <div className="workflow-overview">
            <div className="workflow-overview__intro">
              <h3>What this system does</h3>
              <p>
                This application predicts capacitance-related outcomes from uploaded cyclic
                voltammetry (CV) and related tabular datasets. It is built for an easy
                end-to-end workflow: dataset selection, model training, inference on test data,
                and result review.
              </p>
            </div>

            <div className="workflow-overview__grid">
              <div className="workflow-overview__card">
                <h4>Core models</h4>
                <p>ANN, Random Forest, and XGBoost are available for training and comparison.</p>
              </div>
              <div className="workflow-overview__card">
                <h4>Main inputs</h4>
                <p>CV training datasets and test datasets in `.csv` or `.xlsx` format.</p>
              </div>
              <div className="workflow-overview__card">
                <h4>Main output</h4>
                <p>Predicted capacitance values, model comparison metrics, and best-model summary.</p>
              </div>
            </div>
          </div>
        </SectionCard>

        <SectionCard
          title="Quick summary"
          subtitle="A snapshot of the current workflow state."
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

      <div className="workflow-info-grid">
        <SectionCard
          title="Workflow highlights"
          subtitle="Why this interface is structured this way."
        >
          <ul className="workflow-bullet-list">
            {keyHighlights.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </SectionCard>

        <SectionCard
          title="Model architecture in this website"
          subtitle="A simple explanation of the prediction stack used here."
        >
          <div className="workflow-model-grid">
            {modelCards.map((model) => (
              <article key={model.title} className="workflow-model-card">
                <h4>{model.title}</h4>
                <p>{model.description}</p>
              </article>
            ))}
          </div>
        </SectionCard>

        <SectionCard
          title="Inputs, outputs, and training setup"
          subtitle="Information that helps users understand what to prepare."
        >
          <div className="workflow-metrics-grid">
            {metricsInfo.map((item) => (
              <div key={item.label} className="workflow-metric-item">
                <span>{item.label}</span>
                <strong>{item.value}</strong>
              </div>
            ))}
          </div>
        </SectionCard>
      </div>

      <div className="workflow-step-grid">
        <SectionCard
          title="Step 1: Choose your CV training dataset"
          subtitle="Upload a new file or select one you already stored."
        >
          <p className="workflow-step-label">Step 1</p>
          <p className="supporting-text">
            Start by picking the cyclic voltammetry dataset you want to use for model training.
            This becomes the main dataset for the rest of the workflow.
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
