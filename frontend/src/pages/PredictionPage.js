import React from 'react';
import PageHeader from '../components/app/PageHeader';
import SectionCard from '../components/app/SectionCard';
import PredictionEngine from '../components/PredictionEngine';

function PredictionPage(props) {
  const { selectedDataset, selectedModelType, predictionStatus } = props;

  return (
    <div className="page-layout">
      <PageHeader
        eyebrow="Inference"
        title="Prediction"
        description="Upload or evaluate test data against the currently selected model workflow to estimate BiFe2O3 capacitance-related outcomes."
      />

      <div className="responsive-grid responsive-grid--three">
        <SectionCard title="Selected Dataset">
          <p className="metric-callout">{selectedDataset || 'No dataset selected'}</p>
        </SectionCard>
        <SectionCard title="Selected Model">
          <p className="metric-callout">{selectedModelType || 'all'}</p>
        </SectionCard>
        <SectionCard title="Prediction Status">
          <p className="metric-callout">
            {predictionStatus.loading ? 'Running...' : predictionStatus.message || 'Idle'}
          </p>
          {predictionStatus.error ? <p className="status-box__error">{predictionStatus.error}</p> : null}
        </SectionCard>
      </div>

      <SectionCard title="Prediction Workspace" subtitle="Use the existing prediction engine tools below.">
        <PredictionEngine {...props} />
      </SectionCard>
    </div>
  );
}

export default PredictionPage;