import React, { useMemo } from 'react';
import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import '../styles/ResultsSection.css';

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

const MODEL_ALIASES = {
  ANN: ['ANN', 'ann'],
  RandomForest: ['RandomForest', 'Random Forest', 'randomforest', 'random_forest', 'RF'],
  XGBoost: ['XGBoost', 'xgboost', 'xgb', 'XGBoostRegressor'],
};

const isValidNumber = (value) => typeof value === 'number' && Number.isFinite(value);

const toNumber = (value) => {
  if (value === null || value === undefined || value === '') {
    return null;
  }

  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : null;
};

const firstDefined = (...values) => {
  for (const value of values) {
    if (value !== null && value !== undefined && value !== '') {
      return value;
    }
  }
  return null;
};

const getModelEntry = (source, modelKey) => {
  if (!source || typeof source !== 'object') {
    return null;
  }

  const aliases = MODEL_ALIASES[modelKey] || [modelKey];
  for (const alias of aliases) {
    if (Object.prototype.hasOwnProperty.call(source, alias)) {
      return source[alias];
    }
  }

  return null;
};

const findComparisonEntry = (comparison, modelKey) => {
  if (!Array.isArray(comparison)) {
    return null;
  }

  const aliases = MODEL_ALIASES[modelKey] || [modelKey];
  return (
    comparison.find((item) => {
      const modelName = item?.model || item?.name || item?.Model;
      return aliases.includes(modelName);
    }) || null
  );
};

const formatMetric = (value, digits = 3) => {
  const numeric = toNumber(value);
  return isValidNumber(numeric) ? numeric.toFixed(digits) : '—';
};

const formatCapacitance = (value) => {
  const numeric = toNumber(value);
  return isValidNumber(numeric) ? `${numeric.toFixed(2)} F/g` : '—';
};

const formatConcentration = (value) => {
  const numeric = toNumber(value);
  return isValidNumber(numeric) ? `${numeric.toFixed(3)} M` : '—';
};

const normalizeGraphPoints = (graphData) => {
  if (!graphData) {
    return [];
  }

  if (Array.isArray(graphData)) {
    return graphData
      .map((point, index) => {
        const concentration = toNumber(
          firstDefined(point?.concentration, point?.x, point?.feature, point?.index, index + 1)
        );
        const capacitance = toNumber(
          firstDefined(point?.predicted, point?.capacitance, point?.y, point?.value)
        );

        if (!isValidNumber(concentration) || !isValidNumber(capacitance)) {
          return null;
        }

        return { concentration, capacitance };
      })
      .filter(Boolean);
  }

  if (Array.isArray(graphData?.capacitance_series)) {
    return normalizeGraphPoints(graphData.capacitance_series);
  }

  const concentrations = Array.isArray(graphData?.concentration)
    ? graphData.concentration
    : Array.isArray(graphData?.concentrations)
    ? graphData.concentrations
    : Array.isArray(graphData?.x)
    ? graphData.x
    : null;

  const predicted = Array.isArray(graphData?.predicted)
    ? graphData.predicted
    : Array.isArray(graphData?.capacitance)
    ? graphData.capacitance
    : Array.isArray(graphData?.y)
    ? graphData.y
    : null;

  if (concentrations && predicted) {
    return concentrations
      .map((concentrationValue, index) => {
        const concentration = toNumber(concentrationValue);
        const capacitance = toNumber(predicted[index]);

        if (!isValidNumber(concentration) || !isValidNumber(capacitance)) {
          return null;
        }

        return { concentration, capacitance };
      })
      .filter(Boolean);
  }

  return [];
};

const getPredictionRows = (results) => {
  if (Array.isArray(results?.table)) {
    return results.table;
  }

  if (Array.isArray(results?.prediction_table)) {
    return results.prediction_table;
  }

  return [];
};

const getMetadata = (results) => results?.metadata || {};

const getBestModelName = (bestModelValue) => {
  if (!bestModelValue) {
    return null;
  }

  if (typeof bestModelValue === 'string') {
    return bestModelValue;
  }

  if (typeof bestModelValue === 'object') {
    return firstDefined(bestModelValue.name, bestModelValue.model, bestModelValue.label);
  }

  return null;
};

const buildModelSummary = (results, modelKey) => {
  const performance = getModelEntry(results?.performance, modelKey) || {};
  const modelResult = getModelEntry(results?.models, modelKey) || {};
  const comparisonEntry = findComparisonEntry(results?.comparison, modelKey) || {};
  const graphEntry =
    getModelEntry(results?.graphs, modelKey) ||
    modelResult?.plots?.capacitance_series ||
    modelResult?.plots?.concentration_curve ||
    modelResult?.graph ||
    comparisonEntry?.graph ||
    null;

  const metrics = modelResult?.metrics || {};
  const chartData = normalizeGraphPoints(graphEntry);

  const r2 = toNumber(
    firstDefined(
      performance?.r2,
      performance?.r2_score,
      metrics?.r2,
      metrics?.r2_score,
      modelResult?.r2,
      comparisonEntry?.r2,
      comparisonEntry?.r2_score
    )
  );

  const rmse = toNumber(
    firstDefined(
      performance?.rmse,
      metrics?.rmse,
      modelResult?.rmse,
      comparisonEntry?.rmse,
      comparisonEntry?.RMSE
    )
  );

  const capacitance = toNumber(
    firstDefined(
      performance?.capacitance,
      performance?.predicted_capacitance,
      metrics?.predicted_capacitance_max,
      metrics?.predicted_capacitance_mean,
      modelResult?.capacitance,
      comparisonEntry?.capacitance,
      comparisonEntry?.predicted_capacitance
    )
  );

  const bestConcentration = toNumber(
    firstDefined(
      performance?.best_concentration,
      performance?.concentration,
      modelResult?.best_concentration,
      comparisonEntry?.best_concentration,
      comparisonEntry?.concentration
    )
  );

  const explicitError = firstDefined(
    performance?.error,
    modelResult?.error,
    modelResult?.message,
    modelResult?.success === false ? 'Model training failed.' : null
  );

  const hasData =
    isValidNumber(r2) ||
    isValidNumber(rmse) ||
    isValidNumber(capacitance) ||
    isValidNumber(bestConcentration) ||
    chartData.length > 0;

  const status = explicitError ? 'failed' : hasData ? 'success' : 'failed';

  return {
    key: modelKey,
    label: MODEL_LABELS[modelKey],
    color: MODEL_COLORS[modelKey],
    r2,
    rmse,
    capacitance,
    bestConcentration,
    chartData,
    error: explicitError,
    status,
  };
};

function MetricChip({ label, value, empty = false }) {
  return (
    <div className={`metric-chip${empty ? ' metric-chip--empty' : ''}`}>
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function ResultsSection({ results, hasResults }) {
  const metadata = getMetadata(results);

  const modelSummaries = useMemo(
    () => MODEL_ORDER.map((modelKey) => buildModelSummary(results, modelKey)),
    [results]
  );

  const bestModelRaw = firstDefined(results?.best_model, results?.bestModel);
  const bestModelName = getBestModelName(bestModelRaw);
  const bestModel = modelSummaries.find((item) =>
    (MODEL_ALIASES[item.key] || [item.key]).includes(bestModelName)
  );

  const bestCapacitance = toNumber(
    firstDefined(results?.capacitance, bestModelRaw?.capacitance, bestModel?.capacitance)
  );
  const bestConcentration = toNumber(
    firstDefined(
      results?.best_concentration,
      bestModelRaw?.best_concentration,
      bestModel?.bestConcentration
    )
  );
  const bestDopant = firstDefined(
    results?.best_dopant,
    bestModelRaw?.dopant,
    results?.dopant,
    'Not specified'
  );
  const predictionRows = getPredictionRows(results);

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
          <strong>{metadata.selected_train_dataset || '—'}</strong>
        </div>
        <div className="metadata-item">
          <span>Testing dataset</span>
          <strong>{metadata.uploaded_test_filename || '—'}</strong>
        </div>
        <div className="metadata-item">
          <span>Target column</span>
          <strong>{metadata.target_column || '—'}</strong>
        </div>
        <div className="metadata-item">
          <span>Features used</span>
          <strong>{metadata.feature_columns?.length || 0}</strong>
        </div>
      </div>

      <div className="dashboard-best-highlight">
        <span className="best-highlight__badge">Top Recommendation</span>
        <h3 className="best-highlight__title">
          {bestModel?.label || bestModelName || 'Best model pending'}
        </h3>
        <div className="best-highlight__metrics">
          <div className="best-highlight__metric">
            <span>Best capacitance</span>
            <strong>{formatCapacitance(bestCapacitance)}</strong>
          </div>
          <div className="best-highlight__metric">
            <span>Best concentration</span>
            <strong>{formatConcentration(bestConcentration)}</strong>
          </div>
          <div className="best-highlight__metric">
            <span>Recommended dopant</span>
            <strong>{bestDopant || '—'}</strong>
          </div>
        </div>
      </div>

      <div className="model-dashboard-grid">
        {modelSummaries.map((model) => {
          const isBest = bestModel?.key === model.key;
          const stateClass =
            model.status === 'success' ? 'model-result-card--success' : 'model-result-card--failed';

          return (
            <div
              key={model.key}
              className={`model-result-card ${stateClass}${isBest ? ' model-result-card--active' : ''}`}
            >
              <div className="model-result-card__header">
                <div>
                  <h3 className="model-result-card__title">{model.label}</h3>
                </div>
                <div className="model-result-card__status">
                  <span className="status-badge">
                    {model.status === 'success' ? 'Completed' : 'Failed'}
                  </span>
                </div>
              </div>

              <div className="model-result-card__metrics">
                <MetricChip label="R²" value={formatMetric(model.r2)} empty={!isValidNumber(model.r2)} />
                <MetricChip label="RMSE" value={formatMetric(model.rmse)} empty={!isValidNumber(model.rmse)} />
                <MetricChip
                  label="Capacitance"
                  value={formatCapacitance(model.capacitance)}
                  empty={!isValidNumber(model.capacitance)}
                />
                <MetricChip
                  label="Best concentration"
                  value={formatConcentration(model.bestConcentration)}
                  empty={!isValidNumber(model.bestConcentration)}
                />
              </div>

              {model.status === 'failed' ? (
                <div className="model-failure">
                  <p>{model.error || 'This model did not return valid dashboard metrics.'}</p>
                </div>
              ) : model.chartData.length ? (
                <div className="inline-chart-wrap">
                  <ResponsiveContainer width="100%" height={180}>
                    <LineChart data={model.chartData} margin={{ top: 8, right: 8, left: 0, bottom: 8 }}>
                      <CartesianGrid strokeDasharray="3 3" vertical={false} />
                      <XAxis
                        dataKey="concentration"
                        tickFormatter={(value) => {
                          const numeric = toNumber(value);
                          return isValidNumber(numeric) ? numeric.toFixed(2) : value;
                        }}
                      />
                      <YAxis
                        tickFormatter={(value) => {
                          const numeric = toNumber(value);
                          return isValidNumber(numeric) ? numeric.toFixed(0) : value;
                        }}
                      />
                      <Tooltip
                        formatter={(value) => [formatCapacitance(value), 'Capacitance']}
                        labelFormatter={(label) => `Concentration: ${formatConcentration(label)}`}
                      />
                      <Line
                        type="monotone"
                        dataKey="capacitance"
                        stroke={model.color}
                        strokeWidth={2.5}
                        dot={false}
                        activeDot={{ r: 4 }}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              ) : (
                <div className="model-failure">
                  <p>No concentration-capacitance curve available for this model.</p>
                </div>
              )}
            </div>
          );
        })}
      </div>

      <div className="comparison-table-card">
        <div className="card-heading">
          <h3>Performance comparison</h3>
          <p>Side-by-side dashboard metrics for all evaluated models.</p>
        </div>
        <div className="dashboard-table-wrap">
          <table className="dashboard-table">
            <thead>
              <tr>
                <th>Model</th>
                <th>R²</th>
                <th>RMSE</th>
                <th>Capacitance F/g</th>
                <th>Best concentration</th>
              </tr>
            </thead>
            <tbody>
              {modelSummaries.map((model) => (
                <tr key={model.key}>
                  <td>{model.label}</td>
                  <td>{formatMetric(model.r2)}</td>
                  <td>{formatMetric(model.rmse)}</td>
                  <td>{formatCapacitance(model.capacitance)}</td>
                  <td>{formatConcentration(model.bestConcentration)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="charts-grid">
        <div className="chart-card">
          <div className="card-heading">
            <h3>Predicted capacitance table</h3>
            <p>Prediction outputs returned from backend evaluation.</p>
          </div>

          {predictionRows.length ? (
            <div className="table-wrap">
              <table className="data-table">
                <thead>
                  <tr>
                    {Object.keys(predictionRows[0]).map((column) => (
                      <th key={column}>{column.replace(/_/g, ' ')}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {predictionRows.slice(0, 50).map((row, index) => (
                    <tr key={`prediction-row-${index}`}>
                      {Object.keys(predictionRows[0]).map((column) => (
                        <td key={`${index}-${column}`}>{row[column] ?? '—'}</td>
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
    </div>
  );
}

export default ResultsSection;
