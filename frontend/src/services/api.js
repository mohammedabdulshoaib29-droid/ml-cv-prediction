import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || '/api';

const axiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 900000,
});

const rootAxiosInstance = axios.create({
  baseURL: process.env.REACT_APP_ROOT_API_URL || '',
  timeout: 900000,
});

const buildError = (error, fallbackMessage) => {
  const errorMessage =
    error.response?.data?.error ||
    error.response?.data?.detail ||
    error.response?.data?.message ||
    error.message ||
    fallbackMessage;

  console.error('API Error:', {
    status: error.response?.status,
    message: errorMessage,
    url: error.config?.url,
    method: error.config?.method,
  });

  const newError = new Error(errorMessage);
  newError.response = error.response;
  return newError;
};

const onResponseError = (error) => {
  throw buildError(error, 'An error occurred');
};

axiosInstance.interceptors.response.use((response) => response, onResponseError);
rootAxiosInstance.interceptors.response.use((response) => response, onResponseError);

const postMultipart = async (client, url, formData) =>
  client.post(url, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });

const tryEndpoints = async (requestFactories) => {
  let lastError;

  for (const createRequest of requestFactories) {
    try {
      const response = await createRequest();
      return response.data;
    } catch (error) {
      lastError = error;
      const status = error.response?.status;
      if (status && ![404, 405].includes(status)) {
        throw buildError(error, 'Request failed');
      }
    }
  }

  throw buildError(lastError || new Error('No API endpoint available'), 'Request failed');
};

export const normalizeResults = (payload = {}) => {
  const bestModel =
    payload.best_model ||
    (payload.bestModel
      ? {
          name: payload.bestModel.name,
          capacitance: payload.bestModel.capacitance,
          best_concentration: payload.bestModel.best_concentration || payload.bestModel.bestConcentration,
          dopant: payload.bestModel.dopant,
        }
      : null);

  const comparison = Array.isArray(payload.comparison)
    ? payload.comparison
    : Array.isArray(payload.table)
      ? payload.table
      : [];

  return {
    success: Boolean(payload.success ?? true),
    message: payload.message || payload.training_status || payload.prediction_status || '',
    metadata: payload.metadata || {},
    models: payload.models || {},
    comparison,
    performance: payload.performance || {},
    graphs: payload.graphs || {},
    predictionTable: payload.prediction_table || payload.predictionTable || [],
    bestModel,
    capacitance: payload.capacitance ?? bestModel?.capacitance ?? null,
    bestConcentration: payload.best_concentration ?? bestModel?.best_concentration ?? null,
    timestamp: payload.timestamp || null,
    raw: payload,
  };
};

export const datasetService = {
  getDatasets: async () => {
    try {
      return await tryEndpoints([
        () => axiosInstance.get('/datasets/list'),
        () => rootAxiosInstance.get('/results'),
      ]);
    } catch (error) {
      throw buildError(error, `Failed to load datasets: ${error.message}`);
    }
  },

  uploadDataset: async (file) => {
    try {
      const formData = new FormData();
      formData.append('file', file);

      return await tryEndpoints([
        () => postMultipart(rootAxiosInstance, '/upload-train', formData),
        () => postMultipart(axiosInstance, '/datasets/upload', formData),
      ]);
    } catch (error) {
      throw buildError(error, `Failed to upload dataset: ${error.message}`);
    }
  },

  previewDataset: async (datasetName) => {
    try {
      return await tryEndpoints([
        () => axiosInstance.get(`/datasets/preview/${encodeURIComponent(datasetName)}`),
      ]);
    } catch (error) {
      throw buildError(error, `Failed to preview dataset: ${error.message}`);
    }
  },

  deleteDataset: async (datasetName) => {
    try {
      return await tryEndpoints([
        () => axiosInstance.delete(`/datasets/delete/${encodeURIComponent(datasetName)}`),
      ]);
    } catch (error) {
      throw buildError(error, `Failed to delete dataset: ${error.message}`);
    }
  },
};

export const trainModels = async ({
  datasetName,
  modelType = 'all',
  target,
  predictors,
  testFile,
} = {}) => {
  try {
    if (!datasetName) {
      throw new Error('Dataset name is required');
    }

    const formData = new FormData();
    formData.append('dataset_name', datasetName);
    formData.append('train_dataset', datasetName);
    formData.append('model_type', modelType);

    if (testFile) {
      formData.append('test_file', testFile);
    }
    if (target) {
      formData.append('target', target);
    }
    if (predictors?.length) {
      formData.append('predictors', JSON.stringify(predictors));
    }

    const data = await tryEndpoints([
      () => postMultipart(rootAxiosInstance, '/train', formData),
      () => postMultipart(axiosInstance, '/models/train', formData),
    ]);

    return normalizeResults(data);
  } catch (error) {
    throw buildError(error, `Training failed: ${error.message}`);
  }
};

export const predictionService = {
  predict: async (datasetName, testFile, modelType = 'all', options = {}) => {
    try {
      if (!datasetName) {
        throw new Error('Dataset name is required');
      }
      if (!testFile) {
        throw new Error('Test file is required');
      }

      const formData = new FormData();
      formData.append('dataset_name', datasetName);
      formData.append('train_dataset', datasetName);
      formData.append('test_file', testFile);
      formData.append('model_type', modelType);

      if (options.target) {
        formData.append('target', options.target);
      }

      if (options.predictors?.length) {
        formData.append('predictors', JSON.stringify(options.predictors));
      }

      const data = await tryEndpoints([
        () => postMultipart(rootAxiosInstance, '/predict', formData),
        () => postMultipart(axiosInstance, '/models/predict', formData),
      ]);

      return normalizeResults(data);
    } catch (error) {
      throw buildError(error, `Prediction failed: ${error.message}`);
    }
  },

  uploadTestDataset: async (file, datasetName = '') => {
    try {
      const formData = new FormData();
      formData.append('file', file);
      if (datasetName) {
        formData.append('dataset_name', datasetName);
      }

      return await tryEndpoints([
        () => postMultipart(rootAxiosInstance, '/upload-test', formData),
      ]);
    } catch (error) {
      throw buildError(error, `Failed to upload test dataset: ${error.message}`);
    }
  },

  getLatestResults: async () => {
    try {
      const data = await tryEndpoints([
        () => rootAxiosInstance.get('/results'),
      ]);
      return normalizeResults(data);
    } catch (error) {
      throw buildError(error, `Failed to fetch results: ${error.message}`);
    }
  },
};

export default axiosInstance;
