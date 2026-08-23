import React, { useState } from 'react';
import { Target, Search, Filter, Cpu, Shield, AlertTriangle, Network, Info } from 'lucide-react';
import { AttackVector, KnowledgeGraphData } from '../types';

interface TaxonomyTabProps {
  attacks: AttackVector[];
  graphData: KnowledgeGraphData;
}

export const TaxonomyTab: React.FC<TaxonomyTabProps> = ({ attacks, graphData }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedFamily, setSelectedFamily] = useState('ALL');
  const [genAiOnly, setGenAiOnly] = useState(false);
  const [showGraph, setShowGraph] = useState(false);

  const families = [
    'ALL',
    'Account Takeover',
    'Behavioral Impersonation',
    'Social Engineering',
    'Transaction Manipulation',
    'Merchant Abuse',
    'Identity Abuse',
    'Device Spoofing',
    'AI Adaptive Fraud'
  ];

  const filteredAttacks = attacks.filter((a) => {
    const matchesSearch =
      a.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      a.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
      a.description.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesFamily = selectedFamily === 'ALL' || a.family === selectedFamily;
    const matchesGenAi = !genAiOnly || a.genAi;
    return matchesSearch && matchesFamily && matchesGenAi;
  });

  return (
    <div className="space-y-6">
      
      {/* Header & Controls */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 bg-slate-900 border border-slate-800 rounded-xl p-4">
        <div>
          <h2 className="text-lg font-bold text-slate-100 flex items-center space-x-2">
            <Target className="w-5 h-5 text-cyan-400" />
            <span>GenAI Payment Attack Intelligence & Taxonomy (36 Vectors)</span>
          </h2>
          <p className="text-xs text-slate-400">
            Comprehensive knowledge base covering multi-channel payment fraud vectors and synthetic threat signatures.
          </p>
        </div>

        {/* Knowledge Graph Toggle Button */}
        <button
          onClick={() => setShowGraph(!showGraph)}
          className={`flex items-center space-x-2 px-3.5 py-2 rounded-lg text-xs font-semibold font-mono border transition-all ${
            showGraph
              ? 'bg-cyan-950 text-cyan-400 border-cyan-800'
              : 'bg-slate-800 hover:bg-slate-700 text-slate-300 border-slate-700'
          }`}
        >
          <Network className="w-4 h-4 text-cyan-400" />
          <span>{showGraph ? 'Show Attack Cards' : 'View Threat Knowledge Graph'}</span>
        </button>
      </div>

      {/* Interactive Threat Knowledge Graph Modal/View */}
      {showGraph && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-bold text-slate-200 flex items-center space-x-2">
              <Network className="w-4 h-4 text-cyan-400" />
              <span>Multi-Layer Payment Threat Knowledge Graph Topology</span>
            </h3>
            <span className="text-xs font-mono text-slate-400">
              {graphData.nodes.length} Entities • {graphData.edges.length} Causal Edges
            </span>
          </div>

          <div className="h-80 bg-slate-950 rounded-lg border border-slate-800 p-4 relative overflow-hidden flex items-center justify-center">
            {/* SVG Visual Graph Representation */}
            <div className="w-full h-full relative">
              <svg className="w-full h-full">
                {/* Visual lines for sample nodes */}
                <line x1="20%" y1="30%" x2="45%" y2="50%" stroke="#475569" strokeWidth="1.5" strokeDasharray="3 3" />
                <line x1="80%" y1="30%" x2="55%" y2="50%" stroke="#475569" strokeWidth="1.5" strokeDasharray="3 3" />
                <line x1="45%" y1="50%" x2="50%" y2="80%" stroke="#06b6d4" strokeWidth="2" />
                <line x1="55%" y1="50%" x2="50%" y2="80%" stroke="#06b6d4" strokeWidth="2" />
              </svg>

              {/* Positioned Node Badges */}
              <div className="absolute top-[20%] left-[15%] p-2 rounded-lg bg-red-950/80 border border-red-800 text-[11px] font-mono text-red-300">
                Threat: BIO-01 (Keystroke Synthesis)
              </div>

              <div className="absolute top-[20%] right-[15%] p-2 rounded-lg bg-amber-950/80 border border-amber-800 text-[11px] font-mono text-amber-300">
                Threat: SOC-01 (LLM Voice Clone)
              </div>

              <div className="absolute top-[45%] left-[38%] p-2.5 rounded-lg bg-blue-950/80 border border-blue-800 text-[11px] font-mono text-blue-300">
                Signal: Micro-Keystroke & Velocity Telemetry
              </div>

              <div className="absolute bottom-[10%] left-[36%] p-3 rounded-lg bg-cyan-950/90 border border-cyan-500 text-xs font-mono text-cyan-300 shadow-xl shadow-cyan-500/20 font-bold">
                Defense: AegisPay Hybrid v3.0 (Adversarial Hardened)
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Filter Bar */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        {/* Search */}
        <div className="relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search attack vector or signal..."
            className="w-full bg-slate-900 border border-slate-800 rounded-lg pl-9 pr-4 py-2 text-xs text-slate-200 focus:outline-none focus:border-cyan-500"
          />
        </div>

        {/* Family Selector */}
        <div className="relative">
          <Filter className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <select
            value={selectedFamily}
            onChange={(e) => setSelectedFamily(e.target.value)}
            className="w-full bg-slate-900 border border-slate-800 rounded-lg pl-9 pr-4 py-2 text-xs text-slate-200 focus:outline-none focus:border-cyan-500"
          >
            {families.map((f) => (
              <option key={f} value={f}>{f}</option>
            ))}
          </select>
        </div>

        {/* GenAI Filter Toggle */}
        <div className="flex items-center space-x-2 bg-slate-900 border border-slate-800 rounded-lg px-4 py-2">
          <input
            type="checkbox"
            id="genAiToggle"
            checked={genAiOnly}
            onChange={(e) => setGenAiOnly(e.target.checked)}
            className="rounded border-slate-700 text-cyan-500 focus:ring-cyan-500 bg-slate-800"
          />
          <label htmlFor="genAiToggle" className="text-xs text-slate-300 cursor-pointer flex items-center space-x-1.5">
            <Cpu className="w-3.5 h-3.5 text-purple-400" />
            <span>Filter GenAI / LLM-Assisted Vectors Only</span>
          </label>
        </div>
      </div>

      {/* Attack Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredAttacks.map((attack) => (
          <div
            key={attack.id}
            className="bg-slate-900 border border-slate-800 hover:border-slate-700 rounded-xl p-4 space-y-3 transition-colors flex flex-col justify-between"
          >
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="font-mono text-xs font-bold text-cyan-400 bg-cyan-950/60 px-2 py-0.5 rounded border border-cyan-800">
                  {attack.id}
                </span>
                <div className="flex items-center space-x-1.5">
                  {attack.genAi && (
                    <span className="px-1.5 py-0.5 rounded text-[10px] font-mono font-semibold bg-purple-950 text-purple-300 border border-purple-800 flex items-center space-x-1">
                      <Cpu className="w-2.5 h-2.5 text-purple-400" />
                      <span>GenAI</span>
                    </span>
                  )}
                  <span className={`px-1.5 py-0.5 rounded text-[10px] font-mono font-semibold ${
                    attack.severity === 'CRITICAL' ? 'bg-red-950 text-red-400 border border-red-800' :
                    attack.severity === 'HIGH' ? 'bg-amber-950 text-amber-400 border border-amber-800' :
                    'bg-slate-800 text-slate-400 border border-slate-700'
                  }`}>
                    {attack.severity}
                  </span>
                </div>
              </div>

              <div>
                <h4 className="text-sm font-bold text-slate-100">{attack.name}</h4>
                <span className="text-[11px] text-slate-400 font-mono">{attack.family}</span>
              </div>

              <p className="text-xs text-slate-300 leading-relaxed">{attack.description}</p>
            </div>

            <div className="space-y-2 pt-2 border-t border-slate-800">
              <div className="text-[11px] text-slate-400">
                <strong className="text-slate-300">Evasion:</strong> {attack.evasionStrategy}
              </div>

              <div className="flex flex-wrap gap-1">
                {attack.signals.map((sig, idx) => (
                  <span key={idx} className="text-[10px] font-mono bg-slate-950 text-slate-300 px-1.5 py-0.5 rounded border border-slate-800">
                    {sig}
                  </span>
                ))}
              </div>

              <div className="p-2 rounded bg-slate-950 border border-slate-800/80 text-[11px] text-emerald-400/90 font-mono flex items-start space-x-1.5">
                <Shield className="w-3.5 h-3.5 text-emerald-400 shrink-0 mt-0.5" />
                <span><strong>Policy:</strong> {attack.mitigationPolicy}</span>
              </div>
            </div>

          </div>
        ))}
      </div>

    </div>
  );
};
