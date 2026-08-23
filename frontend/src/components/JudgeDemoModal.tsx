import React from 'react';
import { Zap, CheckCircle2, Loader2, X, RefreshCw, Award, ArrowRight } from 'lucide-react';

interface DemoStep {
  step: number;
  title: string;
  status: 'PENDING' | 'RUNNING' | 'COMPLETED';
  details: string;
}

interface JudgeDemoModalProps {
  isOpen: boolean;
  onClose: () => void;
  steps: DemoStep[];
  isCompleted: boolean;
  isRunning: boolean;
  onRunAgain: () => void;
}

export const JudgeDemoModal: React.FC<JudgeDemoModalProps> = ({
  isOpen,
  onClose,
  steps,
  isCompleted,
  isRunning,
  onRunAgain,
}) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-slate-900 border border-slate-700 rounded-2xl max-w-2xl w-full p-6 space-y-5 shadow-2xl shadow-cyan-500/10 max-h-[90vh] flex flex-col justify-between">
        
        {/* Modal Header */}
        <div className="flex items-center justify-between pb-3 border-b border-slate-800">
          <div className="flex items-center space-x-2.5">
            <div className="p-2 bg-gradient-to-br from-cyan-500 to-blue-600 rounded-lg text-slate-950 font-bold">
              <Zap className="w-5 h-5 fill-current" />
            </div>
            <div>
              <h2 className="text-base font-bold text-slate-100 font-sans">
                Mastercard Challenge Judge 1-Click Pipeline Demo
              </h2>
              <p className="text-xs text-slate-400 font-mono">
                Autonomous Closed-Loop Adversarial Defense & Hardening Verification
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Steps Timeline Feed */}
        <div className="space-y-3 overflow-y-auto pr-1 flex-1 max-h-96">
          {steps.map((s) => (
            <div
              key={s.step}
              className={`p-3 rounded-xl border text-xs font-mono transition-all ${
                s.status === 'COMPLETED'
                  ? 'bg-slate-950/80 border-emerald-800/80 text-slate-200'
                  : s.status === 'RUNNING'
                  ? 'bg-cyan-950/50 border-cyan-500 text-cyan-200 animate-pulse'
                  : 'bg-slate-950/40 border-slate-800/60 text-slate-500'
              }`}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2 font-bold font-sans">
                  {s.status === 'COMPLETED' ? (
                    <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                  ) : s.status === 'RUNNING' ? (
                    <Loader2 className="w-4 h-4 text-cyan-400 animate-spin shrink-0" />
                  ) : (
                    <div className="w-4 h-4 rounded-full border border-slate-700 flex items-center justify-center text-[10px] text-slate-500">
                      {s.step}
                    </div>
                  )}
                  <span className={s.status === 'COMPLETED' ? 'text-slate-100' : (s.status === 'RUNNING' ? 'text-cyan-300' : 'text-slate-400')}>
                    Step {s.step}: {s.title}
                  </span>
                </div>

                <span className={`text-[10px] uppercase font-mono font-semibold px-2 py-0.5 rounded ${
                  s.status === 'COMPLETED' ? 'bg-emerald-950 text-emerald-400 border border-emerald-800' :
                  s.status === 'RUNNING' ? 'bg-cyan-950 text-cyan-400 border border-cyan-800' :
                  'bg-slate-900 text-slate-500'
                }`}>
                  {s.status}
                </span>
              </div>

              {s.details && (
                <p className="mt-2 pl-6 text-[11px] text-slate-400 leading-relaxed">
                  {s.details}
                </p>
              )}
            </div>
          ))}
        </div>

        {/* Modal Footer Summary */}
        <div className="pt-3 border-t border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-3">
          {isCompleted ? (
            <div className="flex items-center space-x-2 text-emerald-400 text-xs font-mono font-bold">
              <Award className="w-5 h-5 text-emerald-400" />
              <span>Full Closed Loop Successfully Verified & Hardened!</span>
            </div>
          ) : (
            <div className="text-xs text-slate-400 font-mono">
              {isRunning ? 'Executing ML pipeline in Python backend...' : 'Ready to execute.'}
            </div>
          )}

          <div className="flex items-center space-x-2 w-full sm:w-auto">
            {isCompleted && (
              <button
                onClick={onRunAgain}
                className="px-3.5 py-2 rounded-lg text-xs font-bold font-mono bg-slate-800 hover:bg-slate-700 text-slate-300 transition-colors"
              >
                Re-Run Demo
              </button>
            )}
            <button
              onClick={onClose}
              className="px-4 py-2 rounded-lg text-xs font-bold font-mono bg-cyan-500 hover:bg-cyan-400 text-slate-950 transition-colors w-full sm:w-auto"
            >
              Done / Return to Lab
            </button>
          </div>
        </div>

      </div>
    </div>
  );
};
