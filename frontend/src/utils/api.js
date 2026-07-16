/**
 * API Utility Functions
 * Centralized API calls for the frontend
 */

import axios from 'axios';

// Create axios instance with base URL
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for adding token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Handle specific error status codes
      switch (error.response.status) {
        case 401:
          // Unauthorized - redirect to login
          if (typeof window !== 'undefined') {
            localStorage.removeItem('token');
            window.location.href = '/login';
          }
          break;
        case 404:
          console.error('Resource not found');
          break;
        case 500:
          console.error('Server error');
          break;
        default:
          console.error('API error:', error.response.status);
      }
    } else if (error.request) {
      // Request was made but no response received
      console.error('No response received:', error.request);
    } else {
      // Something happened in setting up the request
      console.error('Request setup error:', error.message);
    }
    return Promise.reject(error);
  }
);

// Exchange Rate API
export const getExchangeRate = async () => {
  try {
    const response = await api.get('/api/exchange-rate');
    return response.data;
  } catch (error) {
    console.error('Error fetching exchange rate:', error);
    // Return default rate if error
    return { currency: 'USDT', rate: 190000, last_updated: new Date().toISOString() };
  }
};

// Products API
export const getAllProducts = async () => {
  try {
    const response = await api.get('/api/products');
    return response.data;
  } catch (error) {
    console.error('Error fetching products:', error);
    return [];
  }
};

export const getProductById = async (productId) => {
  try {
    const response = await api.get(`/api/products/${productId}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching product ${productId}:`, error);
    return null;
  }
};

export const getProductPrices = async () => {
  try {
    const response = await api.get('/api/products/prices');
    return response.data.prices || [];
  } catch (error) {
    console.error('Error fetching product prices:', error);
    return [];
  }
};

export const calculatePrice = async (productName, supplier = 'auto') => {
  try {
    const response = await api.post('/api/products/calculate-price', {
      product_name: productName,
      supplier: supplier,
    });
    return response.data;
  } catch (error) {
    console.error(`Error calculating price for ${productName}:`, error);
    return null;
  }
};

// Orders API
export const createOrder = async (productId, quantity = 1, paymentMethod = 'crypto') => {
  try {
    const response = await api.post('/api/orders/', {
      product_id: productId,
      quantity: quantity,
      payment_method: paymentMethod,
    });
    return response.data;
  } catch (error) {
    console.error('Error creating order:', error);
    return null;
  }
};

export const getOrder = async (orderId) => {
  try {
    const response = await api.get(`/api/orders/${orderId}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching order ${orderId}:`, error);
    return null;
  }
};

export const getOrderStatus = async (orderId) => {
  try {
    const response = await api.get(`/api/orders/${orderId}/status`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching order status ${orderId}:`, error);
    return null;
  }
};

export const confirmPayment = async (orderId, txHash) => {
  try {
    const response = await api.post(`/api/orders/${orderId}/confirm-payment`, {
      tx_hash: txHash,
    });
    return response.data;
  } catch (error) {
    console.error(`Error confirming payment for order ${orderId}:`, error);
    return null;
  }
};

// Shared Accounts API
export const createSharedAccount = async (productId, quantity = 1) => {
  try {
    const response = await api.post('/api/shared-accounts/', {
      product_id: productId,
      quantity: quantity,
    });
    return response.data;
  } catch (error) {
    console.error('Error creating shared account:', error);
    return null;
  }
};

export const getSharedAccount = async (accountId) => {
  try {
    const response = await api.get(`/api/shared-accounts/${accountId}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching shared account ${accountId}:`, error);
    return null;
  }
};

// User API
export const login = async (email, password) => {
  try {
    const response = await api.post('/api/auth/login', {
      email: email,
      password: password,
    });
    return response.data;
  } catch (error) {
    console.error('Error logging in:', error);
    return null;
  }
};

export const register = async (userData) => {
  try {
    const response = await api.post('/api/auth/register', userData);
    return response.data;
  } catch (error) {
    console.error('Error registering:', error);
    return null;
  }
};

export const getUserProfile = async () => {
  try {
    const response = await api.get('/api/auth/profile');
    return response.data;
  } catch (error) {
    console.error('Error fetching user profile:', error);
    return null;
  }
};

export const updateUserProfile = async (userData) => {
  try {
    const response = await api.put('/api/auth/profile', userData);
    return response.data;
  } catch (error) {
    console.error('Error updating user profile:', error);
    return null;
  }
};

// Health Check
export const healthCheck = async () => {
  try {
    const response = await api.get('/api/health');
    return response.data;
  } catch (error) {
    console.error('Error in health check:', error);
    return { status: 'unhealthy' };
  }
};

export default api;
