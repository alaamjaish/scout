// TypeScript interfaces matching the FastAPI backend schemas

export interface NewsletterRequest {
  topic: string;
}

export interface QualityScore {
  topic_relevance: number;
  engagement: number;
  readability: number;
  informative: number;
  professional: number;
}

export interface QualityCheck {
  total_score: number;
  scores: QualityScore;
  critical_analysis: string;
  harsh_verdict: string;
  improvement_suggestions: string[];
  emoji: string;
}

export interface SearchStrategy {
  topic_type: string;
  search_queries: string[];
  search_strategy: string;
}

export interface NewsletterResponse {
  newsletter: string;
  quality_score: number;
  quality_check: QualityCheck;
  search_strategy: SearchStrategy;
  processing_time: number;
  timestamp: string;
}

export interface HealthResponse {
  status: string;
  timestamp: string;
  api_keys_configured: {
    openai: boolean;
    tavily: boolean;
    resend: boolean;
  };
  version: string;
}

export interface ApiError {
  detail: string;
  status_code: number;
}

// Processing stages for UI
export interface ProcessingStage {
  id: string;
  name: string;
  description: string;
  icon: string;
  status: 'pending' | 'processing' | 'completed' | 'error';
  duration?: number;
  startTime?: Date;
  endTime?: Date;
}

// UI State types
export interface AppState {
  isGenerating: boolean;
  currentStage: number;
  stages: ProcessingStage[];
  newsletter: NewsletterResponse | null;
  error: string | null;
  topic: string;
} 