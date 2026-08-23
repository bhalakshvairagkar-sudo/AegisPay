import React from 'react';
import { Code2, Terminal, Server, Shield, CheckCircle2, FileText } from 'lucide-react';

export const DocsTab: React.FC = () => {
  const endpoints = [
    { method: 'GET', path: '/api/health', desc: 'System status, active model, and closed-loop engine health.' },
    { method: 'GET', path: '/api/attacks/taxonomy', desc: 'Returns all 36 attack vectors and 8 families with GenAI mapping.' },
    { method: 'GET', path: '/api/attacks/graph', desc: 'Returns knowledge graph topology of threat actors, signals, & defenses.' },
    { method: 'POST', path: '/api/attacks/generate', desc: 'Red team generator synthesizing parameterized adversarial scenarios.' },
    { method: 'POST', path: '/api/predict', desc: 'Real-time payment risk scoring & TreeExplainer SHAP attribution waterfall.' },
    { method: 'GET', path: '/api/models/comparison', desc: 'Multi-model benchmark matrix (Rule, RF, XGB, Isolation, Aegis v1-v3).' },
    { method: 'GET', path: '/api/fidelity', desc: 'Calculates statistical fidelity, KS distance, and Wasserstein metric.' },
    { method: 'POST', path: '/api/gap-analysis', desc: 'K-Means clustering on false negatives isolating weak model features.' },
    { method: 'POST', path: '/api/adversarial/retrain', desc: 'Generates targeted counterexamples and hardens active defense model.' },
    { method: 'GET', path: '/api/evolution', desc: 'Multi-round evolutionary progression & zero-shot holdout validation.' },
    { method: 'POST', path: '/api/judge-demo/run', desc: 'Executes the complete 10-step closed loop research pipeline.' },
  ];

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <h2 className="text-base font-bold text-slate-100 flex items-center space-x-2">
          <Code2 className="w-5 h-5 text-cyan-400" />
          <span>AegisPay Research Documentation & REST API Specification</span>
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Complete interface guide for judges, ML researchers, and fraud engineering teams.
        </p>
      </div>

      {/* CLI Reproducibility Box */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3">
        <h3 className="text-sm font-bold text-slate-200 flex items-center space-x-2">
          <Terminal className="w-4 h-4 text-cyan-400" />
          <span>100% Reproducible CLI Benchmark Commands</span>
        </h3>
        <p className="text-xs text-slate-400">
          Execute all experiments and test suites locally with deterministic seeds:
        </p>

        <div className="space-y-2 font-mono text-xs">
          <div className="p-3 bg-slate-950 rounded-lg border border-slate-800 text-slate-300">
            <span className="text-slate-500"># 1. Run Complete End-to-End Closed Loop Experiment Benchmark</span>
            <div className="text-cyan-400 mt-0.5">python scripts/run_full_experiment.py --seed 42 --train-size 1500 --test-size 400</div>
          </div>

          <div className="p-3 bg-slate-950 rounded-lg border border-slate-800 text-slate-300">
            <span className="text-slate-500"># 2. Run Comprehensive Unit & Integration Test Suite (19/19 Tests)</span>
            <div className="text-emerald-400 mt-0.5">python -m pytest backend/tests -v</div>
          </div>

          <div className="p-3 bg-slate-950 rounded-lg border border-slate-800 text-slate-300">
            <span className="text-slate-500"># 3. Start High-Throughput FastAPI REST Backend</span>
            <div className="text-amber-400 mt-0.5">uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload</div>
          </div>
        </div>
      </div>

      {/* REST API Endpoints Specification */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
        <h3 className="text-sm font-bold text-slate-200 flex items-center space-x-2">
          <Server className="w-4 h-4 text-cyan-400" />
          <span>FastAPI Production REST Endpoints</span>
        </h3>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-slate-950 text-slate-400 border-b border-slate-800">
              <tr>
                <th className="p-2.5 w-24">Method</th>
                <th className="p-2.5 w-64">Path</th>
                <th className="p-2.5">Description & Purpose</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {endpoints.map((ep, idx) => (
                <tr key={idx} className="hover:bg-slate-800/30">
                  <td className="p-2.5">
                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                      ep.method === 'GET' ? 'bg-blue-950 text-blue-400 border border-blue-800' : 'bg-emerald-950 text-emerald-400 border border-emerald-800'
                    }`}>
                      {ep.method}
                    </span>
                  </td>
                  <td className="p-2.5 text-cyan-400 font-semibold">{ep.path}</td>
                  <td className="p-2.5 text-slate-300 font-sans text-xs">{ep.desc}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Mastercard Innovation Challenge Compliance Box */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3">
        <h3 className="text-sm font-bold text-slate-200 flex items-center space-x-2">
          <Shield className="w-4 h-4 text-emerald-400" />
          <span>Mastercard Innovation Challenge — Pillars of Excellence</span>
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
          <div className="p-3 bg-slate-950 rounded-lg border border-slate-800 space-y-1">
            <div className="font-bold text-cyan-400">1. Safe Defensive Simulation</div>
            <p className="text-slate-400">
              Models observable fraud behavioral signals without operational malware or illicit instructions.
            </p>
          </div>

          <div className="p-3 bg-slate-950 rounded-lg border border-slate-800 space-y-1">
            <div className="font-bold text-emerald-400">2. Real Closed-Loop ML</div>
            <p className="text-slate-400">
              True adversarial retraining loop with K-Means clustering, counter-sample synthesis, & holdout validation.
            </p>
          </div>

          <div className="p-3 bg-slate-950 rounded-lg border border-slate-800 space-y-1">
            <div className="font-bold text-purple-400">3. Zero Data Leakage</div>
            <p className="text-slate-400">
              Strict isolation of fraud labels and attack metadata from model feature matrices.
            </p>
          </div>
        </div>
      </div>

    </div>
  );
};
