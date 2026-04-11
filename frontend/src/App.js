import React from 'react';
import Header from './components/Header';
import HeroSection from './components/HeroSection';
import OverviewSection from './components/OverviewSection';
import ArchitectureSection from './components/ArchitectureSection';
import ComponentsSection from './components/ComponentsSection';
import InputOutputSection from './components/InputOutputSection';
import PerformanceSection from './components/PerformanceSection';
import InferenceSection from './components/InferenceSection';
import ReferencesSection from './components/ReferencesSection';
import Footer from './components/Footer';
import './App.css';
import './styles/Global.css';

function App() {
  return (
    <div className="app-container">
      <Header />
      <HeroSection />
      <OverviewSection />
      <ArchitectureSection />
      <ComponentsSection />
      <InputOutputSection />
      <PerformanceSection />
      <InferenceSection />
      <ReferencesSection />
      <Footer />
    </div>
  );
}

export default App;
