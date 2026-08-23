"""
Pydantic Data Schemas for AegisPay API
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class TransactionInput(BaseModel):
    amount: float = Field(default=450.00, ge=0.01)
    velocityCount: int = Field(default=4, ge=0, alias="velocity_1h")
    velocity_1h: Optional[int] = None
    velocity_24h: Optional[int] = 8
    deviceFamiliarity: float = Field(default=0.25, ge=0.0, le=1.0, alias="device_familiarity")
    device_familiarity: Optional[float] = None
    locationDeviationKm: float = Field(default=145.0, ge=0.0, alias="geo_distance_km")
    geo_distance_km: Optional[float] = None
    behavioralVariance: float = Field(default=0.85, ge=0.0, le=1.0, alias="behavioral_deviation")
    behavioral_deviation: Optional[float] = None
    merchantRiskScore: float = Field(default=0.70, ge=0.0, le=1.0, alias="merchant_risk_score")
    merchant_risk_score: Optional[float] = None
    accountAgeDays: int = Field(default=42, ge=1, alias="account_age_days")
    account_age_days: Optional[int] = None
    touch_pressure_deviation: Optional[float] = 0.50
    carrier_change_flag: Optional[int] = 0
    mcc_risk_weight: Optional[float] = 0.20
    hour_of_day: Optional[int] = 14
    is_international: Optional[int] = 0

    class Config:
        populate_by_name = True


class FeatureDriver(BaseModel):
    feature: str
    feature_key: str
    value: str
    impact: str  # 'HIGH_RISK', 'MEDIUM_RISK', 'SAFE_FACTOR'
    raw_value: float
    impact_score: float


class PredictionResponse(BaseModel):
    unifiedRiskScore: int
    supervisedMlRisk: float
    anomalyScore: float
    ruleRisk: float
    behavioralVariance: float
    decision: str  # 'ALLOW', 'STEP-UP 3DS VERIFY', 'MANUAL REVIEW', 'BLOCK'
    decisionColor: str
    modelVersion: str
    shapDrivers: List[FeatureDriver]
    is_live_prediction: bool = True


class AttackGenerationRequest(BaseModel):
    count: int = Field(default=25, ge=1, le=200)
    family_filter: str = "ALL"
    sophistication: float = Field(default=7.5, ge=1.0, le=10.0)
    mutation_strength: float = Field(default=0.4, ge=0.1, le=0.9)
    difficulty: Optional[str] = None


class ScenarioOutput(BaseModel):
    scenarioId: str
    attackId: str
    family: str
    name: str
    genAi: bool
    amount: float
    velocity: int
    deviceFam: float
    locationDev: float
    bioVariance: float
    difficulty: str
    mutatedScore: float
    detected_v1: bool
    detected_v2: bool
    detected_v3: bool
    evadedInV1: bool
    evadedInV3: bool
    riskScore: Optional[int] = None


class AttackGenerationResponse(BaseModel):
    scenarios: List[ScenarioOutput]
    logs: List[str]
    total_generated: int
    evasion_rate_v1: float
    evasion_rate_v3: float


class ModelBenchmarkItem(BaseModel):
    id: str
    name: str
    type: str
    precision: float
    recall: float
    f1: float
    rocAuc: float
    prAuc: float
    fpr: float
    fnr: float
    latencyMs: float


class RetrainRequest(BaseModel):
    target_version: str = "v2.0"
    n_counterexamples: int = 300


class JudgeDemoStepResult(BaseModel):
    step: int
    title: str
    status: str  # 'RUNNING', 'COMPLETED'
    details: str
    artifacts: Optional[Dict[str, Any]] = None
