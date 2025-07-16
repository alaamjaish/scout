import React, { useState, useEffect } from 'react';
import { newsletterApi, ApiError } from './services/api';
import { ProcessingStage, AppState } from './types/newsletter';
import TopicInput from './components/Newsletter/TopicInput';
import ProcessingStages from './components/Newsletter/ProcessingStages';
import NewsletterOutput from './components/Newsletter/NewsletterOutput';
import QualityScore from './components/Newsletter/QualityScore';
import './styles/globals.css';

// Define the 5-stage processing pipeline
const initialStages: ProcessingStage[] = [
  {
    id: 'search-planning',
    name: 'Smart Search Planning',
    description: 'AI analyzes your topic and creates targeted search strategies',
    icon: '🧠',
    status: 'pending'
  },
  {
    id: 'content-research',
    name: 'Content Research',
    description: 'Searching the web for the latest and most relevant information',
    icon: '🔍',
    status: 'pending'
  },
  {
    id: 'newsletter-creation',
    name: 'Newsletter Creation',
    description: 'Crafting your professional newsletter with AI-powered writing',
    icon: '✍️',
    status: 'pending'
  },
  {
    id: 'quality-assessment',
    name: 'Quality Assessment',
    description: 'Evaluating newsletter quality across multiple metrics',
    icon: '📊',
    status: 'pending'
  },
  {
    id: 'auto-improvement',
    name: 'Auto-Improvement',
    description: 'Refining and enhancing the newsletter for maximum impact',
    icon: '🔧',
    status: 'pending'
  }
];

const App: React.FC = () => {
  const [appState, setAppState] = useState<AppState>({
    isGenerating: false,
    currentStage: 0,
    stages: initialStages,
    newsletter: null,
    error: null,
    topic: ''
  });

  const [apiHealth, setApiHealth] = useState<boolean | null>(null);

  // Check API health on component mount
  useEffect(() => {
    checkApiHealth();
  }, []);

  const checkApiHealth = async () => {
    try {
      const isHealthy = await newsletterApi.testConnection();
      setApiHealth(isHealthy);
    } catch (error) {
      setApiHealth(false);
    }
  };

  const resetState = () => {
    setAppState({
      isGenerating: false,
      currentStage: 0,
      stages: initialStages.map(stage => ({ ...stage, status: 'pending' })),
      newsletter: null,
      error: null,
      topic: ''
    });
  };

  const updateStageStatus = (stageIndex: number, status: ProcessingStage['status'], duration?: number) => {
    setAppState(prev => ({
      ...prev,
      stages: prev.stages.map((stage, index) => 
        index === stageIndex 
          ? { 
              ...stage, 
              status, 
              duration,
              endTime: status === 'completed' ? new Date() : stage.endTime,
              startTime: status === 'processing' ? new Date() : stage.startTime
            }
          : stage
      ),
      currentStage: status === 'completed' ? stageIndex + 1 : stageIndex
    }));
  };

  const simulateProcessingStages = async () => {
    const stageDurations = [2.3, 18.7, 12.1, 3.8, 11.2]; // Realistic durations
    
    for (let i = 0; i < initialStages.length; i++) {
      updateStageStatus(i, 'processing');
      
      // Simulate processing time
      await new Promise(resolve => setTimeout(resolve, 1000)); // Visual feedback delay
      
      updateStageStatus(i, 'completed', stageDurations[i]);
      
      // Small delay between stages
      if (i < initialStages.length - 1) {
        await new Promise(resolve => setTimeout(resolve, 500));
      }
    }
  };

  const handleTopicSubmit = async (topic: string) => {
    setAppState(prev => ({
      ...prev,
      isGenerating: true,
      topic,
      error: null,
      newsletter: null,
      currentStage: 0,
      stages: initialStages.map(stage => ({ ...stage, status: 'pending' }))
    }));

    try {
      // Start the visual processing simulation
      const processingPromise = simulateProcessingStages();
      
      // Start the actual API call
      const apiPromise = newsletterApi.generateNewsletter(topic);
      
      // Wait for both to complete
      const [newsletter] = await Promise.all([apiPromise, processingPromise]);
      
      setAppState(prev => ({
        ...prev,
        isGenerating: false,
        newsletter,
        error: null
      }));

    } catch (error) {
      const apiError = error as ApiError;
      
      // Mark current stage as error
      setAppState(prev => ({
        ...prev,
        isGenerating: false,
        error: apiError.detail || 'An unexpected error occurred',
        stages: prev.stages.map((stage, index) => 
          index === prev.currentStage 
            ? { ...stage, status: 'error' }
            : stage
        )
      }));
    }
  };

  const handleGenerateAnother = () => {
    resetState();
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-secondary-50 via-white to-primary-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-secondary-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <div className="text-2xl font-bold text-primary-600 mr-3">🚀</div>
              <div>
                <h1 className="text-xl font-bold text-secondary-900">
                  Scout AI Newsletter Generator
                </h1>
                <p className="text-sm text-secondary-600">
                  Professional AI-powered newsletter creation
                </p>
              </div>
            </div>
            
            {/* API Health Indicator */}
            <div className="flex items-center space-x-2">
              {apiHealth === null ? (
                <div className="flex items-center text-secondary-500">
                  <div className="w-2 h-2 bg-secondary-400 rounded-full animate-pulse mr-2"></div>
                  <span className="text-sm">Checking connection...</span>
                </div>
              ) : apiHealth ? (
                <div className="flex items-center text-success-600">
                  <div className="w-2 h-2 bg-success-500 rounded-full mr-2"></div>
                  <span className="text-sm font-medium">API Connected</span>
                </div>
              ) : (
                <div className="flex items-center text-error-600">
                  <div className="w-2 h-2 bg-error-500 rounded-full mr-2"></div>
                  <span className="text-sm font-medium">API Offline</span>
                  <button 
                    onClick={checkApiHealth}
                    className="ml-2 text-xs bg-error-100 hover:bg-error-200 text-error-700 px-2 py-1 rounded"
                  >
                    Retry
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Error Message */}
        {appState.error && (
          <div className="mb-8 bg-error-50 border border-error-200 rounded-lg p-4">
            <div className="flex items-center">
              <svg className="w-5 h-5 text-error-600 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
              <div>
                <h3 className="text-error-900 font-semibold">Generation Failed</h3>
                <p className="text-error-800">{appState.error}</p>
              </div>
            </div>
            <button
              onClick={resetState}
              className="mt-3 bg-error-600 hover:bg-error-700 text-white px-4 py-2 rounded-lg text-sm transition-colors"
            >
              Try Again
            </button>
          </div>
        )}

        {/* Topic Input */}
        {!appState.newsletter && (
          <TopicInput 
            onSubmit={handleTopicSubmit}
            isLoading={appState.isGenerating}
            disabled={apiHealth === false}
          />
        )}

        {/* Processing Stages */}
        {(appState.isGenerating || appState.newsletter) && (
          <ProcessingStages 
            stages={appState.stages}
            currentStage={appState.currentStage}
            isProcessing={appState.isGenerating}
          />
        )}

        {/* Newsletter Output */}
        {appState.newsletter && (
          <div className="space-y-8">
            <NewsletterOutput 
              newsletter={appState.newsletter}
              onNewsletter={handleGenerateAnother}
            />
            
            <QualityScore 
              qualityCheck={appState.newsletter.quality_check}
            />
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-secondary-50 border-t border-secondary-200 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div>
              <h3 className="text-lg font-semibold text-secondary-900 mb-3">
                Architecture
              </h3>
              <ul className="space-y-2 text-sm text-secondary-600">
                <li>• FastAPI Backend (Python)</li>
                <li>• React Frontend (TypeScript)</li>
                <li>• 5-Stage AI Pipeline</li>
                <li>• Real-time Processing</li>
              </ul>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold text-secondary-900 mb-3">
                AI Technologies
              </h3>
              <ul className="space-y-2 text-sm text-secondary-600">
                <li>• OpenAI GPT-4 Integration</li>
                <li>• Tavily Search API</li>
                <li>• Smart Quality Assessment</li>
                <li>• Auto-improvement System</li>
              </ul>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold text-secondary-900 mb-3">
                Features
              </h3>
              <ul className="space-y-2 text-sm text-secondary-600">
                <li>• Professional Newsletter Generation</li>
                <li>• Quality Scoring & Analysis</li>
                <li>• Responsive Design</li>
                <li>• Copy & Share Functionality</li>
              </ul>
            </div>
          </div>
          
          <div className="border-t border-secondary-200 pt-6 mt-6 text-center">
            <p className="text-secondary-600 text-sm">
              Built with modern technologies for professional newsletter generation
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default App; 