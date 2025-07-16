import axios from 'axios';
import { 
  NewsletterResponse, 
  HealthResponse, 
  ApiError 
} from '../types/newsletter';

// Keep the existing axios instance for non-streaming requests
const api = axios.create({
  baseURL: process.env.NODE_ENV === 'production' 
    ? 'https://your-backend-url.com' 
    : 'http://localhost:8000',
  timeout: 5000,
});

// API Service Class
class NewsletterApiService {
  /**
   * Generates a newsletter by connecting to a streaming endpoint and providing real-time updates.
   * @param topic The topic for the newsletter.
   * @param onUpdate A callback function that receives updates from the stream.
   * @param onError A callback function for handling errors.
   * @param onFinish A callback function that is called when the stream is finished.
   */
  async generateNewsletterStream(
    topic: string,
    onUpdate: (update: any) => void,
    onError: (error: ApiError) => void,
    onFinish: () => void
  ): Promise<void> {
    const baseURL = process.env.NODE_ENV === 'production' 
      ? 'https://your-backend-url.com' 
      : 'http://localhost:8000';
      
    try {
      const response = await fetch(`${baseURL}/api/generate-newsletter`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic }),
      });

      if (!response.body) {
        throw new Error('Response body is missing.');
      }
      
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Server responded with ${response.status}: ${errorText}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) {
          onFinish();
          break;
        }

        const chunk = decoder.decode(value);
        // SSE messages are separated by double newlines
        const lines = chunk.split('\n\n');
        
        for (const line of lines) {
          if (line.trim().startsWith('data:')) {
            const jsonString = line.trim().substring(5);
            if (jsonString) {
              try {
                const parsedData = JSON.parse(jsonString);
                onUpdate(parsedData);
              } catch (e) {
                console.error("Failed to parse stream data JSON:", jsonString);
              }
            }
          }
        }
      }
    } catch (error) {
      console.error('Streaming failed:', error);
      onError({
        detail: error instanceof Error ? error.message : 'An unknown streaming error occurred.',
        status_code: 0,
      });
    }
  }

  /**
   * Test API connection using the axios instance
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
   * Validate topic before sending to API
   */
  validateTopic(topic: string): { isValid: boolean; error?: string } {
    const trimmedTopic = topic.trim();
    if (!trimmedTopic) return { isValid: false, error: 'Topic cannot be empty' };
    if (trimmedTopic.length > 200) return { isValid: false, error: 'Topic must be less than 200 characters' };
    return { isValid: true };
  }
}

// Export singleton instance
export const newsletterApi = new NewsletterApiService();

// Export types for convenience
export type { NewsletterResponse, HealthResponse, ApiError };