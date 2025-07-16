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
  const [isTyping, setIsTyping] = useState(false);
  // REMOVED: showSuggestions state is no longer needed.

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validate topic
    const validation = newsletterApi.validateTopic(topic);
    if (!validation.isValid) {
      setError(validation.error || 'Invalid topic');
      return;
    }

    setError(null);
    // REMOVED: No need to hide suggestions anymore.
    onSubmit(topic);
  };

  const handleTopicChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newTopic = e.target.value;
    setTopic(newTopic);
    setIsTyping(true);
    
    if (error) {
      setError(null);
    }

    setTimeout(() => setIsTyping(false), 1000);
  };

  // REMOVED: The exampleTopics data array is gone.
  // REMOVED: The fillExample helper function is gone.

  // Animate character count color
  const getCharCountColor = () => {
    const length = topic.length;
    if (length === 0) return 'text-gray-400';
    if (length < 50) return 'text-green-500';
    if (length < 150) return 'text-blue-500';
    if (length < 180) return 'text-yellow-500';
    return 'text-red-500';
  };

  return (
    <div className="w-full max-w-4xl mx-auto">
      {/* Main Input Card */}
      <div className="bg-white rounded-3xl shadow-2xl border border-gray-200 overflow-hidden">
        {/* Header Section */}
        <div className="bg-gradient-to-br from-blue-50 to-purple-50 px-8 py-8 text-center">
          <div className="inline-flex items-center px-4 py-2 rounded-full bg-blue-100 text-blue-800 text-sm font-medium mb-6">
            <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z" clipRule="evenodd" />
            </svg>
            5-Stage AI Pipeline Ready
          </div>
          
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            Generate Your 
            <span className="bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
              {" "}AI Newsletter
            </span>
          </h2>
          
          <p className="text-xl text-gray-600 max-w-2xl mx-auto leading-relaxed">
            Enter any topic and watch our advanced AI create a professional newsletter in under 60 seconds
          </p>
        </div>

        {/* Form Section */}
        <div className="p-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label 
                htmlFor="topic" 
                className="block text-lg font-semibold text-gray-800 mb-4"
              >
                What would you like your newsletter to cover?
              </label>
              
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                  <svg className="h-6 w-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                </div>
                
                <input
                  type="text"
                  id="topic"
                  value={topic}
                  onChange={handleTopicChange}
                  placeholder="e.g., Artificial Intelligence trends, Climate change solutions..."
                  disabled={disabled || isLoading}
                  className={`
                    w-full pl-12 pr-20 py-5 text-lg border-2 rounded-2xl 
                    focus:ring-4 focus:ring-blue-500/20 focus:border-blue-500
                    transition-all duration-300 ease-in-out
                    disabled:bg-gray-50 disabled:cursor-not-allowed
                    placeholder:text-gray-400
                    ${error 
                      ? 'border-red-300 bg-red-50 focus:ring-red-500/20 focus:border-red-500' 
                      : 'border-gray-300 hover:border-gray-400 bg-white'
                    }
                  `}
                  maxLength={200}
                />
                
                {/* Character Count */}
                <div className={`absolute right-4 top-1/2 transform -translate-y-1/2 text-sm font-medium ${getCharCountColor()}`}>
                  {topic.length}/200
                  {isTyping && (
                    <div className="inline-block ml-2 w-1 h-4 bg-blue-500 animate-pulse"></div>
                  )}
                </div>
              </div>
              
              {error && (
                <div className="mt-3 p-3 bg-red-50 border border-red-200 rounded-lg">
                  <p className="text-sm text-red-700 flex items-center">
                    <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                    </svg>
                    {error}
                  </p>
                </div>
              )}
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={disabled || isLoading || !topic.trim()}
              className={`
                w-full py-5 px-8 rounded-2xl font-bold text-lg
                transition-all duration-300 ease-in-out transform
                focus:outline-none focus:ring-4 focus:ring-blue-500/20
                disabled:cursor-not-allowed disabled:transform-none
                ${isLoading || disabled
                  ? 'bg-gray-200 text-gray-500'
                  : 'bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white hover:shadow-2xl hover:scale-[1.02] active:scale-[0.98] hover:-translate-y-1'
                }
              `}
            >
              {isLoading ? (
                <div className="flex items-center justify-center">
                  <svg className="animate-spin -ml-1 mr-3 h-6 w-6 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  <span>Generating Newsletter...</span>
                </div>
              ) : (
                <div className="flex items-center justify-center">
                  <svg className="w-6 h-6 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                  Generate Professional Newsletter
                </div>
              )}
            </button>
          </form>
        </div>

        {/* REMOVED: The entire "Example Topics Section" was here. */}
        
      </div>

      {/* REMOVED: The "Additional Info" text was here. */}
      
    </div>
  );
};

export default TopicInput;