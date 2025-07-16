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

  return (
    <div className="w-full max-w-4xl mx-auto my-8">
      <div className="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
        {/* --- MODIFIED HEADER --- */}
        {/* The header is now simpler and centers the text. */}
        <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-6 text-center">
          <h3 className="text-2xl font-bold">Your Newsletter is Ready! 🎉</h3>
          {/* REMOVED: The extra details like time, quality score, etc. are gone. */}
        </div>
        {/* --- END MODIFIED HEADER --- */}

        {/* Newsletter Content */}
        <div className="p-8">
          <div className="prose prose-lg max-w-none">
            <div 
              className="bg-gray-50 rounded-lg p-6 border border-gray-200 font-serif text-gray-800 leading-relaxed"
              style={{ minHeight: '400px' }}
            >
              <pre className="whitespace-pre-wrap font-serif text-base leading-relaxed">
                {newsletter.newsletter}
              </pre>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex flex-wrap gap-4 mt-6 pt-6 border-t border-gray-200">
            <button
              onClick={handleCopy}
              className="flex items-center px-5 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors duration-200 font-semibold"
            >
              {copied ? (
                <>
                  <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" /></svg>
                  Copied!
                </>
              ) : (
                <>
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" /></svg>
                  Copy Newsletter
                </>
              )}
            </button>

            <button
              onClick={() => window.print()}
              className="flex items-center px-5 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg transition-colors duration-200 font-semibold"
            >
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" /></svg>
              Print
            </button>

            {onNewsletter && (
              <button
                onClick={onNewsletter}
                className="flex items-center px-5 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors duration-200 font-semibold ml-auto"
              >
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" /></svg>
                Generate Another
              </button>
            )}
          </div>
        </div>
        
        {/* REMOVED: The footer stats section is gone. */}
      </div>
    </div>
  );
};

export default NewsletterOutput;