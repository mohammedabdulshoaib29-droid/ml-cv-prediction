import axios from 'axios';

const API_BASE_URL = '/api';

const axiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 900000,
});

axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    const errorMessage =
      error.response?.data?.error ||
      error.response?.data?.detail ||
      error.response?.data?.message ||
      error.message ||
      'An error occurred';

    console.error('API Error:', {
      status: error.response?.status,
      message: errorMessage,
      url: error.config?.url,
      method: error.config?.method,
    });

    const newError = new Error(errorMessage);
    newError.response = error.response;
    throw newError;
  }
);

export const datasetService = {
  getDatasets: async () => {
    try {
      const response = await axiosInstance.get('/datasets/list');
      return response.data;
    } catch (error) {
      console.error('Error fetching datasets:', error);
      throw new Error(`Failed to load datasets: ${error.message}`);
    }
  },

  uploadDataset: async (file) => {
    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await axiosInstance.post('/datasets/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      return response.data;
    } catch (error) {
      console.error('Error uploading dataset:', error);
      throw new Error(`Failed to upload dataset: ${error.message}`);
    }
  },

  previewDataset: async (datasetName) => {
    try {
      const response = await axiosInstance.get(`/datasets/preview/${encodeURIComponent(datasetName)}`);
      return response.data;
    } catch (error) {
      console.error('Error previewing dataset:', error);
      throw new Error(`Failed to preview dataset: ${error.message}`);
    }
  },

  deleteDataset: async (datasetName) => {
    try {
      const response = await axiosInstance.delete(`/datasets/delete/${encodeURIComponent(datasetName)}`);
      return response.data;
    } catch (error) {
      console.error('Error deleting dataset:', error);
      throw new Error(`Failed to delete dataset: ${error.message}`);
    }
  },
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
      formData.append('test_file', testFile);
      formData.append('model_type', modelType);

      if (options.target) {
        formData.append('target', options.target);
      }

      if (options.predictors?.length) {
        formData.append('predictors', JSON.stringify(options.predictors));
      }

      const response = await axiosInstance.post('/models/predict', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      return response.data;
    } catch (error) {
      console.error('Error making predictions:', error);
      throw new Error(`Prediction failed: ${error.message}`);
    }
  },
};

export default axiosInstance;
