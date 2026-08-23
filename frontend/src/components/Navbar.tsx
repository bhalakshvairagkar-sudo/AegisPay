import React from 'react';
import { Shield, Cpu, Zap, Activity, Database, CheckCircle2 } from 'lucide-react';

interface NavbarProps {
  currentModelVersion: string;
  isDemoMode: boolean;
  onToggleDemoMode: (enabled: boolean) => void;
  onLaunchJudgeDemo: () => void;
  isDemoRunning: boolean;
  demoStep: number;
}

export const Navbar: React.FC<NavbarProps> = ({
  currentModelVersion,
  isDemoMode,
  onToggleDemoMode,
  onLaunchJudgeDemo,
  isDemoRunning,
  demoStep,
}) => {
  return (
    <header className="sticky top-0 z-50 bg-slate-900/90 backdrop-blur border-b border-slate-800 px-4 lg:px-8 py-3">
      <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
        
        {/* Logo & Identity */}
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-gradient-to-br from-cyan-500 to-blue-600 rounded-lg shadow-lg shadow-cyan-500/20 text-slate-950 font-bold flex items-center justify-center">
            <Shield className="w-6 h-6 text-slate-950 stroke-[2.5]" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="text-xl font-extrabold tracking-wider bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 via-teal-300 to-blue-500">
                AEGISPAY
              </span>
              <span className="text-xs px-2 py-0.5 rounded-full bg-cyan-950 border border-cyan-800 text-cyan-400 font-mono font-semibold">
                v2026.1
              </span>
            </div>
            <p className="text-xs text-slate-400 hidden sm:block">
              Adaptive Adversarial AI Lab for Payment Security • Mastercard Innovation Challenge
            </p>
          </div>
        </div>

        {/* Engine Status Badges & Controls */}
        <div className="flex items-center space-x-3 text-xs font-mono">
          {/* Live vs Demo Badge Toggle */}
          <button
            onClick={() => onToggleDemoMode(!isDemoMode)}
            className={`flex items-center space-x-1.5 px-2.5 py-1.5 rounded-md border text-[11px] transition-all ${
              isDemoMode
                ? 'bg-purple-950/60 border-purple-800 text-purple-300'
                : 'bg-emerald-950/60 border-emerald-800 text-emerald-300'
            }`}
            title="Click to toggle between Live Backend and Reproducible Demo Artifact mode"
          >
            {isDemoMode ? (
              <>
                <Database className="w-3.5 h-3.5 text-purple-400" />
                <span>REPRODUCIBLE DEMO ARTIFACT</span>
              </>
            ) : (
              <>
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                <span>LIVE RESEARCH EXPERIMENT</span>
              </>
            )}
          </button>

          {/* Closed Loop Status */}
          <div className="hidden lg:flex items-center space-x-2 px-3 py-1.5 rounded-md bg-slate-800/80 border border-slate-700">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
            <span className="text-slate-300">Loop: <strong className="text-emerald-400">ACTIVE</strong></span>
          </div>

          {/* Active Model Version */}
          <div className="flex items-center space-x-2 px-3 py-1.5 rounded-md bg-slate-800/80 border border-slate-700">
            <Cpu className="w-4 h-4 text-cyan-400" />
            <span className="text-slate-300">Model: <strong className="text-cyan-400">{currentModelVersion}</strong></span>
          </div>

          {/* Judge 1-Click Demo Launcher */}
          <button
            onClick={onLaunchJudgeDemo}
            disabled={isDemoRunning}
            className={`flex items-center space-x-2 px-3.5 py-1.5 rounded-md font-semibold transition-all shadow-md ${
              isDemoRunning
                ? 'bg-amber-500/20 text-amber-400 border border-amber-500/40 animate-pulse'
                : 'bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 shadow-cyan-500/20'
            }`}
          >
            {isDemoRunning ? (
              <>
                <Activity className="w-4 h-4 animate-spin text-amber-400" />
                <span>Demo Step {demoStep}/9...</span>
              </>
            ) : (
              <>
                <Zap className="w-4 h-4 text-slate-950 fill-current" />
                <span>⚡ Judge 1-Click Demo</span>
              </>
            )}
          </button>
        </div>

      </div>
    </header>
  );
};
