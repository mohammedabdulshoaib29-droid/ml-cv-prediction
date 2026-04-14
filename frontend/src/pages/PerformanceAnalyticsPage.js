import React from 'react';
import PageHeader from '../components/app/PageHeader';
import SectionCard from '../components/app/SectionCard';

function PerformanceAnalyticsPage({ latestResults }) {
  const models = latestResults?.models || latestResults?.comparison || {};
  const performance = latestResults?.performance || {};
  const predictionTable = latestResults?.prediction_table || latestResults?.table || [];

  return (
    <div className="page-layout">
      <PageHeader
        eyebrow="Model Evaluation"
        title="Performance Analytics"
        description="Inspect model-wise metrics, comparison summaries, and output table counts from the latest available results."
      />

      <div className="responsive-grid responsive-grid--three">
        <SectionCard title="Models Evaluated">
          <p className="metric-callout">{Array.isArray(models) ? models.length : Object.keys(models || {}).length}</p>
        </SectionCard>
        <SectionCard title="Best Model">
          <p className="metric-callout">{latestResults?.best_model || performance?.best_model || 'Not available'}</p>
        </SectionCard>
        <SectionCard title="Prediction Rows">
          <p className="metric-callout">{Array.isArray(predictionTable) ? predictionTable.length : 0}</p>
        </SectionCard>
      </div>

      <div className="responsive-grid responsive-grid--two">
        <SectionCard title="Performance Summary" subtitle="Metric payload returned by the backend.">
          <pre className="data-preview">{JSON.stringify(performance, null, 2)}</pre>
        </SectionCard>

        <SectionCard title="Model Comparison" subtitle="Comparison data for all trained models.">
          <pre className="data-preview">{JSON.stringify(models, null, 2)}</pre>
        </SectionCard>
      </div>
    </div>
  );
}

export default PerformanceAnalyticsPage;