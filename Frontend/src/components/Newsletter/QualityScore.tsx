import React from 'react';
import { QualityCheck } from '../../types/newsletter';

interface QualityScoreProps {
  qualityCheck: QualityCheck;
}

const QualityScore: React.FC<QualityScoreProps> = ({ qualityCheck }) => {
  const getScoreColor = (score: number, maxScore: number = 10) => {
    const percentage = (score / maxScore) * 100;
    if (percentage >= 80) return 'text-success-600 bg-success-100 border-success-200';
    if (percentage >= 60) return 'text-warning-600 bg-warning-100 border-warning-200';
    return 'text-error-600 bg-error-100 border-error-200';
  };

  const getTotalScoreColor = (score: number) => {
    if (score >= 40) return 'text-success-600 bg-success-100';
    if (score >= 30) return 'text-warning-600 bg-warning-100';
    return 'text-error-600 bg-error-100';
  };

  const getScoreEmoji = (score: number) => {
    if (score >= 40) return '🏆';
    if (score >= 35) return '✨';
    if (score >= 30) return '👍';
    if (score >= 25) return '😐';
    return '🔧';
  };

  const scoreMetrics = [
    { name: 'Topic Relevance', score: qualityCheck.scores.topic_relevance, icon: '🎯' },
    { name: 'Engagement', score: qualityCheck.scores.engagement, icon: '💫' },
    { name: 'Readability', score: qualityCheck.scores.readability, icon: '📖' },
    { name: 'Informative', score: qualityCheck.scores.informative, icon: '🧠' },
    { name: 'Professional', score: qualityCheck.scores.professional, icon: '💼' },
  ];

  return (
    <div className="w-full max-w-4xl mx-auto my-8">
      <div className="bg-white rounded-xl shadow-lg p-6 border border-secondary-200">
        <div className="text-center mb-6">
          <h3 className="text-2xl font-bold text-secondary-900 mb-2">
            Quality Assessment
          </h3>
          <p className="text-secondary-600">
            AI-powered analysis of your newsletter's quality and effectiveness
          </p>
        </div>

        {/* Overall Score */}
        <div className="text-center mb-8">
          <div className={`inline-flex items-center justify-center w-24 h-24 rounded-full border-4 ${getTotalScoreColor(qualityCheck.total_score)}`}>
            <div className="text-center">
              <div className="text-2xl font-bold">
                {qualityCheck.total_score}
              </div>
              <div className="text-xs font-medium">
                /50
              </div>
            </div>
          </div>
          <div className="mt-3">
            <div className="text-lg font-semibold text-secondary-900 flex items-center justify-center gap-2">
              <span>{getScoreEmoji(qualityCheck.total_score)}</span>
              <span>{qualityCheck.emoji}</span>
            </div>
            <div className="text-sm text-secondary-600 mt-1">
              Overall Quality Score
            </div>
          </div>
        </div>

        {/* Individual Scores */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mb-6">
          {scoreMetrics.map((metric, index) => (
            <div 
              key={index}
              className={`p-4 rounded-lg border-2 ${getScoreColor(metric.score)}`}
            >
              <div className="text-center">
                <div className="text-2xl mb-2">{metric.icon}</div>
                <div className="text-lg font-bold">{metric.score}/10</div>
                <div className="text-sm font-medium">{metric.name}</div>
              </div>
              
              {/* Progress bar */}
              <div className="mt-3">
                <div className="w-full bg-secondary-200 rounded-full h-2">
                  <div 
                    className={`h-2 rounded-full transition-all duration-500 ${
                      metric.score >= 8 ? 'bg-success-500' :
                      metric.score >= 6 ? 'bg-warning-500' :
                      'bg-error-500'
                    }`}
                    style={{ width: `${(metric.score / 10) * 100}%` }}
                  ></div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Analysis Details */}
        <div className="space-y-4">
          <div className="bg-primary-50 rounded-lg p-4 border border-primary-200">
            <h4 className="font-semibold text-primary-900 mb-2 flex items-center">
              <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
              </svg>
              Critical Analysis
            </h4>
            <p className="text-primary-800 leading-relaxed">
              {qualityCheck.critical_analysis}
            </p>
          </div>

          <div className="bg-secondary-50 rounded-lg p-4 border border-secondary-200">
            <h4 className="font-semibold text-secondary-900 mb-2 flex items-center">
              <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clipRule="evenodd" />
              </svg>
              AI Verdict
            </h4>
            <p className="text-secondary-800 leading-relaxed font-medium">
              {qualityCheck.harsh_verdict}
            </p>
          </div>

          {qualityCheck.improvement_suggestions && qualityCheck.improvement_suggestions.length > 0 && (
            <div className="bg-warning-50 rounded-lg p-4 border border-warning-200">
              <h4 className="font-semibold text-warning-900 mb-2 flex items-center">
                <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                </svg>
                Improvement Suggestions
              </h4>
              <ul className="text-warning-800 space-y-1">
                {qualityCheck.improvement_suggestions.map((suggestion, index) => (
                  <li key={index} className="flex items-start">
                    <span className="text-warning-600 mr-2">•</span>
                    <span>{suggestion}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default QualityScore; 