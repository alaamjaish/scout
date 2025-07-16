import React, { useState } from 'react';
import { NewsletterResponse } from '../../types/newsletter';

interface NewsletterOutputProps {
  newsletter: NewsletterResponse;
  onNewsletter?: () => void;
}

const NewsletterOutput: React.FC<NewsletterOutputProps> = ({ 
  newsletter, 
  onNewsletter 
}) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(newsletter.newsletter);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy text: ', err);
    }
  };

  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleString();
  };

  return (
    <div className="w-full max-w-4xl mx-auto my-8">
      <div className="bg-white rounded-xl shadow-lg border border-secondary-200 overflow-hidden">
        {/* Header */}
        <div className="bg-gradient-to-r from-primary-600 to-primary-700 text-white p-6">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-2xl font-bold mb-2">Your Newsletter is Ready! 🎉</h3>
              <p className="text-primary-100">
                Generated in {newsletter.processing_time.toFixed(1)}s • 
                Quality Score: {newsletter.quality_score}/50 • 
                {formatTimestamp(newsletter.timestamp)}
              </p>
            </div>
            <div className="text-right">
              <div className="text-3xl font-bold">
                {newsletter.quality_score}/50
              </div>
              <div className="text-sm text-primary-100">
                Quality Score
              </div>
            </div>
          </div>
        </div>

        {/* Newsletter Content */}
        <div className="p-6">
          <div className="prose prose-lg max-w-none">
            <div 
              className="bg-secondary-50 rounded-lg p-6 border border-secondary-200 font-serif text-secondary-900 leading-relaxed"
              style={{ minHeight: '400px' }}
            >
              <pre className="whitespace-pre-wrap font-serif text-base leading-relaxed">
                {newsletter.newsletter}
              </pre>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex flex-wrap gap-3 mt-6 pt-4 border-t border-secondary-200">
            <button
              onClick={handleCopy}
              className="flex items-center px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors duration-200"
            >
              {copied ? (
                <>
                  <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                  Copied!
                </>
              ) : (
                <>
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                  </svg>
                  Copy Newsletter
                </>
              )}
            </button>

            <button
              onClick={() => window.print()}
              className="flex items-center px-4 py-2 bg-secondary-600 hover:bg-secondary-700 text-white rounded-lg transition-colors duration-200"
            >
              <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
              </svg>
              Print
            </button>

            {onNewsletter && (
              <button
                onClick={onNewsletter}
                className="flex items-center px-4 py-2 bg-success-600 hover:bg-success-700 text-white rounded-lg transition-colors duration-200"
              >
                <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
                Generate Another
              </button>
            )}
          </div>
        </div>

        {/* Footer Stats */}
        <div className="bg-secondary-50 px-6 py-4 border-t border-secondary-200">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
            <div>
              <div className="text-lg font-semibold text-secondary-900">
                {newsletter.search_strategy.search_queries.length}
              </div>
              <div className="text-sm text-secondary-600">Search Queries</div>
            </div>
            <div>
              <div className="text-lg font-semibold text-secondary-900">
                {newsletter.search_strategy.topic_type}
              </div>
              <div className="text-sm text-secondary-600">Topic Category</div>
            </div>
            <div>
              <div className="text-lg font-semibold text-secondary-900">
                {newsletter.processing_time.toFixed(1)}s
              </div>
              <div className="text-sm text-secondary-600">Processing Time</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NewsletterOutput; 