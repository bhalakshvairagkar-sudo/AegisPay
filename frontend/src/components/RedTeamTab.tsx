import React, { useState } from 'react';
import { Zap, Play, Terminal, Layers, CheckCircle2, XCircle, AlertTriangle, Shield } from 'lucide-react';
import { ScenarioItem } from '../types';

interface RedTeamTabProps {
  scenarios: ScenarioItem[];
  logs: string[];
  isGenerating: boolean;
  onGenerate: (params: {
    count: number;
    family_filter: string;
    sophistication: number;
    mutation_strength: number;
    difficulty?: string;
  }) => void;
  evasionRateV1: number;
  evasionRateV3: number;
}

export const RedTeamTab: React.FC<RedTeamTabProps> = ({
  scenarios,
  logs,
  isGenerating,
  onGenerate,
  evasionRateV1,
  evasionRateV3
}) => {
  const [count, setCount] = useState(25);
  const [familyFilter, setFamilyFilter] = useState('ALL');
  const [sophistication, setSophistication] = useState(7.5);
  const [mutationStrength, setMutationStrength] = useState(0.45);
  const [difficulty, setDifficulty] = useState('Hard');

  const families = [
    'ALL',
    'Account Takeover',
    'Behavioral Impersonation',
    'Social Engineering',
    'Transaction Manipulation',
    'Merchant Abuse',
    'Identity Abuse',
    'Device Spoofing'
  ];

  const handleRun = () => {
    onGenerate({
      count,
      family_filter: familyFilter,
      sophistication,
      mutation_strength: mutationStrength,
      difficulty
    });
  };

  return (
    <div className="space-y-6">
      
      {/* Top Generator Controls & Terminal Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Controls Card */}
        <div className="lg:col-span-5 bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
          <div>
            <h2 className="text-base font-bold text-slate-100 flex items-center space-x-2">
              <Zap className="w-5 h-5 text-red-400" />
              <span>Red Team Adversarial Generator</span>
            </h2>
            <p className="text-xs text-slate-400">
              Parametric synthetic scenario synthesizer with dynamic feature mutation vectors.
            </p>
          </div>

          <div className="space-y-3 text-xs">
            {/* Family Selector */}
            <div>
              <label className="block text-slate-300 font-semibold mb-1">Target Attack Family</label>
              <select
                value={familyFilter}
                onChange={(e) => setFamilyFilter(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-red-500 font-mono"
              >
                {families.map((f) => (
                  <option key={f} value={f}>{f}</option>
                ))}
              </select>
            </div>

            {/* Difficulty Preset */}
            <div>
              <label className="block text-slate-300 font-semibold mb-1">Difficulty Level</label>
              <div className="grid grid-cols-4 gap-1.5 font-mono">
                {['Easy', 'Moderate', 'Hard', 'Adversarial'].map((lvl) => (
                  <button
                    key={lvl}
                    type="button"
                    onClick={() => {
                      setDifficulty(lvl);
                      if (lvl === 'Easy') setMutationStrength(0.15);
                      if (lvl === 'Moderate') setMutationStrength(0.35);
                      if (lvl === 'Hard') setMutationStrength(0.60);
                      if (lvl === 'Adversarial') setMutationStrength(0.85);
                    }}
                    className={`py-1.5 rounded text-[11px] border transition-colors ${
                      difficulty === lvl
                        ? 'bg-red-950 text-red-400 border-red-800 font-bold'
                        : 'bg-slate-950 text-slate-400 border-slate-800 hover:text-slate-200'
                    }`}
                  >
                    {lvl}
                  </button>
                ))}
              </div>
            </div>

            {/* Scenario Count Slider */}
            <div>
              <div className="flex justify-between text-slate-300 mb-1">
                <span>Generation Batch Size:</span>
                <span className="font-mono text-cyan-400">{count} scenarios</span>
              </div>
              <input
                type="range"
                min="5"
                max="100"
                step="5"
                value={count}
                onChange={(e) => setCount(Number(e.target.value))}
                className="w-full accent-cyan-500"
              />
            </div>

            {/* Mutation Strength Slider */}
            <div>
              <div className="flex justify-between text-slate-300 mb-1">
                <span>Adversarial Perturbation Scale:</span>
                <span className="font-mono text-red-400">{Math.round(mutationStrength * 100)}%</span>
              </div>
              <input
                type="range"
                min="0.1"
                max="0.9"
                step="0.05"
                value={mutationStrength}
                onChange={(e) => setMutationStrength(Number(e.target.value))}
                className="w-full accent-red-500"
              />
            </div>
          </div>

          <button
            onClick={handleRun}
            disabled={isGenerating}
            className={`w-full py-2.5 rounded-lg text-xs font-bold font-mono flex items-center justify-center space-x-2 transition-all ${
              isGenerating
                ? 'bg-slate-800 text-slate-500 cursor-not-allowed'
                : 'bg-gradient-to-r from-red-600 to-rose-700 hover:from-red-500 hover:to-rose-600 text-white shadow-lg shadow-red-600/20'
            }`}
          >
            <Play className={`w-4 h-4 fill-current ${isGenerating ? 'animate-spin' : ''}`} />
            <span>{isGenerating ? 'Synthesizing Attacks...' : 'EXECUTE RED TEAM GENERATION'}</span>
          </button>
        </div>

        {/* Terminal Execution Log & Evasion Stats */}
        <div className="lg:col-span-7 bg-slate-900 border border-slate-800 rounded-xl p-5 flex flex-col justify-between space-y-4">
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-bold text-slate-200 flex items-center space-x-2">
                <Terminal className="w-4 h-4 text-cyan-400" />
                <span>Adversarial Synthesis Terminal</span>
              </h3>
              <span className="text-[11px] font-mono text-emerald-400">STATUS: READY</span>
            </div>

            {/* Terminal Window */}
            <div className="bg-slate-950 rounded-lg p-3 border border-slate-800 font-mono text-xs text-slate-300 h-44 overflow-y-auto space-y-1">
              <div className="text-slate-500">[SYSTEM] AegisPay Red Team Engine v2026.1 initialized.</div>
              {logs.map((log, idx) => (
                <div key={idx} className="text-cyan-400 flex items-start space-x-1.5">
                  <span className="text-slate-600">❯</span>
                  <span>{log}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Evasion Rate Comparison Badge Bar */}
          <div className="grid grid-cols-2 gap-3 pt-2 border-t border-slate-800">
            <div className="p-2.5 bg-slate-950 rounded-lg border border-slate-800 text-center">
              <div className="text-[11px] text-slate-400">Baseline v1.0 Evasion Rate</div>
              <div className="text-lg font-black font-mono text-red-400">{evasionRateV1}%</div>
            </div>

            <div className="p-2.5 bg-slate-950 rounded-lg border border-slate-800 text-center">
              <div className="text-[11px] text-slate-400">Hardened v3.0 Evasion Rate</div>
              <div className="text-lg font-black font-mono text-emerald-400">{evasionRateV3}%</div>
            </div>
          </div>

        </div>

      </div>

      {/* Generated Scenarios Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-base font-bold text-slate-100 flex items-center space-x-2">
              <Layers className="w-4 h-4 text-cyan-400" />
              <span>Synthesized Adversarial Scenarios Matrix</span>
            </h3>
            <p className="text-xs text-slate-400">
              Transaction payloads mutated against fraud models with genuine detection vs evasion outcomes.
            </p>
          </div>
          <span className="text-xs font-mono text-slate-400">{scenarios.length} Scenarios</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-slate-950 text-slate-400 border-b border-slate-800">
              <tr>
                <th className="p-2.5">Scenario ID</th>
                <th className="p-2.5">Attack Name / Family</th>
                <th className="p-2.5">Amount</th>
                <th className="p-2.5">Velocity</th>
                <th className="p-2.5">Device Fam</th>
                <th className="p-2.5">Bio Dev</th>
                <th className="p-2.5">Difficulty</th>
                <th className="p-2.5">Def v1.0</th>
                <th className="p-2.5">Def v3.0</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {scenarios.length === 0 ? (
                <tr>
                  <td colSpan={9} className="p-6 text-center text-slate-500">
                    No scenarios synthesized yet. Click 'Execute Red Team Generation' above.
                  </td>
                </tr>
              ) : (
                scenarios.map((s) => (
                  <tr key={s.scenarioId} className="hover:bg-slate-800/30 transition-colors">
                    <td className="p-2.5 text-cyan-400 font-semibold">{s.scenarioId}</td>
                    <td className="p-2.5">
                      <div className="font-sans font-semibold text-slate-200">{s.name}</div>
                      <div className="text-[10px] text-slate-400">{s.family}</div>
                    </td>
                    <td className="p-2.5 text-slate-200">${s.amount.toFixed(2)}</td>
                    <td className="p-2.5 text-slate-300">{s.velocity} tx/h</td>
                    <td className="p-2.5 text-slate-300">{s.deviceFam.toFixed(2)}</td>
                    <td className="p-2.5 text-slate-300">{s.bioVariance.toFixed(2)}</td>
                    <td className="p-2.5">
                      <span className={`px-1.5 py-0.5 rounded text-[10px] ${
                        s.difficulty === 'Adversarial' ? 'bg-red-950 text-red-400 border border-red-800' :
                        s.difficulty === 'Hard' ? 'bg-amber-950 text-amber-400 border border-amber-800' :
                        'bg-slate-800 text-slate-300'
                      }`}>
                        {s.difficulty}
                      </span>
                    </td>
                    <td className="p-2.5">
                      {s.detected_v1 ? (
                        <span className="text-emerald-400 font-bold flex items-center space-x-1">
                          <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                          <span>DETECTED</span>
                        </span>
                      ) : (
                        <span className="text-red-400 font-bold flex items-center space-x-1">
                          <XCircle className="w-3.5 h-3.5 text-red-400" />
                          <span>EVADED</span>
                        </span>
                      )}
                    </td>
                    <td className="p-2.5">
                      {s.detected_v3 ? (
                        <span className="text-emerald-400 font-bold flex items-center space-x-1">
                          <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                          <span>DETECTED</span>
                        </span>
                      ) : (
                        <span className="text-amber-400 font-bold flex items-center space-x-1">
                          <XCircle className="w-3.5 h-3.5 text-amber-400" />
                          <span>EVADED</span>
                        </span>
                      )}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
};
