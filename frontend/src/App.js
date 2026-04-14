import React, { useMemo, useState } from 'react';
import DatasetManager from './components/DatasetManager';
import PredictionEngine from './components/PredictionEngine';
import ResultsSection from './components/ResultsSection';
import './styles/dashboard.css';

function App() {
  const [selectedDataset, setSelectedDataset] = useState('');
  const [predictionResults, setPredictionResults] = useState(null);

  const hasResults = useMemo(() => {
    return Boolean(predictionResults && predictionResults.success);
  }, [predictionResults]);

  return (
    <div className="app-shell">
      <header className="dashboard-hero">
        <div>
          <p className="dashboard-eyebrow">Machine Learning Dashboard</p>
          <h1>Capacitance Prediction Workspace</h1>
          <p className="dashboard-subtitle">
            Select a stored training dataset, upload a testing dataset, and compare ANN,
            Random Forest, and XGBoost predictions in one place.
          </p>
        </div>
        <div className="dashboard-hero-badge">
          <span>Training Dataset</span>
          <strong>{selectedDataset || 'Not selected'}</strong>
        </div>
      </header>

      <main className="ml-dashboard-grid">
        <section className="dashboard-panel panel-span-7">
          <DatasetManager
            selectedDataset={selectedDataset}
            onSelectDataset={setSelectedDataset}
          />
        </section>

        <section className="dashboard-panel panel-span-5">
          <PredictionEngine
            selectedDataset={selectedDataset}
            onPredictionComplete={setPredictionResults}
          />
        </section>

        <section className="dashboard-panel panel-span-12">
          <ResultsSection results={predictionResults} hasResults={hasResults} />
        </section>
      </main>
    </div>
  );
}

export default App;