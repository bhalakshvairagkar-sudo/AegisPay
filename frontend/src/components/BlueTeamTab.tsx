import React from 'react';
import { Shield, Cpu, Activity, AlertCircle, CheckCircle, Sliders, Layers } from 'lucide-react';
import { ModelBenchmark } from '../types';

interface BlueTeamTabProps {
  models: ModelBenchmark[];
  currentModelVersion: string;
}

export const BlueTeamTab: React.FC<BlueTeamTabProps> = ({ models, currentModelVersion }) => {
  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
          <div>
            <h2 className="text-base font-bold text-slate-100 flex items-center space-x-2">
              <Shield className="w-5 h-5 text-emerald-400" />
              <span>Blue Team Defense & Model Performance Benchmark Matrix</span>
            </h2>
            <p className="text-xs text-slate-400">
              Rigorous, independently evaluated performance metrics across legacy rules, baseline ML, and AegisPay adversarial models.
            </p>
          </div>
          <span className="px-3 py-1 bg-cyan-950 border border-cyan-800 text-cyan-400 font-mono text-xs rounded-full font-semibold">
            Active: Model {currentModelVersion}
          </span>
        </div>
      </div>

      {/* Model Benchmark Matrix Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-bold text-slate-200 flex items-center space-x-2">
            <Cpu className="w-4 h-4 text-cyan-400" />
            <span>Multi-Model Evaluation Matrix</span>
          </h3>
          <span className="text-xs font-mono text-slate-400">{models.length} Models Evaluated</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-slate-950 text-slate-400 border-b border-slate-800">
              <tr>
                <th className="p-3">Model Architecture</th>
                <th className="p-3">Type</th>
                <th className="p-3 text-right">Precision</th>
                <th className="p-3 text-right">Recall</th>
                <th className="p-3 text-right">F1-Score</th>
                <th className="p-3 text-right">ROC-AUC</th>
                <th className="p-3 text-right">PR-AUC</th>
                <th className="p-3 text-right">FPR</th>
                <th className="p-3 text-right">FNR</th>
                <th className="p-3 text-right">Latency</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {models.map((m) => {
                const isAegis = m.id.startsWith('aegispay');
                return (
                  <tr
                    key={m.id}
                    className={`transition-colors ${
                      isAegis
                        ? 'bg-cyan-950/20 hover:bg-cyan-950/40 font-semibold'
                        : 'hover:bg-slate-800/30'
                    }`}
                  >
                    <td className="p-3">
                      <div className={`font-sans ${isAegis ? 'text-cyan-300 font-bold' : 'text-slate-200'}`}>
                        {m.name}
                      </div>
                      <div className="text-[10px] text-slate-400 font-mono">{m.id}</div>
                    </td>
                    <td className="p-3 text-slate-400">{m.type}</td>
                    <td className="p-3 text-right text-slate-200">{(m.precision * 100).toFixed(1)}%</td>
                    <td className="p-3 text-right text-slate-200">{(m.recall * 100).toFixed(1)}%</td>
                    <td className={`p-3 text-right font-bold ${
                      m.f1 > 0.90 ? 'text-emerald-400' : (m.f1 > 0.70 ? 'text-amber-400' : 'text-rose-400')
                    }`}>
                      {(m.f1 * 100).toFixed(1)}%
                    </td>
                    <td className="p-3 text-right text-slate-300">{(m.rocAuc * 100).toFixed(1)}%</td>
                    <td className="p-3 text-right text-slate-300">{(m.prAuc * 100).toFixed(1)}%</td>
                    <td className="p-3 text-right text-slate-300">{(m.fpr * 100).toFixed(2)}%</td>
                    <td className="p-3 text-right text-slate-300">{(m.fnr * 100).toFixed(1)}%</td>
                    <td className="p-3 text-right text-cyan-400 font-bold">{m.latencyMs}ms</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* Unified Risk Policy Threshold Cards */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
        <div>
          <h3 className="text-sm font-bold text-slate-200 flex items-center space-x-2">
            <Sliders className="w-4 h-4 text-cyan-400" />
            <span>AegisPay Unified Risk Engine & Policy Decision Gating</span>
          </h3>
          <p className="text-xs text-slate-400">
            Real-time multi-dimensional scoring mapping into automated payment challenge and block actions.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
          
          {/* Allow */}
          <div className="p-3.5 bg-emerald-950/40 border border-emerald-800/80 rounded-lg space-y-1.5">
            <div className="flex items-center justify-between text-xs font-mono font-bold text-emerald-400">
              <span>SCORE: 0 - 29</span>
              <CheckCircle className="w-4 h-4 text-emerald-400" />
            </div>
            <div className="text-sm font-bold text-emerald-300 font-sans">ALLOW (Frictionless)</div>
            <p className="text-[11px] text-slate-400">Standard legitimate cardholder payment flow without step-up auth.</p>
          </div>

          {/* Step-Up */}
          <div className="p-3.5 bg-cyan-950/40 border border-cyan-800/80 rounded-lg space-y-1.5">
            <div className="flex items-center justify-between text-xs font-mono font-bold text-cyan-400">
              <span>SCORE: 30 - 59</span>
              <Activity className="w-4 h-4 text-cyan-400" />
            </div>
            <div className="text-sm font-bold text-cyan-300 font-sans">STEP-UP 3DS VERIFY</div>
            <p className="text-[11px] text-slate-400">Frictionless 3DS or biometric confirmation challenge triggered.</p>
          </div>

          {/* Manual Review */}
          <div className="p-3.5 bg-amber-950/40 border border-amber-800/80 rounded-lg space-y-1.5">
            <div className="flex items-center justify-between text-xs font-mono font-bold text-amber-400">
              <span>SCORE: 60 - 79</span>
              <AlertCircle className="w-4 h-4 text-amber-400" />
            </div>
            <div className="text-sm font-bold text-amber-300 font-sans">MANUAL FRAUD REVIEW</div>
            <p className="text-[11px] text-slate-400">Routed to security operations console for fraud analyst inspection.</p>
          </div>

          {/* Block */}
          <div className="p-3.5 bg-rose-950/40 border border-rose-800/80 rounded-lg space-y-1.5">
            <div className="flex items-center justify-between text-xs font-mono font-bold text-rose-400">
              <span>SCORE: 80 - 100</span>
              <Shield className="w-4 h-4 text-rose-400" />
            </div>
            <div className="text-sm font-bold text-rose-300 font-sans">SILENT IMMEDIATE BLOCK</div>
            <p className="text-[11px] text-slate-400">High confidence malicious fraud vector blocked at network gateway.</p>
          </div>

        </div>
      </div>

    </div>
  );
};
