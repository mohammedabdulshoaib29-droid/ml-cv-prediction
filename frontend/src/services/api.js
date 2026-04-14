import axios from 'axios';

// Use relative paths since frontend and backend are on the same server
const API_BASE_URL = '/api';

// Create axios instance with better error handling
const axiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 900000, // 15 minute timeout for predictions (model training can be slow)
});

// Add response interceptor for better error handling
axiosInstance.interceptors.response.use(
  response => response,
  error => {
    const errorMessage = error.response?.data?.detail || error.response?.data?.message || error.message || 'An error occurred';
    console.error('API Error:', {
      status: error.response?.status,
      message: errorMessage,
      url: error.config?.url,
      method: error.config?.method
    });
    
    const newError = new Error(errorMessage);
    newError.response = error.response;
    throw newError;
  }
);

export const datasetService = {
  getDatasets: async () => {
    try {
      const response = await axiosInstance.get(`/datasets`);
      return response.data.datasets;
    } catch (error) {
      console.error('Error fetching datasets:', error);
      throw new Error(`Failed to load datasets: ${error.message}`);
    }
  },

  uploadDataset: async (file) => {
    try {
      const formData = new FormData();
      formData.append('file', file);
      const response = await axiosInstance.post(`/upload-dataset`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      return response.data;
    } catch (error) {
      console.error('Error uploading dataset:', error);
      throw new Error(`Failed to upload dataset: ${error.message}`);
    }
  },

  deleteDataset: async (datasetName) => {
    try {
      const response = await axiosInstance.delete(`/datasets/${datasetName}`);
      return response.data;
    } catch (error) {
      console.error('Error deleting dataset:', error);
      throw new Error(`Failed to delete dataset: ${error.message}`);
    }
  }
};

export const predictionService = {
  predict: async (datasetName, testFile, modelType = 'all') => {
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

      const response = await axiosInstance.post(`/models/predict`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      return response.data;
    } catch (error) {
      console.error('Error making predictions:', error);
      throw new Error(`Prediction failed: ${error.message}`);
    }
  }
};
