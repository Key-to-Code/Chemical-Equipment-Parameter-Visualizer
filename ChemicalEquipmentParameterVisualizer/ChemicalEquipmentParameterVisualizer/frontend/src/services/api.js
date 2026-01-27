import axios from 'axios';

// Use environment variable for API URL configuration
// Falls back to localhost:8000 for local development if not set
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 second timeout for requests
});

// Request interceptor for debugging and adding common headers
api.interceptors.request.use(
  (config) => {
    // Log requests in development mode
    if (import.meta.env.DEV) {
      console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`);
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for consistent error handling
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Create a consistent error format
    const errorMessage = error.response?.data?.error 
      || error.response?.data?.message 
      || error.message 
      || 'An unexpected error occurred';
    
    // Log errors in development mode
    if (import.meta.env.DEV) {
      console.error(`[API Error] ${errorMessage}`, error);
    }
    
    return Promise.reject(error);
  }
);

export const uploadCSV = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await api.post('/upload/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const getDatasets = async () => {
  const response = await api.get('/datasets/');
  return response.data;
};

export const getDatasetDetail = async (id) => {
  const response = await api.get(`/datasets/${id}/`);
  return response.data;
};

export const getDatasetSummary = async (id) => {
  const response = await api.get(`/datasets/${id}/summary/`);
  return response.data;
};

export const downloadPDF = async (id, filename) => {
  const response = await api.get(`/datasets/${id}/generate_pdf/`, {
    responseType: 'blob',
  });
  const url = window.URL.createObjectURL(new Blob([response.data]));
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', filename || 'report.pdf');
  document.body.appendChild(link);
  link.click();
  link.remove();
};

export default api;
