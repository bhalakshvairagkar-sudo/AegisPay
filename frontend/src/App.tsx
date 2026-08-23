import React, { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { TabNavigation } from './components/TabNavigation';
import { DashboardTab } from './components/DashboardTab';
import { TaxonomyTab } from './components/TaxonomyTab';
import { RedTeamTab } from './components/RedTeamTab';
import { BlueTeamTab } from './components/BlueTeamTab';
import { GapAnalysisTab } from './components/GapAnalysisTab';
import { EvolutionTab } from './components/EvolutionTab';
import { SandboxTab } from './components/SandboxTab';
import { FidelityTab } from './components/FidelityTab';
import { DocsTab } from './components/DocsTab';
import { JudgeDemoModal } from './components/JudgeDemoModal';

import { api } from './services/api';
import {
  AttackVector,
  ScenarioItem,
  ModelBenchmark,
  EvolutionRound,
  GapAnalysisReport,
  FidelityData,
  DashboardData,
  HoldoutResult,
  KnowledgeGraphData
} from './types';

import {
  DEMO_DASHBOARD_DATA,
  DEMO_BASELINE_MODELS,
  DEMO_EVOLUTION_ROUNDS,
  DEMO_HOLDOUT_RESULT,
  DEMO_FIDELITY_DATA,
  DEMO_EVASION_CLUSTERS,
  DEMO_KNOWLEDGE_GRAPH
} from './services/mockData';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [isDemoMode, setIsDemoMode] = useState(false);
  const [currentModelVersion, setCurrentModelVersion] = useState('v1.0');

  // Core Data States
  const [dashboardData, setDashboardData] = useState<DashboardData>(DEMO_DASHBOARD_DATA);
  const [attacks, setAttacks] = useState<AttackVector[]>([]);
  const [graphData, setGraphData] = useState<KnowledgeGraphData>(DEMO_KNOWLEDGE_GRAPH);
  const [scenarios, setScenarios] = useState<ScenarioItem[]>([]);
  const [logs, setLogs] = useState<string[]>([]);
  const [models, setModels] = useState<ModelBenchmark[]>(DEMO_BASELINE_MODELS);
  const [gapReport, setGapReport] = useState<GapAnalysisReport>({
    total_tested: 94,
    evasion_count: 9,
    evasion_rate: 9.6,
    clusters: DEMO_EVASION_CLUSTERS,
    recommendation: 'Gap Analysis isolated 9 evasions across 3 clusters. Recommend generating 300 targeted counter-samples.'
  });
  const [evolutionRounds, setEvolutionRounds] = useState<EvolutionRound[]>(DEMO_EVOLUTION_ROUNDS);
  const [holdoutResult, setHoldoutResult] = useState<HoldoutResult>(DEMO_HOLDOUT_RESULT);
  const [fidelityData, setFidelityData] = useState<FidelityData>(DEMO_FIDELITY_DATA);

  // Status States
  const [isGenerating, setIsGenerating] = useState(false);
  const [isRetraining, setIsRetraining] = useState(false);
  const [evasionRateV1, setEvasionRateV1] = useState(9.6);
  const [evasionRateV3, setEvasionRateV3] = useState(1.1);

  // Judge Demo Modal States
  const [isJudgeModalOpen, setIsJudgeModalOpen] = useState(false);
  const [demoSteps, setDemoSteps] = useState<Array<{ step: number; title: string; status: 'PENDING' | 'RUNNING' | 'COMPLETED'; details: string }>>([
    { step: 1, title: 'Identify GenAI Threat Surface', status: 'PENDING', details: 'Load 36 structured vectors across 8 families.' },
    { step: 2, title: 'Synthesize Adversarial Attacks', status: 'PENDING', details: 'Generate 25 mutated payment payloads.' },
    { step: 3, title: 'Evaluate Baseline Defense v1.0', status: 'PENDING', details: 'Execute XGBoost and hybrid classifier.' },
    { step: 4, title: 'Cluster Missed Evasions', status: 'PENDING', details: 'Run K-Means to isolate weak feature centroids.' },
    { step: 5, title: 'Synthesize Targeted Counterexamples', status: 'PENDING', details: 'Synthesize 250 targeted counter-samples.' },
    { step: 6, title: 'Retrain & Harden Defense v2.0', status: 'PENDING', details: 'Execute sample-weighted adversarial training.' },
    { step: 7, title: 'Re-Evaluate on Evasion Surface', status: 'PENDING', details: 'Test hardened defense on previous evasions.' },
    { step: 8, title: 'Evaluate Zero-Shot Unseen Holdout', status: 'PENDING', details: 'Test on strictly reserved ADV-01 attacks.' },
    { step: 9, title: 'Deploy Hardened Defense v3.0', status: 'PENDING', details: 'Activate v3.0 model on live scoring endpoint.' },
  ]);
  const [isJudgeDemoRunning, setIsJudgeDemoRunning] = useState(false);
  const [isJudgeDemoCompleted, setIsJudgeDemoCompleted] = useState(false);
  const [judgeDemoCurrentStep, setJudgeDemoCurrentStep] = useState(1);

  // Load initial backend state
  useEffect(() => {
    const loadInitialData = async () => {
      // 1. Health & Active model
      const health = await api.checkHealth();
      setCurrentModelVersion(health.active_model || 'v1.0');

      // 2. Taxonomy & Graph
      const tax = await api.getTaxonomy();
      if (tax.attacks && tax.attacks.length > 0) setAttacks(tax.attacks);
      const gr = await api.getKnowledgeGraph();
      setGraphData(gr);

      // 3. Dashboard Data
      const dash = await api.getDashboardData();
      setDashboardData(dash);

      // 4. Models
      const m = await api.getModelBenchmarks();
      setModels(m);

      // 5. Gap Report
      const gap = await api.getGapAnalysis();
      setGapReport(gap);

      // 6. Evolution
      const evo = await api.getEvolutionHistory();
      setEvolutionRounds(evo.rounds);
      setHoldoutResult(evo.holdout_evaluation);

      // 7. Fidelity
      const fid = await api.getFidelityMetrics();
      setFidelityData(fid);

      // 8. Generate initial Red Team scenarios batch
      const initialScenarios = await api.generateAttacks({
        count: 25,
        family_filter: 'ALL',
        sophistication: 7.5,
        mutation_strength: 0.45,
        difficulty: 'Hard'
      });
      setScenarios(initialScenarios.scenarios);
      setLogs(initialScenarios.logs);
      setEvasionRateV1(initialScenarios.evasion_rate_v1);
      setEvasionRateV3(initialScenarios.evasion_rate_v3);
    };

    loadInitialData();
  }, [isDemoMode]);

  // Handle Red Team Attack Generation
  const handleGenerateAttacks = async (params: any) => {
    setIsGenerating(true);
    setLogs((prev) => [...prev, `Starting Red Team generation (Count: ${params.count}, Mutation: ${Math.round(params.mutation_strength * 100)}%)...`]);
    try {
      const res = await api.generateAttacks(params);
      setScenarios(res.scenarios);
      setLogs(res.logs);
      setEvasionRateV1(res.evasion_rate_v1);
      setEvasionRateV3(res.evasion_rate_v3);
    } catch (e) {
      console.error(e);
    } finally {
      setIsGenerating(false);
    }
  };

  // Handle Adversarial Retraining
  const handleRetrain = async (targetVer: string) => {
    setIsRetraining(true);
    try {
      const res = await api.executeRetraining(targetVer);
      setCurrentModelVersion(res.retrained_model_version || targetVer);
      // Refresh models & dashboard
      const m = await api.getModelBenchmarks();
      setModels(m);
      const dash = await api.getDashboardData();
      setDashboardData(dash);
      const gap = await api.getGapAnalysis();
      setGapReport(gap);
    } catch (e) {
      console.error(e);
    } finally {
      setIsRetraining(false);
    }
  };

  // Handle Judge 1-Click Demo
  const handleLaunchJudgeDemo = async () => {
    setIsJudgeModalOpen(true);
    setIsJudgeDemoRunning(true);
    setIsJudgeDemoCompleted(false);

    // Run backend real judge demo or animate step-by-step
    const runDemo = async () => {
      const demoResult = await api.runJudgeDemo();
      const serverSteps = demoResult.steps || [];

      for (let i = 0; i < demoSteps.length; i++) {
        setJudgeDemoCurrentStep(i + 1);
        setDemoSteps((prev) =>
          prev.map((step, idx) => {
            if (idx < i) return { ...step, status: 'COMPLETED' };
            if (idx === i) {
              const matchingServerStep = serverSteps.find((s: any) => s.step === i + 1);
              return {
                ...step,
                status: 'RUNNING',
                details: matchingServerStep ? matchingServerStep.details : step.details
              };
            }
            return { ...step, status: 'PENDING' };
          })
        );
        await new Promise((r) => setTimeout(r, 600));
      }

      setDemoSteps((prev) =>
        prev.map((s, idx) => {
          const matchingServerStep = serverSteps.find((item: any) => item.step === idx + 1);
          return {
            ...s,
            status: 'COMPLETED',
            details: matchingServerStep ? matchingServerStep.details : s.details
          };
        })
      );

      setCurrentModelVersion('v3.0');
      setIsJudgeDemoRunning(false);
      setIsJudgeDemoCompleted(true);
    };

    runDemo();
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      
      {/* Top Navbar */}
      <Navbar
        currentModelVersion={currentModelVersion}
        isDemoMode={isDemoMode}
        onToggleDemoMode={(enabled) => {
          setIsDemoMode(enabled);
          api.setDemoMode(enabled);
        }}
        onLaunchJudgeDemo={handleLaunchJudgeDemo}
        isDemoRunning={isJudgeDemoRunning}
        demoStep={judgeDemoCurrentStep}
      />

      {/* Tab Navigation */}
      <TabNavigation activeTab={activeTab} onSelectTab={setActiveTab} />

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-4 lg:p-8">
        {activeTab === 'dashboard' && (
          <DashboardTab
            data={dashboardData}
            recentScenarios={scenarios}
            currentModelVersion={currentModelVersion}
          />
        )}

        {activeTab === 'taxonomy' && (
          <TaxonomyTab attacks={attacks} graphData={graphData} />
        )}

        {activeTab === 'redteam' && (
          <RedTeamTab
            scenarios={scenarios}
            logs={logs}
            isGenerating={isGenerating}
            onGenerate={handleGenerateAttacks}
            evasionRateV1={evasionRateV1}
            evasionRateV3={evasionRateV3}
          />
        )}

        {activeTab === 'blueteam' && (
          <BlueTeamTab models={models} currentModelVersion={currentModelVersion} />
        )}

        {activeTab === 'gapanalysis' && (
          <GapAnalysisTab
            report={gapReport}
            isRetraining={isRetraining}
            onRetrain={handleRetrain}
            currentModelVersion={currentModelVersion}
          />
        )}

        {activeTab === 'evolution' && (
          <EvolutionTab rounds={evolutionRounds} holdoutResult={holdoutResult} />
        )}

        {activeTab === 'inspector' && (
          <SandboxTab currentModelVersion={currentModelVersion} />
        )}

        {activeTab === 'fidelity' && (
          <FidelityTab fidelityData={fidelityData} />
        )}

        {activeTab === 'docs' && (
          <DocsTab />
        )}
      </main>

      {/* Judge 1-Click Demo Modal */}
      <JudgeDemoModal
        isOpen={isJudgeModalOpen}
        onClose={() => setIsJudgeModalOpen(false)}
        steps={demoSteps}
        isCompleted={isJudgeDemoCompleted}
        isRunning={isJudgeDemoRunning}
        onRunAgain={handleLaunchJudgeDemo}
      />

      {/* Footer */}
      <footer className="bg-slate-900 border-t border-slate-800 px-4 py-3 text-center text-xs text-slate-500 font-mono">
        AegisPay Defense Lab © 2026 • Mastercard Innovation Challenge @ GFF 2026 • AI Defense Lab for Payment Security
      </footer>

    </div>
  );
};

export default App;
