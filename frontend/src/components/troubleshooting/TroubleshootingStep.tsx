import React from 'react';
import { TroubleshootingStepItem } from '../../types';
import { CheckCircle2, AlertTriangle, ArrowRight, ShieldAlert } from 'lucide-react';

interface TroubleshootingStepProps {
  step: TroubleshootingStepItem;
  isActive: boolean;
  isCompleted: boolean;
  onComplete?: () => void;
}

export const TroubleshootingStep: React.FC<TroubleshootingStepProps> = ({
  step,
  isActive,
  isCompleted,
  onComplete
}) => {
  return (
    <div className={`p-5 rounded-xl border transition-all ${
      isActive 
        ? 'bg-white border-blue-500 shadow-md ring-2 ring-blue-500/10'
        : isCompleted 
          ? 'bg-slate-50 border-emerald-200 opacity-90'
          : 'bg-white border-slate-200 opacity-60'
    }`}>
      <div className="flex items-start gap-4">
        {/* Step indicator */}
        <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm flex-shrink-0 ${
          isCompleted 
            ? 'bg-emerald-500 text-white' 
            : isActive 
              ? 'bg-blue-600 text-white' 
              : 'bg-slate-200 text-slate-600'
        }`}>
          {isCompleted ? <CheckCircle2 className="w-5 h-5" /> : step.stepNumber}
        </div>

        <div className="flex-1">
          <div className="flex items-center justify-between">
            <h4 className="font-bold text-slate-900 text-base">Step {step.stepNumber}: Action Required</h4>
            {isActive && (
              <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-blue-50 text-blue-700 border border-blue-200 animate-pulse">
                Active Step
              </span>
            )}
          </div>

          <p className="mt-2 text-sm text-slate-800 font-medium leading-relaxed">
            {step.action}
          </p>

          <div className="mt-3 p-3 bg-slate-50 rounded-lg border border-slate-200 text-xs text-slate-600">
            <span className="font-bold text-slate-700">Expected Outcome: </span>
            {step.expectedOutcome}
          </div>

          {/* Safety Warning if present */}
          {step.safetyWarning && (
            <div className="mt-3 p-3 bg-rose-50 border border-rose-200 rounded-lg text-xs text-rose-800 flex items-start gap-2">
              <ShieldAlert className="w-4 h-4 text-rose-600 flex-shrink-0 mt-0.5" />
              <div>
                <span className="font-bold">LOTO / Safety Warning: </span>
                {step.safetyWarning}
              </div>
            </div>
          )}

          {/* Action button if active */}
          {isActive && onComplete && (
            <div className="mt-4 flex justify-end">
              <button
                onClick={onComplete}
                className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold text-xs rounded-lg shadow-sm transition-colors cursor-pointer"
              >
                <span>Confirm Action Completed</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
