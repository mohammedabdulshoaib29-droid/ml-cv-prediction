import React, { useEffect, useMemo, useState } from 'react';
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  ResponsiveContainer,
  Scatter,
  ScatterChart,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';

const MODEL_ORDER = ['ANN', 'RandomForest', 'XGBoost'];
const MODEL_LABELS = {
  ANN: 'ANN',
  RandomForest: 'Random Forest',
  XGBoost: 'XGBoost',
};
const MODEL_COLORS = {
  ANN: '#4f46e5',
  RandomForest: '#0f766e',
  XGBoost: '#ea580c',
};

const formatMetric = (value, digits = 4) => {
  if (value === null || value === undefined || Number.isNaN(Number(value))) {
    return '-';
  }
  return Number(value).toFixed(digits);
};

function MetricCard({ label, value, unit }) {
  return (
    <div className="metric-chip">
      <span>{label}</span>
      <strong>
        {value}
        {unit ? ` ${unit}` : ''}
      </strong>
    </div>
  );
}

function ModelPerformanceCard({ modelKey, modelData, isActive, onActivate }) {
  const metrics = modelData?.metrics || {};
  const successful = modelData?.success;

  return (
    <button
      type="button"
      className={`model-card ${isActive ? 'model-card-active' : ''}`}
      onClick={() => onActivate(modelKey)}
    >
      <div className="model-card-header">
        <div>
          <p className="model-name">{MODEL_LABELS[modelKey]}</p>
          <span className={`status-dot ${successful ? 'status-dot-success' : 'status-dot-error'}`}>
            {successful ? 'Evaluated' : 'Failed'}
          </span>
        </div>
        <div className="model-color-indicator" style={{ backgroundColor: MODEL_COLORS[modelKey] }} />
      </div>

      <div className="model-card-grid">
        <MetricCard label="R²" value={formatMetric(metrics.r2_score)} />
        <MetricCard label="RMSE" value={formatMetric(metrics.rmse)} />
        <MetricCard label="Predicted Mean" value={formatMetric(metrics.predicted_capacitance_mean, 2)} unit="F/g" />
      </div>
    </button>
  );
}

function PlotBlock({ title, description, image, children }) {
  return (
    <div className="chart-card">
      <div className="card-heading">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>

      {image ? (
        <div className="plot-image-wrap">
          <img src={`data:image/png;base64,${image}`} alt={title} className="plot-image" />
        </div>
      ) : (
        children
      )}
    </div>
  );
}

function ResultsSection({ results, hasResults }) {
  const [activeModel, setActiveModel] = useState('ANN');

  const availableModels = useMemo(() => {
    if (!results?.models) {
      return [];
    }

    return MODEL_ORDER.filter((key) => results.models[key]?.success);
  }, [results]);

  useEffect(() => {
    if (availableModels.length && !availableModels.includes(activeModel)) {
      setActiveModel(availableModels[0]);
    }
  }, [activeModel, availableModels]);

  const currentModelKey = availableModels.includes(activeModel) ? activeModel : availableModels[0];
  const currentModel = currentModelKey ? results?.models?.[currentModelKey] : null;
  const comparisonData = results?.comparison || [];
  const predictionTable = results?.prediction_table || [];
  const metadata = results?.metadata || {};
  const modelErrors = results?.model_errors || [];

  const actualVsPredicted = currentModel?.plots?.actual_vs_predicted || [];
  const errorDistribution = (currentModel?.plots?.error_distribution || []).map((item, index) => ({
    index: index + 1,
    ...item,
  }));
  const plotImages = currentModel?.plots?.images || {};

  if (!hasResults) {
    return (
      <div className="dashboard-section">
        <div className="section-header">
          <div>
            <p className="section-kicker">Step 3</p>
            <h2>Model Results Dashboard</h2>
            <p className="section-text">
              Run a prediction to unlock model comparison, metrics, predicted capacitance values, and plots.
            </p>
          </div>
        </div>
        <div className="empty-dashboard">
          <h3>No results yet</h3>
          <p>Select a stored training dataset, upload a separate testing dataset, and start evaluation.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-section">
      <div className="section-header">
        <div>
          <p className="section-kicker">Step 3</p>
          <h2>Model Results Dashboard</h2>
          <p className="section-text">
            Compare ANN, Random Forest, and XGBoost performance on the uploaded testing dataset.
          </p>
        </div>
      </div>

      <div className="metadata-bar">
        <div className="metadata-item">
          <span>Training dataset</span>
          <strong>{metadata.selected_train_dataset || '-'}</strong>
        </div>
        <div className="metadata-item">
          <span>Testing dataset</span>
          <strong>{metadata.uploaded_test_filename || '-'}</strong>
        </div>
        <div className="metadata-item">
          <span>Target column</span>
          <strong>{metadata.target_column || '-'}</strong>
        </div>
        <div className="metadata-item">
          <span>Features used</span>
          <strong>{metadata.feature_columns?.length || 0}</strong>
        </div>
      </div>

      {!!modelErrors.length && (
        <div className="empty-state">
          {modelErrors.map((item) => (
            <p key={item.model}>
              <strong>{item.model}:</strong> {item.error}
            </p>
          ))}
        </div>
      )}

      <div className="model-cards-grid">
        {MODEL_ORDER.map((modelKey) => (
          <ModelPerformanceCard
            key={modelKey}
            modelKey={modelKey}
            modelData={results?.models?.[modelKey]}
            isActive={currentModelKey === modelKey}
            onActivate={setActiveModel}
          />
        ))}
      </div>

      {currentModel && (
        <>
          <div className="chart-card">
            <div className="card-heading">
              <h3>{MODEL_LABELS[currentModelKey]} detailed metrics</h3>
              <p>Model performance and predicted capacitance range.</p>
            </div>

            <div className="model-card-grid">
              <MetricCard label="R² Score" value={formatMetric(currentModel.metrics?.r2_score)} />
              <MetricCard label="RMSE" value={formatMetric(currentModel.metrics?.rmse)} />
              <MetricCard label="MAE" value={formatMetric(currentModel.metrics?.mae)} />
              <MetricCard
                label="Predicted Mean"
                value={formatMetric(currentModel.metrics?.predicted_capacitance_mean, 2)}
                unit="F/g"
              />
              <MetricCard
                label="Predicted Min"
                value={formatMetric(currentModel.metrics?.predicted_capacitance_min, 2)}
                unit="F/g"
              />
              <MetricCard
                label="Predicted Max"
                value={formatMetric(currentModel.metrics?.predicted_capacitance_max, 2)}
                unit="F/g"
              />
              <MetricCard label="Training Samples" value={currentModel.metrics?.train_samples ?? '-'} />
              <MetricCard label="Testing Samples" value={currentModel.metrics?.test_samples ?? '-'} />
            </div>
          </div>

          <div className="charts-grid">
            <div className="chart-card">
              <div className="card-heading">
                <h3>Model comparison bar chart</h3>
                <p>Higher R² and lower RMSE indicate better generalization.</p>
              </div>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={comparisonData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="model" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="r2_score" name="R²">
                    {comparisonData.map((entry) => (
                      <Cell key={`${entry.model}-r2`} fill={MODEL_COLORS[entry.model] || '#4f46e5'} />
                    ))}
                  </Bar>
                  <Bar dataKey="rmse" name="RMSE" fill="#f59e0b" />
                </BarChart>
              </ResponsiveContainer>
            </div>

            <PlotBlock
              title="Actual vs Predicted values"
              description={`Parity view for ${MODEL_LABELS[currentModelKey]}.`}
              image={plotImages.actual_vs_predicted}
            >
              <ResponsiveContainer width="100%" height={300}>
                <ScatterChart>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="actual" name="Actual" />
                  <YAxis dataKey="predicted" name="Predicted" />
                  <Tooltip cursor={{ strokeDasharray: '3 3' }} />
                  <Scatter data={actualVsPredicted} fill={MODEL_COLORS[currentModelKey]} />
                </ScatterChart>
              </ResponsiveContainer>
            </PlotBlock>

            <PlotBlock
              title="Error distribution"
              description="Residual spread for the selected model."
              image={plotImages.error_distribution}
            >
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={errorDistribution}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="index" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="error" fill={MODEL_COLORS[currentModelKey]} />
                </BarChart>
              </ResponsiveContainer>
            </PlotBlock>
          </div>
        </>
      )}

      <div className="prediction-table-card">
        <div className="card-heading">
          <h3>Predicted capacitance table</h3>
          <p>Actual values and per-model predictions returned from backend evaluation.</p>
        </div>

        {predictionTable.length ? (
          <div className="table-wrap">
            <table className="data-table">
              <thead>
                <tr>
                  {Object.keys(predictionTable[0]).map((column) => (
                    <th key={column}>{column}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {predictionTable.slice(0, 50).map((row, index) => (
                  <tr key={`prediction-row-${index}`}>
                    {Object.keys(predictionTable[0]).map((column) => (
                      <td key={`${index}-${column}`}>{String(row[column] ?? '')}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p className="empty-state">No prediction rows were returned.</p>
        )}
      </div>
    </div>
  );
}

export default ResultsSection;
