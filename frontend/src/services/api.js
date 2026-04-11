import axios from 'axios';

// Use relative paths since frontend and backend are on the same server
const API_BASE_URL = '/api';

export const datasetService = {
  getDatasets: async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/datasets`);
      return response.data.datasets;
    } catch (error) {
      console.error('Error fetching datasets:', error);
      throw error;
    }
  },

  uploadDataset: async (file) => {
    try {
      const formData = new FormData();
      formData.append('file', file);
      const response = await axios.post(`${API_BASE_URL}/upload-dataset`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      return response.data;
    } catch (error) {
      console.error('Error uploading dataset:', error);
      throw error;
    }
  },

  deleteDataset: async (datasetName) => {
    try {
      const response = await axios.delete(`${API_BASE_URL}/datasets/${datasetName}`);
      return response.data;
    } catch (error) {
      console.error('Error deleting dataset:', error);
      throw error;
    }
  }
};

export const predictionService = {
  predict: async (datasetName, testFile, modelType = 'all') => {
    try {
      const formData = new FormData();
      formData.append('dataset_name', datasetName);
      formData.append('test_file', testFile);
      formData.append('model_type', modelType);

      const response = await axios.post(`${API_BASE_URL}/predict`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      return response.data;
    } catch (error) {
      console.error('Error making predictions:', error);
      throw error;
    }
  }
};
