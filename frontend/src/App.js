import React, { useCallback, useEffect, useMemo, useState } from 'react';
import AppShell from './components/app/AppShell';
import HomePage from './pages/HomePage';
import DatasetManagementPage from './pages/DatasetManagementPage';
import ModelTrainingPage from './pages/ModelTrainingPage';
import PredictionPage from './pages/PredictionPage';
import DashboardPage from './pages/DashboardPage';
import PerformanceAnalyticsPage from './pages/PerformanceAnalyticsPage';
import './styles/app-shell.css';

const ROUTES = {
  '/': 'Home',
  '/datasets': 'Dataset Management',
  '/training': 'Model Training',
  '/prediction': 'Prediction',
  '/dashboard': 'Dashboard',
  '/analytics': 'Performance Analytics',
};

const DEFAULT_MODEL_TYPE = 'all';

const getInitialRoute = () => {
  const currentPath = window.location.pathname || '/';
  return ROUTES[currentPath] ? currentPath : '/';
};

function App() {
  const [currentRoute, setCurrentRoute] = useState(getInitialRoute);
  const [selectedDataset, setSelectedDataset] = useState('');
  const [selectedModelType, setSelectedModelType] = useState(DEFAULT_MODEL_TYPE);
  const [latestResults, setLatestResults] = useState(null);
  const [trainingStatus, setTrainingStatus] = useState({
    loading: false,
    success: false,
    error: '',
    message: '',
  });
  const [predictionStatus, setPredictionStatus] = useState({
    loading: false,
    success: false,
    error: '',
    message: '',
  });
  const [datasetList, setDatasetList] = useState([]);
  const [datasetPreview, setDatasetPreview] = useState(null);

  useEffect(() => {
    const onPopState = () => {
      setCurrentRoute(getInitialRoute());
    };

    window.addEventListener('popstate', onPopState);

    return () => {
      window.removeEventListener('popstate', onPopState);
    };
  }, []);

  const navigate = useCallback((route) => {
    const safeRoute = ROUTES[route] ? route : '/';
    if (safeRoute !== window.location.pathname) {
      window.history.pushState({}, '', safeRoute);
    }
    setCurrentRoute(safeRoute);
  }, []);

  const sharedPageProps = useMemo(
    () => ({
      selectedDataset,
      setSelectedDataset,
      selectedModelType,
      setSelectedModelType,
      latestResults,
      setLatestResults,
      trainingStatus,
      setTrainingStatus,
      predictionStatus,
      setPredictionStatus,
      datasetList,
      setDatasetList,
      datasetPreview,
      setDatasetPreview,
      navigate,
    }),
    [
      selectedDataset,
      selectedModelType,
      latestResults,
      trainingStatus,
      predictionStatus,
      datasetList,
      datasetPreview,
      navigate,
    ]
  );

  const renderPage = () => {
    switch (currentRoute) {
      case '/datasets':
        return <DatasetManagementPage {...sharedPageProps} />;
      case '/training':
        return <ModelTrainingPage {...sharedPageProps} />;
      case '/prediction':
        return <PredictionPage {...sharedPageProps} />;
      case '/dashboard':
        return <DashboardPage {...sharedPageProps} />;
      case '/analytics':
        return <PerformanceAnalyticsPage {...sharedPageProps} />;
      case '/':
      default:
        return <HomePage {...sharedPageProps} />;
    }
  };

  return (
    <AppShell currentRoute={currentRoute} navigate={navigate} navItems={ROUTES}>
      {renderPage()}
    </AppShell>
  );
}

export default App;