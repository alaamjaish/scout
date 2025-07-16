import axios, { AxiosResponse, AxiosError } from 'axios';
import { 
  NewsletterRequest, 
  NewsletterResponse, 
  HealthResponse, 
  ApiError 
} from '../types/newsletter';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: process.env.NODE_ENV === 'production' 
    ? 'https://your-backend-url.com' 
    : 'http://localhost:8000',
  timeout: 120000, // 2 minutes for newsletter generation
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('❌ API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response: AxiosResponse) => {
    console.log(`✅ API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error: AxiosError) => {
    console.error('❌ API Response Error:', error);
    
    // Handle different error types
    if (error.response) {
      // Server responded with error status
      const responseData = error.response.data as any;
      const apiError: ApiError = {
        detail: responseData?.detail || 'An error occurred',
        status_code: error.response.status,
      };
      return Promise.reject(apiError);
    } else if (error.request) {
      // Request made but no response received
      const apiError: ApiError = {
        detail: 'Network error - Unable to reach the server',
        status_code: 0,
      };
      return Promise.reject(apiError);
    } else {
      // Something else happened
      const apiError: ApiError = {
        detail: error.message || 'An unexpected error occurred',
        status_code: 0,
      };
      return Promise.reject(apiError);
    }
  }
);

// API Service Class
class NewsletterApiService {
  /**
   * Generate a newsletter based on the provided topic
   */
  async generateNewsletter(topic: string): Promise<NewsletterResponse> {
    try {
      const request: NewsletterRequest = { topic: topic.trim() };
      const response = await api.post<NewsletterResponse>('/api/generate-newsletter', request);
      return response.data;
    } catch (error) {
      console.error('Failed to generate newsletter:', error);
      throw error;
    }
  }

  /**
   * Check the health status of the API
   */
  async checkHealth(): Promise<HealthResponse> {
    try {
      const response = await api.get<HealthResponse>('/health');
      return response.data;
    } catch (error) {
      console.error('Failed to check health:', error);
      throw error;
    }
  }

  /**
   * Test API connection
   */
  async testConnection(): Promise<boolean> {
    try {
      await api.get('/api/test-connection');
      return true;
    } catch (error) {
      console.error('Connection test failed:', error);
      return false;
    }
  }

  /**
   * Get API documentation URL
   */
  getDocsUrl(): string {
    const baseUrl = process.env.NODE_ENV === 'production' 
      ? 'https://your-backend-url.com' 
      : 'http://localhost:8000';
    return `${baseUrl}/docs`;
  }

  /**
   * Validate topic before sending to API
   */
  validateTopic(topic: string): { isValid: boolean; error?: string } {
    const trimmedTopic = topic.trim();
    
    if (!trimmedTopic) {
      return { isValid: false, error: 'Topic cannot be empty' };
    }
    
    if (trimmedTopic.length < 1) {
      return { isValid: false, error: 'Topic must be at least 1 character long' };
    }
    
    if (trimmedTopic.length > 200) {
      return { isValid: false, error: 'Topic must be less than 200 characters' };
    }
    
    return { isValid: true };
  }
}

// Export singleton instance
export const newsletterApi = new NewsletterApiService();

// Export types for convenience
export type { NewsletterRequest, NewsletterResponse, HealthResponse, ApiError }; 