import React from 'react';
import PageHeader from '../components/app/PageHeader';
import SectionCard from '../components/app/SectionCard';
import DatasetManager from '../components/DatasetManager';

function DatasetManagementPage(props) {
  const { selectedDataset, datasetList } = props;

  return (
    <div className="page-layout">
      <PageHeader
        eyebrow="Data Operations"
        title="Dataset Management"
        description="Upload training data, browse available datasets, inspect previews, and prepare your selected dataset for downstream model training and prediction."
      />

      <div className="responsive-grid responsive-grid--two">
        <SectionCard title="Current Selection" subtitle="Your active training dataset for the workflow.">
          <p className="metric-callout">{selectedDataset || 'No dataset selected'}</p>
          <p className="supporting-text">Available datasets: {Array.isArray(datasetList) ? datasetList.length : 0}</p>
        </SectionCard>

        <SectionCard title="Dataset Guidance" subtitle="Recommended upload and review practices.">
          <ul className="feature-list">
            <li>Upload clean CSV or tabular data prepared for training.</li>
            <li>Preview column structure before starting model training.</li>
            <li>Keep one dataset selected to maintain a consistent workflow.</li>
          </ul>
        </SectionCard>
      </div>

      <SectionCard title="Dataset Workspace" subtitle="Use the existing dataset manager tools below.">
        <DatasetManager {...props} />
      </SectionCard>
    </div>
  );
}

export default DatasetManagementPage;