import React, { useState, useEffect } from 'react';
import { Search, Sliders, Shield, AlertTriangle, CheckCircle2, TrendingUp, Info } from 'lucide-react';
import { PredictionResult } from '../types';
import { api } from '../services/api';

interface SandboxTabProps {
  currentModelVersion: string;
}

export const SandboxTab: React.FC<SandboxTabProps> = ({ currentModelVersion }) => {
  const [amount, setAmount] = useState(450);
  const [velocityCount, setVelocityCount] = useState(4);
  const [deviceFamiliarity, setDeviceFamiliarity] = useState(0.25);
  const [locationDeviationKm, setLocationDeviationKm] = useState(145);
  const [behavioralVariance, setBehavioralVariance] = useState(0.85);
  const [merchantRiskScore, setMerchantRiskScore] = useState(0.70);
  const [accountAgeDays, setAccountAgeDays] = useState(42);

  const [prediction, setPrediction] = useState<PredictionResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  // Compute live prediction whenever parameters change
  useEffect(() => {
    let isCancelled = false;
    const runInference = async () => {
      setIsLoading(true);
      const res = await api.predictTransaction({
        amount,
        velocityCount,
        deviceFamiliarity,
        locationDeviationKm,
        behavioralVariance,
        merchantRiskScore,
        accountAgeDays
      });
      if (!isCancelled) {
        setPrediction(res);
        setIsLoading(false);
      }
    };

    const timer = setTimeout(runInference, 150);
    return () => {
      isCancelled = true;
      clearTimeout(timer);
    };
  }, [amount, velocityCount, deviceFamiliarity, locationDeviationKm, behavioralVariance, merchantRiskScore, accountAgeDays]);

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
          <div>
            <h2 className="text-base font-bold text-slate-100 flex items-center space-x-2">
              <Search className="w-5 h-5 text-cyan-400" />
              <span>Real-Time Transaction Sandbox & SHAP Explainability Engine</span>
            </h2>
            <p className="text-xs text-slate-400">
              Interactive transaction risk inference with authentic TreeExplainer feature attributions.
            </p>
          </div>
          <span className="px-3 py-1 bg-cyan-950 border border-cyan-800 text-cyan-400 font-mono text-xs rounded-full font-semibold">
            Inference: Model {currentModelVersion}
          </span>
        </div>
      </div>

      {/* Main Grid: Parameters Sliders vs Prediction & SHAP Breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left Column: Transaction Parameter Sliders (5 cols) */}
        <div className="lg:col-span-5 bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
          <h3 className="text-sm font-bold text-slate-200 flex items-center space-x-2">
            <Sliders className="w-4 h-4 text-cyan-400" />
            <span>Transaction Telemetry Parameters</span>
          </h3>

          <div className="space-y-3.5 text-xs font-mono">
            {/* Amount */}
            <div>
              <div className="flex justify-between text-slate-300 mb-1">
                <span>Transaction Amount:</span>
                <span className="text-cyan-400 font-bold">${amount.toFixed(2)}</span>
              </div>
              <input
                type="range"
                min="1"
                max="2500"
                step="5"
                value={amount}
                onChange={(e) => setAmount(Number(e.target.value))}
                className="w-full accent-cyan-500"
              />
            </div>

            {/* Velocity (1-Hour) */}
            <div>
              <div className="flex justify-between text-slate-300 mb-1">
                <span>1-Hour Transaction Velocity:</span>
                <span className="text-cyan-400 font-bold">{velocityCount} tx/hr</span>
              </div>
              <input
                type="range"
                min="0"
                max="15"
                step="1"
                value={velocityCount}
                onChange={(e) => setVelocityCount(Number(e.target.value))}
                className="w-full accent-cyan-500"
              />
            </div>

            {/* Device Familiarity */}
            <div>
              <div className="flex justify-between text-slate-300 mb-1">
                <span>Device Familiarity Index:</span>
                <span className="text-cyan-400 font-bold">{(deviceFamiliarity * 100).toFixed(0)}%</span>
              </div>
              <input
                type="range"
                min="0.0"
                max="1.0"
                step="0.05"
                value={deviceFamiliarity}
                onChange={(e) => setDeviceFamiliarity(Number(e.target.value))}
                className="w-full accent-cyan-500"
              />
            </div>

            {/* Location Deviation (km) */}
            <div>
              <div className="flex justify-between text-slate-300 mb-1">
                <span>Geolocation Deviation:</span>
                <span className="text-cyan-400 font-bold">{locationDeviationKm} km</span>
              </div>
              <input
                type="range"
                min="0"
                max="1000"
                step="10"
                value={locationDeviationKm}
                onChange={(e) => setLocationDeviationKm(Number(e.target.value))}
                className="w-full accent-cyan-500"
              />
            </div>

            {/* Behavioral Variance */}
            <div>
              <div className="flex justify-between text-slate-300 mb-1">
                <span>Behavioral Biometric Deviation:</span>
                <span className="text-cyan-400 font-bold">{(behavioralVariance * 100).toFixed(0)}%</span>
              </div>
              <input
                type="range"
                min="0.0"
                max="1.0"
                step="0.05"
                value={behavioralVariance}
                onChange={(e) => setBehavioralVariance(Number(e.target.value))}
                className="w-full accent-cyan-500"
              />
            </div>

            {/* Merchant Risk Score */}
            <div>
              <div className="flex justify-between text-slate-300 mb-1">
                <span>Merchant Baseline Risk (MCC):</span>
                <span className="text-cyan-400 font-bold">{(merchantRiskScore * 100).toFixed(0)}%</span>
              </div>
              <input
                type="range"
                min="0.0"
                max="1.0"
                step="0.05"
                value={merchantRiskScore}
                onChange={(e) => setMerchantRiskScore(Number(e.target.value))}
                className="w-full accent-cyan-500"
              />
            </div>

            {/* Account Age (Days) */}
            <div>
              <div className="flex justify-between text-slate-300 mb-1">
                <span>Account Vintage / Age:</span>
                <span className="text-cyan-400 font-bold">{accountAgeDays} days</span>
              </div>
              <input
                type="range"
                min="1"
                max="365"
                step="1"
                value={accountAgeDays}
                onChange={(e) => setAccountAgeDays(Number(e.target.value))}
                className="w-full accent-cyan-500"
              />
            </div>

          </div>
        </div>

        {/* Right Column: Real-time Decision & SHAP Drivers (7 cols) */}
        <div className="lg:col-span-7 space-y-4">
          
          {/* Decision & Risk Score Card */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
              <div>
                <span className="text-xs font-mono text-slate-400">UNIFIED RISK SCORE</span>
                <div className="text-3xl font-black font-mono text-slate-100 flex items-baseline space-x-2">
                  <span>{prediction ? prediction.unifiedRiskScore : 0}</span>
                  <span className="text-xs text-slate-400">/ 100</span>
                </div>
              </div>

              {/* Recommended Decision Badge */}
              <div className="text-right">
                <span className="text-xs font-mono text-slate-400 block mb-1">RECOMMENDED ACTION</span>
                <span className={`px-3 py-1.5 rounded-lg text-xs font-mono font-extrabold border uppercase tracking-wider ${
                  prediction ? prediction.decisionColor : 'bg-slate-800 text-slate-400'
                }`}>
                  {prediction ? prediction.decision : 'EVALUATING...'}
                </span>
              </div>
            </div>

            {/* Sub-Score Breakdown Matrix */}
            {prediction && (
              <div className="grid grid-cols-3 gap-3 pt-3 border-t border-slate-800 text-xs font-mono">
                <div className="p-2.5 bg-slate-950 rounded-lg border border-slate-800">
                  <span className="text-slate-400 text-[10px]">Supervised ML</span>
                  <div className="text-sm font-bold text-cyan-400">{(prediction.supervisedMlRisk).toFixed(1)}%</div>
                </div>

                <div className="p-2.5 bg-slate-950 rounded-lg border border-slate-800">
                  <span className="text-slate-400 text-[10px]">Isolation Forest</span>
                  <div className="text-sm font-bold text-amber-400">{(prediction.anomalyScore * 100).toFixed(1)}%</div>
                </div>

                <div className="p-2.5 bg-slate-950 rounded-lg border border-slate-800">
                  <span className="text-slate-400 text-[10px]">Static Rule Risk</span>
                  <div className="text-sm font-bold text-slate-300">{prediction.ruleRisk.toFixed(0)}%</div>
                </div>
              </div>
            )}
          </div>

          {/* SHAP Feature Attribution Waterfall Card */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-bold text-slate-200 flex items-center space-x-2">
                <TrendingUp className="w-4 h-4 text-cyan-400" />
                <span>SHAP Feature Attribution Breakdown</span>
              </h3>
              <span className="text-[10px] font-mono text-slate-400">TreeExplainer Marginal Values</span>
            </div>

            <p className="text-xs text-slate-400">
              Positive contributions increase fraud risk; negative contributions mitigate risk as safe trust factors.
            </p>

            <div className="space-y-2 pt-2">
              {prediction?.shapDrivers.map((driver, idx) => {
                const isRisk = driver.impact !== 'SAFE_FACTOR';
                return (
                  <div
                    key={idx}
                    className="p-2.5 bg-slate-950 border border-slate-800 rounded-lg flex items-center justify-between text-xs font-mono"
                  >
                    <div>
                      <div className="font-sans font-semibold text-slate-200">{driver.feature}</div>
                      <div className="text-[10px] text-slate-500">{driver.feature_key}</div>
                    </div>

                    <div className="text-right">
                      <span className={`font-bold px-2 py-0.5 rounded text-[11px] ${
                        isRisk
                          ? (driver.impact === 'HIGH_RISK' ? 'bg-red-950 text-red-400 border border-red-800' : 'bg-amber-950 text-amber-400 border border-amber-800')
                          : 'bg-emerald-950 text-emerald-400 border border-emerald-800'
                      }`}>
                        {driver.value}
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>

          </div>

        </div>

      </div>

    </div>
  );
};
