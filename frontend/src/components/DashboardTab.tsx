import React from 'react';
import { Target, Shield, Zap, Database, RefreshCw, Layers, CheckCircle2, AlertOctagon } from 'lucide-react';
import { DashboardData, ScenarioItem } from '../types';

interface DashboardTabProps {
  data: DashboardData;
  recentScenarios: ScenarioItem[];
  currentModelVersion: string;
}

export const DashboardTab: React.FC<DashboardTabProps> = ({
  data,
  recentScenarios,
  currentModelVersion
}) => {
  return (
    <div className="space-y-6">
      
      {/* Top KPI Metrics Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        
        {/* Metric 1: Attack Intelligence Surface */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-2">
          <div className="flex items-center justify-between text-slate-400 text-xs">
            <span>Attack Intelligence Surface</span>
            <Target className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-2xl font-black font-mono text-slate-100">{data.totalAttackVariants} Variants</div>
          <div className="text-xs text-slate-400 flex items-center space-x-1">
            <span className="text-emerald-400 font-semibold">{data.totalAttackFamilies} Major Families</span>
            <span>• 100% GenAI Mapped</span>
          </div>
        </div>

        {/* Metric 2: Detection Rate */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-2">
          <div className="flex items-center justify-between text-slate-400 text-xs">
            <span>Current Detection Rate (F1)</span>
            <Shield className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-black font-mono text-emerald-400">
            {data.detectionRateF1}
          </div>
          <div className="text-xs text-slate-400 flex items-center space-x-1">
            <span className="text-cyan-400 font-semibold">
              Model {currentModelVersion}
            </span>
            <span>• FPR: {data.fpr}</span>
          </div>
        </div>

        {/* Metric 3: Adversarial Robustness Score */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-2">
          <div className="flex items-center justify-between text-slate-400 text-xs">
            <span>Adversarial Robustness Score</span>
            <Zap className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-2xl font-black font-mono text-amber-400">
            {data.robustnessScore}
          </div>
          <div className="text-xs text-slate-400 flex items-center space-x-1">
            <span>Degradation Resilience Across Levels</span>
          </div>
        </div>

        {/* Metric 4: Synthetic Data Fidelity */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-2">
          <div className="flex items-center justify-between text-slate-400 text-xs">
            <span>Synthetic Data Fidelity</span>
            <Database className="w-4 h-4 text-blue-400" />
          </div>
          <div className="text-2xl font-black font-mono text-blue-400">{data.fidelityScore}</div>
          <div className="text-xs text-slate-400 flex items-center space-x-1">
            <span>Wasserstein / KS-Test Similarity</span>
          </div>
        </div>

      </div>

      {/* Central Architecture Loop Visual Diagram */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2">
          <div>
            <h2 className="text-lg font-bold text-slate-100 flex items-center space-x-2">
              <RefreshCw className="w-5 h-5 text-cyan-400" />
              <span>AegisPay Autonomous Closed-Loop Architecture</span>
            </h2>
            <p className="text-xs text-slate-400">
              Continuous Loop: Attack Generation → Evasion Discovery → Gap Analysis → Targeted Retraining → Unseen Testing
            </p>
          </div>
          <div className="flex items-center space-x-2">
            <span className="px-2.5 py-1 rounded-full text-[11px] font-mono bg-cyan-950 text-cyan-300 border border-cyan-800">
              Exp: {data.experimentId}
            </span>
            <span className="px-2.5 py-1 rounded-full text-[11px] font-mono bg-slate-800 text-slate-300 border border-slate-700">
              Seed: {data.seed}
            </span>
          </div>
        </div>

        {/* Loop Workflow Diagram Cards */}
        <div className="grid grid-cols-1 md:grid-cols-5 gap-3 pt-2">
          
          <div className="p-3 bg-slate-950 border border-red-900/50 rounded-lg text-center space-y-1 hover:border-red-700 transition-colors">
            <div className="text-xs font-bold text-red-400 font-mono">1. RED TEAM</div>
            <div className="text-sm font-semibold text-slate-200">Scenario Generator</div>
            <p className="text-[10px] text-slate-400">Generates adaptive adversarial payment vectors.</p>
          </div>

          <div className="p-3 bg-slate-950 border border-blue-900/50 rounded-lg text-center space-y-1 hover:border-blue-700 transition-colors">
            <div className="text-xs font-bold text-blue-400 font-mono">2. SIMULATOR</div>
            <div className="text-sm font-semibold text-slate-200">Payment Sandbox</div>
            <p className="text-[10px] text-slate-400">Synthesizes users, merchants, & telemetry.</p>
          </div>

          <div className="p-3 bg-slate-950 border border-emerald-900/50 rounded-lg text-center space-y-1 hover:border-emerald-700 transition-colors">
            <div className="text-xs font-bold text-emerald-400 font-mono">3. BLUE TEAM</div>
            <div className="text-sm font-semibold text-slate-200">Hybrid Classifier</div>
            <p className="text-[10px] text-slate-400">XGBoost + Anomaly + Risk Policy scoring.</p>
          </div>

          <div className="p-3 bg-slate-950 border border-amber-900/50 rounded-lg text-center space-y-1 hover:border-amber-700 transition-colors">
            <div className="text-xs font-bold text-amber-400 font-mono">4. GAP ANALYZER</div>
            <div className="text-sm font-semibold text-slate-200">Evasion Clustering</div>
            <p className="text-[10px] text-slate-400">Clusters false negatives to isolate weak features.</p>
          </div>

          <div className="p-3 bg-slate-950 border border-cyan-900/50 rounded-lg text-center space-y-1 hover:border-cyan-700 transition-colors">
            <div className="text-xs font-bold text-cyan-400 font-mono">5. RETRAINING</div>
            <div className="text-sm font-semibold text-slate-200">Hardened Model</div>
            <p className="text-[10px] text-slate-400">Generates counter-samples & updates defense.</p>
          </div>

        </div>
      </div>

      {/* Robustness vs Difficulty Chart & Live Attack Feed */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Robustness Curve Chart Component */}
        <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2">
            <div>
              <h3 className="text-sm font-bold text-slate-200">Detection Rate vs Attack Difficulty Level</h3>
              <p className="text-xs text-slate-400">Real empirical recall as adversarial feature perturbation increases</p>
            </div>
            <div className="flex items-center space-x-3 text-xs font-mono">
              <span className="flex items-center space-x-1">
                <span className="w-2.5 h-2.5 rounded-full bg-slate-500 inline-block"></span>
                <span className="text-slate-400">Defense v1.0</span>
              </span>
              <span className="flex items-center space-x-1">
                <span className="w-2.5 h-2.5 rounded-full bg-cyan-400 inline-block"></span>
                <span className="text-cyan-400">Defense v3.0</span>
              </span>
            </div>
          </div>

          {/* SVG Visual Representation of Robustness Curves */}
          <div className="h-52 w-full bg-slate-950 rounded-lg border border-slate-800 p-4 relative flex items-end justify-between px-6 sm:px-12">
            
            {/* Grid Lines */}
            <div className="absolute inset-0 flex flex-col justify-between p-4 pointer-events-none opacity-20">
              <div className="border-b border-slate-600 w-full"></div>
              <div className="border-b border-slate-600 w-full"></div>
              <div className="border-b border-slate-600 w-full"></div>
            </div>

            {/* Level Bars Comparison */}
            {data.robustnessLevels.map((item, idx) => (
              <div key={idx} className="z-10 flex flex-col items-center space-y-2 h-full justify-end">
                <div className="flex items-end space-x-2 h-36">
                  {/* V1 Bar */}
                  <div 
                    style={{ height: `${Math.max(4, item.v1)}%` }} 
                    className="w-5 bg-slate-600 rounded-t transition-all duration-500 relative group"
                  >
                    <span className="opacity-0 group-hover:opacity-100 absolute -top-6 left-1/2 -translate-x-1/2 bg-slate-800 text-[10px] font-mono px-1 rounded text-slate-300 whitespace-nowrap z-20">
                      v1: {item.v1}%
                    </span>
                  </div>
                  {/* V3 Bar */}
                  <div 
                    style={{ height: `${Math.max(4, item.v3)}%` }} 
                    className="w-5 bg-cyan-500 rounded-t transition-all duration-500 relative group shadow-lg shadow-cyan-500/30"
                  >
                    <span className="opacity-0 group-hover:opacity-100 absolute -top-6 left-1/2 -translate-x-1/2 bg-cyan-900 text-[10px] font-mono px-1 rounded text-cyan-200 whitespace-nowrap z-20">
                      v3: {item.v3}%
                    </span>
                  </div>
                </div>
                <span className="text-[10px] font-mono text-slate-400 text-center">{item.level}</span>
              </div>
            ))}

          </div>
        </div>

        {/* Live Attack Feed Card */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-bold text-slate-200 flex items-center space-x-2">
                <Target className="w-4 h-4 text-red-400" />
                <span>Recent Generated Scenarios</span>
              </h3>
              <span className="text-[10px] font-mono text-slate-400">{recentScenarios.length} active</span>
            </div>

            <div className="space-y-2 max-h-60 overflow-y-auto pr-1 mt-3">
              {recentScenarios.length === 0 ? (
                <div className="p-4 text-center text-xs text-slate-500 font-mono">
                  No scenarios loaded yet. Run Red Team generator to simulate attacks.
                </div>
              ) : (
                recentScenarios.slice(0, 5).map((scn) => (
                  <div key={scn.scenarioId} className="p-2.5 bg-slate-950 border border-slate-800 rounded-lg text-xs space-y-1">
                    <div className="flex items-center justify-between">
                      <span className="font-mono text-slate-400">{scn.scenarioId}</span>
                      <span className={`px-1.5 py-0.5 rounded text-[10px] font-mono font-semibold ${
                        scn.difficulty === 'Adversarial' ? 'bg-red-950 text-red-400 border border-red-800' : 'bg-amber-950 text-amber-400 border border-amber-800'
                      }`}>
                        {scn.difficulty}
                      </span>
                    </div>
                    <div className="font-semibold text-slate-200 truncate">{scn.name}</div>
                    <div className="flex items-center justify-between text-[10px] text-slate-400 font-mono">
                      <span>Amt: ${scn.amount.toFixed(2)}</span>
                      <span>
                        Def v1: {scn.detected_v1 ? <span className="text-emerald-400 font-bold">DETECTED</span> : <span className="text-red-400 font-bold">EVADED</span>}
                      </span>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>

          <div className="pt-2 border-t border-slate-800 text-[11px] font-mono text-slate-400 flex justify-between">
            <span>Model: {currentModelVersion}</span>
            <span className="text-cyan-400">Dataset: {data.datasetVersion}</span>
          </div>
        </div>

      </div>

    </div>
  );
};
