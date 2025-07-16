import React, { useState, useEffect } from 'react';
import { newsletterApi, ApiError } from './services/api';
import { ProcessingStage, AppState } from './types/newsletter';
import TopicInput from './components/Newsletter/TopicInput';
import ProcessingStages from './components/Newsletter/ProcessingStages';
import NewsletterOutput from './components/Newsletter/NewsletterOutput';
import './styles/globals.css';

const initialStages: ProcessingStage[] = [
  { id: 'search-planning', name: 'Smart Search Planning', description: 'AI creates targeted search strategies', icon: '🧠', status: 'pending' },
  { id: 'content-research', name: 'Content Research', description: 'Searching the web for relevant information', icon: '🔍', status: 'pending' },
  { id: 'newsletter-creation', name: 'Newsletter Creation', description: 'Crafting the newsletter with AI', icon: '✍️', status: 'pending' },
  { id: 'quality-assessment', name: 'Quality Assessment', description: 'Evaluating quality across multiple metrics', icon: '📊', status: 'pending' },
  { id: 'auto-improvement', name: 'Auto-Improvement', description: 'Refining the newsletter for maximum impact', icon: '🔧', status: 'pending' }
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

  useEffect(() => { checkApiHealth(); }, []);

  const checkApiHealth = async () => {
    try {
      const isHealthy = await newsletterApi.testConnection();
      setApiHealth(isHealthy);
    } catch (error) {
      setApiHealth(false);
    }
  };

  // 1. This function now fully resets the app to its initial state.
  const resetState = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
    setAppState({
      isGenerating: false,
      currentStage: 0,
      stages: initialStages.map(stage => ({ ...stage, status: 'pending' })),
      newsletter: null,
      error: null,
      topic: ''
    });
  };
  
  const handleStreamUpdate = (update: { type: string; data: any }) => {
    if (update.type === 'update') {
      const { stage: stageIndex, status } = update.data;
      setAppState(prev => ({
        ...prev,
        currentStage: stageIndex,
        stages: prev.stages.map((stage, index) => {
          if (index < stageIndex) return { ...stage, status: 'completed' };
          if (index === stageIndex) return { ...stage, status };
          return stage;
        })
      }));
    } else if (update.type === 'final') {
      setAppState(prev => ({
        ...prev,
        isGenerating: false,
        newsletter: update.data as AppState['newsletter'],
      }));
    } else if (update.type === 'error') {
      setAppState(prev => ({
        ...prev,
        isGenerating: false,
        error: update.data.message || 'An error occurred in the generation stream.',
        stages: prev.stages.map((s, i) => i === prev.currentStage ? { ...s, status: 'error' } : s)
      }));
    }
  };

  const handleTopicSubmit = (topic: string) => {
    // Clear previous results and errors before starting a new run
    setAppState(prev => ({
      ...prev,
      isGenerating: true,
      topic,
      error: null,
      newsletter: null, // Clear the old newsletter immediately
      currentStage: 0,
      stages: initialStages.map(stage => ({ ...stage, status: 'pending' }))
    }));
        
    newsletterApi.generateNewsletterStream(
      topic,
      handleStreamUpdate,
      (error) => handleStreamUpdate({ type: 'error', data: error }),
      () => { console.log('Stream finished.'); }
    );
  };

  const handleGenerateAnother = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };
  
  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="fixed top-0 w-full bg-white/95 backdrop-blur-md shadow-sm border-b border-gray-200 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            
            {/* 2. Wrapped the logo and title in a clickable div that calls resetState */}
            <div onClick={resetState} className="flex items-center cursor-pointer" title="Reset to Home">
              <div className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mr-3">🚀</div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">Scout AI</h1>
                <p className="text-sm text-gray-600">Newsletter Generator</p>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              {apiHealth === null ? (
                <div className="flex items-center text-gray-500"><div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse mr-2"></div><span className="text-sm">Connecting...</span></div>
              ) : apiHealth ? (
                <div className="flex items-center text-green-600"><div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div><span className="text-sm font-medium">Online</span></div>
              ) : (
                <div className="flex items-center text-red-600"><div className="w-2 h-2 bg-red-500 rounded-full mr-2"></div><span className="text-sm font-medium">Offline</span><button onClick={checkApiHealth} className="ml-2 text-xs bg-red-100 hover:bg-red-200 text-red-700 px-2 py-1 rounded">Retry</button></div>
              )}
            </div>
          </div>
        </div>
      </nav>
      <main className="pt-24 pb-20 bg-gray-50" id="generator-section">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
          {appState.error && (
            <div className="bg-red-50 border border-red-200 rounded-xl p-6">
              <div className="flex items-center">
                <svg className="w-6 h-6 text-red-600 mr-3" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" /></svg>
                <div>
                  <h3 className="text-red-900 font-semibold text-lg">Generation Failed</h3>
                  <p className="text-red-800">{appState.error}</p>
                </div>
              </div>
              <button onClick={() => setAppState(prev => ({...prev, error: null}))} className="mt-4 bg-red-600 hover:bg-red-700 text-white px-6 py-3 rounded-lg font-semibold transition-colors">Dismiss</button>
            </div>
          )}

          <TopicInput 
            onSubmit={handleTopicSubmit} 
            isLoading={appState.isGenerating} 
            disabled={apiHealth === false} 
          />

          {appState.isGenerating && (
            <ProcessingStages 
              stages={appState.stages} 
              currentStage={appState.currentStage} 
              isProcessing={appState.isGenerating} 
            />
          )}

          {appState.newsletter && !appState.isGenerating && (
             <NewsletterOutput 
                newsletter={appState.newsletter} 
                onNewsletter={handleGenerateAnother} 
              />
          )}
        </div>
      </main>
    </div>
  );
};

export default App;