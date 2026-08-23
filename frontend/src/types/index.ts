export interface AttackVector {
  id: string;
  family: string;
  name: string;
  genAi: boolean;
  sophistication: number;
  severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  detectability: 'VERY LOW' | 'LOW' | 'MEDIUM' | 'HIGH';
  evasionStrategy: string;
  signals: string[];
  description: string;
  mitigationPolicy: string;
}

export interface ScenarioItem {
  scenarioId: string;
  attackId: string;
  family: string;
  name: string;
  genAi: boolean;
  amount: number;
  velocity: number;
  deviceFam: number;
  locationDev: number;
  bioVariance: number;
  difficulty: string;
  mutatedScore: number;
  detected_v1: boolean;
  detected_v2: boolean;
  detected_v3: boolean;
  evadedInV1: boolean;
  evadedInV3: boolean;
  riskScore?: number;
}

export interface ModelBenchmark {
  id: string;
  name: string;
  type: string;
  precision: number;
  recall: number;
  f1: number;
  rocAuc: number;
  prAuc: number;
  fpr: number;
  fnr: number;
  latencyMs: number;
}

export interface EvolutionRound {
  round: number;
  model: string;
  attacksTested: number;
  detected: number;
  evaded: number;
  evasionRate: number;
  f1Score: number;
  topVulnerability: string;
  timestamp: string;
}

export interface FeatureDriver {
  feature: string;
  feature_key: string;
  value: string;
  impact: 'HIGH_RISK' | 'MEDIUM_RISK' | 'SAFE_FACTOR';
  raw_value: number;
  impact_score: number;
}

export interface PredictionResult {
  unifiedRiskScore: number;
  supervisedMlRisk: number;
  anomalyScore: number;
  ruleRisk: number;
  behavioralVariance: number;
  decision: 'ALLOW' | 'STEP-UP 3DS VERIFY' | 'MANUAL REVIEW' | 'BLOCK';
  decisionColor: string;
  modelVersion: string;
  shapDrivers: FeatureDriver[];
  is_live_prediction?: boolean;
}

export interface EvasionCluster {
  cluster_id: string;
  impact_badge: string;
  title: string;
  dominant_family: string;
  evasion_count: number;
  percentage_of_evasions: number;
  weak_feature: string;
  weak_feature_label: string;
  description: string;
  centroid_features: Record<string, number>;
}

export interface GapAnalysisReport {
  total_tested: number;
  evasion_count: number;
  evasion_rate: number;
  clusters: EvasionCluster[];
  recommendation: string;
  evaded_scenarios?: ScenarioItem[];
}

export interface FidelityData {
  fidelityScore: number;
  ksDistanceAmount: number;
  ksPValueAmount: number;
  wassersteinDistanceAmount: number;
  ksDistanceVelocity: number;
  jensenShannonDivergence: number;
  correlationSimilarity: number;
  densityCurve: {
    bins: number[];
    reference: number[];
    synthetic: number[];
  };
  formula_description: string;
}

export interface DashboardData {
  totalAttackVariants: number;
  totalAttackFamilies: number;
  currentModelVersion: string;
  detectionRateF1: string;
  fpr: string;
  robustnessScore: string;
  fidelityScore: string;
  experimentId: string;
  datasetVersion: string;
  seed: number;
  robustnessLevels: Array<{
    level: string;
    v1: number;
    v3: number;
  }>;
}

export interface HoldoutResult {
  family_tested: string;
  primary_vector: string;
  samples_tested: number;
  baselineDetectionRate: number;
  hardenedDetectionRate: number;
  generalizationDelta: number;
}

export interface KnowledgeGraphNode {
  id: string;
  label: string;
  type: string;
  color: string;
}

export interface KnowledgeGraphEdge {
  source: string;
  target: string;
  relation: string;
}

export interface KnowledgeGraphData {
  nodes: KnowledgeGraphNode[];
  edges: KnowledgeGraphEdge[];
}
