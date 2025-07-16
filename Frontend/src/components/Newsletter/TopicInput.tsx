import React, { useState } from 'react';
import { newsletterApi } from '../../services/api';

interface TopicInputProps {
  onSubmit: (topic: string) => void;
  isLoading: boolean;
  disabled?: boolean;
}

const TopicInput: React.FC<TopicInputProps> = ({ onSubmit, isLoading, disabled = false }) => {
  const [topic, setTopic] = useState('');
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validate topic
    const validation = newsletterApi.validateTopic(topic);
    if (!validation.isValid) {
      setError(validation.error || 'Invalid topic');
      return;
    }

    setError(null);
    onSubmit(topic);
  };

  const handleTopicChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newTopic = e.target.value;
    setTopic(newTopic);
    
    // Clear error when user starts typing
    if (error) {
      setError(null);
    }
  };

  const exampleTopics = [
    "Artificial Intelligence Trends 2025",
    "Sustainable Technology Innovations",
    "Remote Work Productivity Tips",
    "Cybersecurity Best Practices",
    "Climate Change Solutions"
  ];

  const fillExample = (example: string) => {
    setTopic(example);
    setError(null);
  };

  return (
    <div className="w-full max-w-2xl mx-auto">
      <div className="bg-white rounded-xl shadow-lg p-8 border border-secondary-200">
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold text-secondary-900 mb-3">
            Generate Your AI Newsletter
          </h2>
          <p className="text-secondary-600 text-lg">
            Enter any topic and watch our 5-stage AI pipeline create a professional newsletter
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label 
              htmlFor="topic" 
              className="block text-sm font-semibold text-secondary-700 mb-3"
            >
              Newsletter Topic
            </label>
            <div className="relative">
              <input
                type="text"
                id="topic"
                value={topic}
                onChange={handleTopicChange}
                placeholder="e.g., Artificial Intelligence, Climate Change, Tech Trends..."
                disabled={disabled || isLoading}
                className={`
                  w-full px-4 py-4 text-lg border-2 rounded-lg 
                  focus:ring-2 focus:ring-primary-500 focus:border-transparent
                  transition-all duration-200 ease-in-out
                  disabled:bg-secondary-50 disabled:cursor-not-allowed
                  ${error 
                    ? 'border-error-300 bg-error-50' 
                    : 'border-secondary-300 hover:border-secondary-400'
                  }
                `}
                maxLength={200}
              />
              <div className="absolute right-3 top-1/2 transform -translate-y-1/2 text-sm text-secondary-400">
                {topic.length}/200
              </div>
            </div>
            
            {error && (
              <p className="mt-2 text-sm text-error-600 flex items-center">
                <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                </svg>
                {error}
              </p>
            )}
          </div>

          <button
            type="submit"
            disabled={disabled || isLoading || !topic.trim()}
            className={`
              w-full py-4 px-6 rounded-lg font-semibold text-lg
              transition-all duration-200 ease-in-out transform
              focus:outline-none focus:ring-4 focus:ring-primary-200
              disabled:cursor-not-allowed disabled:transform-none
              ${isLoading || disabled
                ? 'bg-secondary-300 text-secondary-500'
                : 'bg-gradient-to-r from-primary-600 to-primary-700 hover:from-primary-700 hover:to-primary-800 text-white hover:shadow-lg hover:scale-[1.02] active:scale-[0.98]'
              }
            `}
          >
            {isLoading ? (
              <div className="flex items-center justify-center">
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Generating Newsletter...
              </div>
            ) : (
              <div className="flex items-center justify-center">
                <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
                </svg>
                Generate Newsletter
              </div>
            )}
          </button>
        </form>

        {/* Example Topics */}
        <div className="mt-8">
          <p className="text-sm font-medium text-secondary-700 mb-3">
            Try these example topics:
          </p>
          <div className="flex flex-wrap gap-2">
            {exampleTopics.map((example, index) => (
              <button
                key={index}
                onClick={() => fillExample(example)}
                disabled={disabled || isLoading}
                className="px-3 py-1 text-sm bg-secondary-100 hover:bg-secondary-200 text-secondary-700 rounded-full transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {example}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default TopicInput; 