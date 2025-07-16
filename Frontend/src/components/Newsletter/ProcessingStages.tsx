import React, { useEffect, useRef } from 'react';
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
  // 1. Create a ref to hold an array of the stage DOM elements
  const stageRefs = useRef<(HTMLDivElement | null)[]>([]);

  // 2. This effect runs whenever the currentStage changes
  useEffect(() => {
    // Only scroll if we are actively processing
    if (isProcessing && currentStage < stages.length) {
      stageRefs.current[currentStage]?.scrollIntoView({
        behavior: 'smooth',
        block: 'start', // This brings the element to the top of the screen
      });
    }
  }, [currentStage, isProcessing, stages.length]); // Dependencies for the effect

  const getStageIcon = (stage: ProcessingStage) => {
    switch (stage.status) {
      case 'completed':
        return (
          <svg className="w-6 h-6 text-green-600" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
          </svg>
        );
      case 'processing':
        return (
          <svg className="w-6 h-6 text-blue-600 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        );
      case 'error':
        return (
          <svg className="w-6 h-6 text-red-600" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
          </svg>
        );
      default: // pending
        return (
          <div className="w-6 h-6 rounded-full border-2 border-gray-300 bg-gray-100"></div>
        );
    }
  };

  const getStageStyles = (stage: ProcessingStage) => {
    const baseStyles = "relative flex items-start space-x-4 p-5 rounded-xl transition-all duration-300";
    
    switch (stage.status) {
      case 'completed':
        return `${baseStyles} bg-green-50 border-2 border-green-200`;
      case 'processing':
        return `${baseStyles} bg-blue-50 border-2 border-blue-300 shadow-lg scale-105`;
      case 'error':
        return `${baseStyles} bg-red-50 border-2 border-red-200`;
      default:
        return `${baseStyles} bg-white border-2 border-gray-200`;
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto">
      <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
        <div className="text-center mb-6">
          <h3 className="text-2xl font-bold text-gray-900 mb-2">AI Processing Pipeline</h3>
          <p className="text-gray-600">Watching your newsletter being crafted in real-time...</p>
        </div>

        <div className="space-y-4">
          {stages.map((stage, index) => (
            // 3. Attach the ref for each stage to its corresponding div
            <div 
              key={stage.id} 
              ref={el => stageRefs.current[index] = el}
              className={getStageStyles(stage)}
            >
              <div className="flex-shrink-0 flex items-center justify-center w-12 h-12 rounded-full bg-white border-2 border-gray-200 shadow-sm">
                {getStageIcon(stage)}
              </div>
              <div className="flex-grow min-w-0">
                <h4 className="text-lg font-semibold text-gray-800">{stage.name}</h4>
                <p className="text-gray-600">{stage.description}</p>
              </div>
              <div className="flex-shrink-0 text-3xl opacity-80">{stage.icon}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ProcessingStages;