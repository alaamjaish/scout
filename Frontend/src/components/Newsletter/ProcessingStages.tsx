import React from 'react';
import { ProcessingStage } from '../../types/newsletter';

interface ProcessingStagesProps {
  stages: ProcessingStage[];
  currentStage: number;
  isProcessing: boolean;
}

const ProcessingStages: React.FC<ProcessingStagesProps> = ({ 
  stages, 
  currentStage, 
  isProcessing 
}) => {
  const getStageIcon = (stage: ProcessingStage) => {
    switch (stage.status) {
      case 'completed':
        return (
          <svg className="w-6 h-6 text-success-600" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
          </svg>
        );
      case 'processing':
        return (
          <svg className="w-6 h-6 text-primary-600 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        );
      case 'error':
        return (
          <svg className="w-6 h-6 text-error-600" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
          </svg>
        );
      default: // pending
        return (
          <div className="w-6 h-6 rounded-full border-2 border-secondary-300 bg-secondary-100"></div>
        );
    }
  };

  const getStageStyles = (stage: ProcessingStage, index: number) => {
    const baseStyles = "relative flex items-center p-4 rounded-lg transition-all duration-300";
    
    switch (stage.status) {
      case 'completed':
        return `${baseStyles} bg-success-50 border-2 border-success-200`;
      case 'processing':
        return `${baseStyles} bg-primary-50 border-2 border-primary-200 shadow-lg`;
      case 'error':
        return `${baseStyles} bg-error-50 border-2 border-error-200`;
      default:
        return `${baseStyles} bg-secondary-50 border-2 border-secondary-200`;
    }
  };

  const formatDuration = (duration?: number) => {
    if (!duration) return '';
    return duration >= 1 ? `${duration.toFixed(1)}s` : `${(duration * 1000).toFixed(0)}ms`;
  };

  if (!isProcessing && stages.every(stage => stage.status === 'pending')) {
    return null;
  }

  return (
    <div className="w-full max-w-4xl mx-auto my-8">
      <div className="bg-white rounded-xl shadow-lg p-6 border border-secondary-200">
        <div className="text-center mb-6">
          <h3 className="text-2xl font-bold text-secondary-900 mb-2">
            AI Processing Pipeline
          </h3>
          <p className="text-secondary-600">
            Watch your newsletter being crafted through our 5-stage AI system
          </p>
        </div>

        <div className="space-y-4">
          {stages.map((stage, index) => (
            <div key={stage.id} className={getStageStyles(stage, index)}>
              {/* Progress connector line */}
              {index < stages.length - 1 && (
                <div className="absolute left-8 top-16 w-0.5 h-8 bg-secondary-200"></div>
              )}

              <div className="flex items-start space-x-4 w-full">
                {/* Stage Icon */}
                <div className="flex-shrink-0 flex items-center justify-center w-12 h-12 rounded-full bg-white border-2 border-secondary-200">
                  {getStageIcon(stage)}
                </div>

                {/* Stage Content */}
                <div className="flex-grow min-w-0">
                  <div className="flex items-center justify-between mb-1">
                    <h4 className="text-lg font-semibold text-secondary-900">
                      {stage.name}
                    </h4>
                    {stage.duration && (
                      <span className="text-sm font-medium text-secondary-500">
                        {formatDuration(stage.duration)}
                      </span>
                    )}
                  </div>
                  
                  <p className="text-secondary-600 mb-2">
                    {stage.description}
                  </p>

                  {/* Status indicator */}
                  <div className="flex items-center space-x-2">
                    <span className={`
                      px-2 py-1 text-xs font-medium rounded-full
                      ${stage.status === 'completed' ? 'bg-success-100 text-success-700' :
                        stage.status === 'processing' ? 'bg-primary-100 text-primary-700' :
                        stage.status === 'error' ? 'bg-error-100 text-error-700' :
                        'bg-secondary-100 text-secondary-600'
                      }
                    `}>
                      {stage.status === 'completed' ? '✓ Completed' :
                       stage.status === 'processing' ? '⚡ Processing...' :
                       stage.status === 'error' ? '❌ Error' :
                       '⏳ Pending'
                      }
                    </span>
                  </div>
                </div>

                {/* Stage emoji/icon */}
                <div className="flex-shrink-0 text-2xl">
                  {stage.icon}
                </div>
              </div>

              {/* Processing animation overlay */}
              {stage.status === 'processing' && (
                <div className="absolute inset-0 bg-gradient-to-r from-primary-400/10 to-primary-600/10 rounded-lg animate-pulse"></div>
              )}
            </div>
          ))}
        </div>

        {/* Overall progress bar */}
        <div className="mt-6 pt-4 border-t border-secondary-200">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-secondary-700">
              Overall Progress
            </span>
            <span className="text-sm font-medium text-secondary-700">
              {Math.round((stages.filter(s => s.status === 'completed').length / stages.length) * 100)}%
            </span>
          </div>
          <div className="w-full bg-secondary-200 rounded-full h-2">
            <div 
              className="bg-gradient-to-r from-primary-500 to-primary-600 h-2 rounded-full transition-all duration-500 ease-in-out"
              style={{ 
                width: `${(stages.filter(s => s.status === 'completed').length / stages.length) * 100}%` 
              }}
            ></div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProcessingStages; 