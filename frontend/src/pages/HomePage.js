import React from 'react';
import PageHeader from '../components/app/PageHeader';
import SectionCard from '../components/app/SectionCard';

function HomePage({ navigate, latestResults, selectedDataset }) {
  const quickLinks = [
    { label: 'Home', route: '/' },
    { label: 'Dataset Management', route: '/datasets' },
    { label: 'Model Training', route: '/training' },
    { label: 'Prediction', route: '/prediction' },
    { label: 'Dashboard', route: '/dashboard' },
    { label: 'Performance Analytics', route: '/analytics' },
  ];

  const summaryItems = [
    { label: 'Selected Dataset', value: selectedDataset || 'No dataset selected' },
    {
      label: 'Best Model',
      value: latestResults?.best_model || latestResults?.metadata?.best_model || 'Awaiting training results',
    },
    {
      label: 'Capacitance',
      value: latestResults?.capacitance || latestResults?.metadata?.capacitance || 'Not available yet',
    },
  ];

  return (
    <div className="page-layout">
      <PageHeader
        eyebrow="BiFe₂O₃ Materials Intelligence"
        title="Predict capacitance and compare machine learning models in one workspace"
        description="This system helps researchers manage datasets, train regression models, generate predictions, and review analytics for BiFe2O3 material experiments without leaving the application shell."
        actions={
          <div className="button-group">
            <button type="button" className="primary-button" onClick={() => navigate('/datasets')}>
              Manage Datasets
            </button>
            <button type="button" className="secondary-button" onClick={() => navigate('/dashboard')}>
              Open Dashboard
            </button>
          </div>
        }
      />

      <div className="responsive-grid responsive-grid--three">
        {summaryItems.map((item) => (
          <SectionCard key={item.label} title={item.label}>
            <p className="metric-callout">{item.value}</p>
          </SectionCard>
        ))}
      </div>

      <div className="responsive-grid responsive-grid--two">
        <SectionCard
          title="Platform Workflow"
          subtitle="Follow the full model lifecycle from data ingestion to analytical insight."
        >
          <ol className="feature-list feature-list--numbered">
            <li>Upload and inspect training datasets.</li>
            <li>Select a preferred model strategy or compare all models.</li>
            <li>Predict on test data and review the latest outputs.</li>
            <li>Track R², RMSE, capacitance, and visual performance summaries.</li>
          </ol>
        </SectionCard>

        <SectionCard
          title="Navigate the application"
          subtitle="Each page is dedicated to a focused part of the ML workflow."
        >
          <div className="link-grid">
            {quickLinks.map((item) => (
              <button
                key={item.route}
                type="button"
                className="link-tile"
                onClick={() => navigate(item.route)}
              >
                <span className="link-tile__title">{item.label}</span>
                <span className="link-tile__text">Open page</span>
              </button>
            ))}
          </div>
        </SectionCard>
      </div>
    </div>
  );
}

export default HomePage;