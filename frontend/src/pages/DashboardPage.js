import React from 'react';
import PageHeader from '../components/app/PageHeader';
import SectionCard from '../components/app/SectionCard';
import ResultsSection from '../components/ResultsSection';

function DashboardPage({ latestResults, trainingStatus, predictionStatus, navigate }) {
  const performance = latestResults?.performance || latestResults?.comparison || {};
  const bestModel = latestResults?.best_model || performance?.best_model || 'Not available';
  const r2Value = performance?.r2 || performance?.R2 || latestResults?.r2 || 'Not available';
  const rmseValue = performance?.rmse || performance?.RMSE || latestResults?.rmse || 'Not available';
  const capacitanceValue =
    latestResults?.capacitance || latestResults?.best_concentration || latestResults?.metadata?.capacitance || 'Not available';
  const graphItems = latestResults?.graphs
    ? Object.entries(latestResults.graphs)
    : [];

  return (
    <div className="page-layout">
      <PageHeader
        eyebrow="Executive View"
        title="Dashboard"
        description="Review the latest training and prediction outcomes, including core regression metrics and graph outputs."
        actions={
          <div className="button-group">
            <button type="button" className="secondary-button" onClick={() => navigate('/training')}>
              Train Models
            </button>
            <button type="button" className="primary-button" onClick={() => navigate('/prediction')}>
              Run Prediction
            </button>
          </div>
        }
      />

      <div className="responsive-grid responsive-grid--four">
        <SectionCard title="R²">
          <p className="metric-callout">{String(r2Value)}</p>
        </SectionCard>
        <SectionCard title="RMSE">
          <p className="metric-callout">{String(rmseValue)}</p>
        </SectionCard>
        <SectionCard title="Capacitance">
          <p className="metric-callout">{String(capacitanceValue)}</p>
        </SectionCard>
        <SectionCard title="Best Model">
          <p className="metric-callout">{String(bestModel)}</p>
        </SectionCard>
      </div>

      <div className="responsive-grid responsive-grid--two">
        <SectionCard title="Workflow Status" subtitle="Latest process state across training and prediction.">
          <ul className="feature-list">
            <li>Training: {trainingStatus.loading ? 'Running...' : trainingStatus.message || 'Idle'}</li>
            <li>Prediction: {predictionStatus.loading ? 'Running...' : predictionStatus.message || 'Idle'}</li>
            {trainingStatus.error ? <li className="status-box__error">Training error: {trainingStatus.error}</li> : null}
            {predictionStatus.error ? <li className="status-box__error">Prediction error: {predictionStatus.error}</li> : null}
          </ul>
        </SectionCard>

        <SectionCard title="Graphs" subtitle="Rendered data from backend graph outputs or placeholders.">
          {graphItems.length ? (
            <div className="graph-list">
              {graphItems.map(([key, value]) => (
                <div key={key} className="graph-placeholder">
                  <strong>{key}</strong>
                  <p>{typeof value === 'string' ? value : 'Graph data available'}</p>
                </div>
              ))}
            </div>
          ) : (
            <div className="graph-placeholder">
              <strong>No graph payload available yet</strong>
              <p>Train models or fetch recent results to populate dashboard visualizations.</p>
            </div>
          )}
        </SectionCard>
      </div>

      <SectionCard title="Detailed Results" subtitle="Expanded output from the latest pipeline run.">
        <ResultsSection
          results={latestResults}
          loading={trainingStatus.loading || predictionStatus.loading}
          error={trainingStatus.error || predictionStatus.error}
        />
      </SectionCard>
    </div>
  );
}

export default DashboardPage;