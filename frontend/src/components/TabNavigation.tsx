import React from 'react';
import {
  BarChart3,
  Target,
  Zap,
  Shield,
  AlertTriangle,
  RefreshCw,
  Search,
  Database,
  Code2
} from 'lucide-react';

interface TabNavigationProps {
  activeTab: string;
  onSelectTab: (tabId: string) => void;
}

export const TabNavigation: React.FC<TabNavigationProps> = ({ activeTab, onSelectTab }) => {
  const tabs = [
    { id: 'dashboard', label: 'Dashboard', icon: BarChart3 },
    { id: 'taxonomy', label: 'Attack Intelligence', icon: Target },
    { id: 'redteam', label: 'Red Team Lab', icon: Zap },
    { id: 'blueteam', label: 'Blue Team Defense', icon: Shield },
    { id: 'gapanalysis', label: 'Gap Analysis', icon: AlertTriangle },
    { id: 'evolution', label: 'Closed-Loop Evolution', icon: RefreshCw },
    { id: 'inspector', label: 'Tx Sandbox', icon: Search },
    { id: 'fidelity', label: 'Data Fidelity', icon: Database },
    { id: 'docs', label: 'Architecture & API', icon: Code2 },
  ];

  return (
    <nav className="bg-slate-900 border-b border-slate-800 px-4 lg:px-8 overflow-x-auto">
      <div className="max-w-7xl mx-auto flex space-x-1 py-2">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => onSelectTab(tab.id)}
              className={`flex items-center space-x-2 px-3.5 py-2 rounded-lg text-xs font-medium whitespace-nowrap transition-colors ${
                isActive
                  ? 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/30'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
              }`}
            >
              <Icon className={`w-4 h-4 ${isActive ? 'text-cyan-400' : 'text-slate-400'}`} />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>
    </nav>
  );
};
