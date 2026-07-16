/**
 * Helper Functions
 * Utility functions for the frontend
 */

// Format price in Persian locale
export const formatPrice = (price) => {
  if (price === undefined || price === null) return '...';
  return new Intl.NumberFormat('fa-IR').format(price);
};

// Format price with currency
export const formatCurrency = (price, currency = 'تومان') => {
  return `${formatPrice(price)} ${currency}`;
};

// Calculate discount percentage
export const calculateDiscount = (ourPrice, originalPrice) => {
  if (!ourPrice || !originalPrice || originalPrice === 0) return 0;
  return Math.round(((originalPrice - ourPrice) / originalPrice) * 100);
};

// Truncate text
export const truncate = (text, length = 50) => {
  if (!text) return '';
  if (text.length <= length) return text;
  return text.substring(0, length) + '...';
};

// Generate a random ID
export const generateId = () => {
  return Math.random().toString(36).substring(2, 9);
};

// Debounce function
export const debounce = (func, wait = 300) => {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
};

// Throttle function
export const throttle = (func, limit = 1000) => {
  let inThrottle;
  return function executedFunction(...args) {
    if (!inThrottle) {
      func(...args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
};

// Copy to clipboard
export const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch (error) {
    console.error('Error copying to clipboard:', error);
    return false;
  }
};

// Check if value is empty
export const isEmpty = (value) => {
  if (value === null || value === undefined) return true;
  if (typeof value === 'string' && value.trim() === '') return true;
  if (Array.isArray(value) && value.length === 0) return true;
  if (typeof value === 'object' && Object.keys(value).length === 0) return true;
  return false;
};

// Get initials from name
export const getInitials = (name) => {
  if (!name) return '?';
  const words = name.split(' ');
  if (words.length === 1) return words[0].charAt(0).toUpperCase();
  return (words[0].charAt(0) + words[words.length - 1].charAt(0)).toUpperCase();
};

// Format date in Persian locale
export const formatDate = (date, options = {}) => {
  if (!date) return '';
  const defaultOptions = {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    ...options
  };
  return new Intl.DateTimeFormat('fa-IR', defaultOptions).format(new Date(date));
};

// Format time ago
export const formatTimeAgo = (date) => {
  if (!date) return '';
  const now = new Date();
  const pastDate = new Date(date);
  const seconds = Math.floor((now - pastDate) / 1000);
  
  const intervals = {
    سال: 31536000,
    ماه: 2592000,
    هفته: 604800,
    روز: 86400,
    ساعت: 3600,
    دقیقه: 60,
    ثانیه: 1
  };
  
  for (const [unit, secondsInUnit] of Object.entries(intervals)) {
    const interval = Math.floor(seconds / secondsInUnit);
    if (interval >= 1) {
      return `${interval} ${unit} پیش`;
    }
  }
  
  return 'همین الان';
};

// Validate email
export const isValidEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

// Validate Persian phone number
export const isValidPersianPhone = (phone) => {
  const phoneRegex = /^(0|\+98)?9\d{9}$/;
  return phoneRegex.test(phone);
};

// Get query param from URL
export const getQueryParam = (param) => {
  if (typeof window !== 'undefined') {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
  }
  return null;
};

// Scroll to element
export const scrollToElement = (elementId) => {
  if (typeof window !== 'undefined') {
    const element = document.getElementById(elementId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }
};

// Check if user is authenticated
export const isAuthenticated = () => {
  if (typeof window !== 'undefined') {
    return !!localStorage.getItem('token');
  }
  return false;
};

// Logout
export const logout = () => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/login';
  }
};

// Get user from localStorage
export const getUser = () => {
  if (typeof window !== 'undefined') {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  }
  return null;
};

// Set user in localStorage
export const setUser = (user) => {
  if (typeof window !== 'undefined') {
    localStorage.setItem('user', JSON.stringify(user));
  }
};

// Set token in localStorage
export const setToken = (token) => {
  if (typeof window !== 'undefined') {
    localStorage.setItem('token', token);
  }
};
