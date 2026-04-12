import React, { Suspense, lazy } from 'react';
import Header from './components/Header';
import HeroSection from './components/HeroSection';
import Footer from './components/Footer';
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
  return (
    <div className="app-container">
      <Header />
      <HeroSection />
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
        <InferenceSection />
      </Suspense>
      <Suspense fallback={<LoadingPlaceholder />}>
        <ReferencesSection />
      </Suspense>
      <Footer />
    </div>
  );
}

export default App;
