import React, { useState } from 'react';
import { AlertTriangle, RefreshCw, Layers, CheckCircle2, Zap, ArrowRight } from 'lucide-react';
import { GapAnalysisReport } from '../types';

interface GapAnalysisTabProps {
  report: GapAnalysisReport;
  isRetraining: boolean;
  onRetrain: (targetVersion: string) => void;
  currentModelVersion: string;
}

export const GapAnalysisTab: React.FC<GapAnalysisTabProps> = ({
  report,
  isRetraining,
  onRetrain,
  currentModelVersion
}) => {
  const [targetVersion, setTargetVersion] = useState('v2.0');

  return (
    <div className="space-y-6">
      
      {/* Header & Stats Overview */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
          <div>
            <h2 className="text-base font-bold text-slate-100 flex items-center space-x-2">
              <AlertTriangle className="w-5 h-5 text-amber-400" />
              <span>Adversarial Gap Analysis & Evasion Clustering</span>
            </h2>
            <p className="text-xs text-slate-400">
              Unsupervised clustering (K-Means) isolating false negative blind spots in current model {currentModelVersion}.
            </p>
          </div>

          <div className="flex items-center space-x-3 font-mono text-xs">
            <div className="px-3 py-1.5 bg-slate-950 border border-slate-800 rounded-lg">
              <span className="text-slate-400">Tested: </span>
              <strong className="text-slate-200">{report.total_tested}</strong>
            </div>
            <div className="px-3 py-1.5 bg-red-950/60 border border-red-800 rounded-lg">
              <span className="text-red-400">Evasions: </span>
              <strong className="text-red-300">{report.evasion_count} ({report.evasion_rate}%)</strong>
            </div>
          </div>
        </div>

        {/* Recommendation Bar */}
        <div className="p-3 bg-amber-950/30 border border-amber-800/60 rounded-lg text-xs text-amber-300 flex items-start space-x-2 font-mono">
          <Zap className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
          <span>{report.recommendation}</span>
        </div>
      </div>

      {/* Evasion Cluster Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {report.clusters.map((cluster) => (
          <div
            key={cluster.cluster_id}
            className="bg-slate-900 border border-slate-800 hover:border-slate-700 rounded-xl p-5 space-y-3 flex flex-col justify-between"
          >
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="font-mono text-xs font-bold text-cyan-400 bg-cyan-950/60 px-2 py-0.5 rounded border border-cyan-800">
                  {cluster.cluster_id}
                </span>
                <span className={`px-2 py-0.5 rounded text-[10px] font-mono font-semibold ${
                  cluster.impact_badge.includes('High')
                    ? 'bg-red-950 text-red-400 border border-red-800'
                    : 'bg-amber-950 text-amber-400 border border-amber-800'
                }`}>
                  {cluster.impact_badge}
                </span>
              </div>

              <div>
                <h4 className="text-sm font-bold text-slate-100">{cluster.title}</h4>
                <span className="text-xs text-slate-400 font-mono">{cluster.dominant_family}</span>
              </div>

              <p className="text-xs text-slate-300 leading-relaxed">{cluster.description}</p>
            </div>

            <div className="space-y-2 pt-3 border-t border-slate-800 font-mono text-xs">
              <div className="flex justify-between text-slate-400">
                <span>Evasions:</span>
                <strong className="text-red-400">{cluster.evasion_count} ({cluster.percentage_of_evasions.toFixed(1)}%)</strong>
              </div>

              <div className="p-2 bg-slate-950 border border-slate-800 rounded text-[11px] text-slate-300">
                <span className="text-slate-400">Weak Feature: </span>
                <span className="text-amber-400 font-semibold">{cluster.weak_feature_label}</span>
              </div>
            </div>

          </div>
        ))}
      </div>

      {/* 1-Click Retraining Action Box */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div>
          <h3 className="text-sm font-bold text-slate-100 flex items-center space-x-2">
            <RefreshCw className="w-4 h-4 text-cyan-400" />
            <span>Automated Counter-Sample Synthesis & Retraining</span>
          </h3>
          <p className="text-xs text-slate-400">
            Synthesizes 300 targeted adversarial counter-samples focused on weak feature centroids to train hardened defense.
          </p>
        </div>

        <div className="flex items-center space-x-3 w-full sm:w-auto">
          <select
            value={targetVersion}
            onChange={(e) => setTargetVersion(e.target.value)}
            className="bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 font-mono focus:outline-none focus:border-cyan-500"
          >
            <option value="v2.0">Target: Defense v2.0</option>
            <option value="v3.0">Target: Defense v3.0 (Robust)</option>
          </select>

          <button
            onClick={() => onRetrain(targetVersion)}
            disabled={isRetraining}
            className={`px-4 py-2 rounded-lg text-xs font-bold font-mono whitespace-nowrap flex items-center space-x-2 transition-all ${
              isRetraining
                ? 'bg-slate-800 text-slate-500 cursor-not-allowed'
                : 'bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 font-extrabold shadow-lg shadow-cyan-500/20'
            }`}
          >
            <RefreshCw className={`w-4 h-4 ${isRetraining ? 'animate-spin' : ''}`} />
            <span>{isRetraining ? 'Retraining Models...' : 'TRIGGER RETRAINING LOOP'}</span>
          </button>
        </div>
      </div>

    </div>
  );
};
