import React, { Suspense, lazy, useState } from 'react';
import Header from './components/Header';
import HeroSection from './components/HeroSection';
import Footer from './components/Footer';
import DatasetManager from './components/DatasetManager';
import PredictionEngine from './components/PredictionEngine';
import ResultsSection from './components/ResultsSection';
import './App.css';
import './styles/Global.css';

// Lazy load heavy components for faster initial load
const OverviewSection = lazy(() => import('./components/OverviewSection'));
const ArchitectureSection = lazy(() => import('./components/ArchitectureSection'));
const ComponentsSection = lazy(() => import('./components/ComponentsSection'));
const InputOutputSection = lazy(() => import('./components/InputOutputSection'));
const PerformanceSection = lazy(() => import('./components/PerformanceSection'));
const InferenceSection = lazy(() => import('./components/InferenceSection'));
const ReferencesSection = lazy(() => import('./components/ReferencesSection'));

// Loading placeholder
const LoadingPlaceholder = () => <div style={{padding: '40px', textAlign: 'center', color: '#666'}}>Loading...</div>;

function App() {
  const [selectedDataset, setSelectedDataset] = useState('');
  const [predictionResults, setPredictionResults] = useState(null);

  const handlePredictionComplete = (results) => {
    setPredictionResults(results);
    // Scroll to results section
    setTimeout(() => {
      document.querySelector('.results-section')?.scrollIntoView({ behavior: 'smooth' });
    }, 100);
  };

  const handleRunAnother = () => {
    setPredictionResults(null);
    // Scroll back to prediction engine
    document.querySelector('.prediction-engine')?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className="app-container">
      <Header />
      <HeroSection />
      
      {/* ML Application Section - 3 Main Sections */}
      <div className="ml-app-section">
        <div className="section-container">
          {/* Section 1: Dataset Management */}
          <DatasetManager 
            onDatasetSelected={setSelectedDataset}
          />

          {/* Section 2: Run Prediction */}
          <PredictionEngine 
            selectedDataset={selectedDataset}
            onPredictionComplete={handlePredictionComplete}
          />

          {/* Section 3: Results */}
          {predictionResults && (
            <ResultsSection 
              results={predictionResults}
              onRunAnother={handleRunAnother}
            />
          )}
        </div>
      </div>

      <Suspense fallback={<LoadingPlaceholder />}>
        <OverviewSection />
      </Suspense>
      <Suspense fallback={<LoadingPlaceholder />}>
        <ArchitectureSection />
      </Suspense>
      <Suspense fallback={<LoadingPlaceholder />}>
        <ComponentsSection />
      </Suspense>
      <Suspense fallback={<LoadingPlaceholder />}>
        <InputOutputSection />
      </Suspense>
      <Suspense fallback={<LoadingPlaceholder />}>
        <PerformanceSection />
      </Suspense>
      <Suspense fallback={<LoadingPlaceholder />}>
        <ReferencesSection />
      </Suspense>
      <Footer />
    </div>
  );
}

export default App;
