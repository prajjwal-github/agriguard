import React, { useState } from 'react';
import {
  CheckCircle2,
  AlertTriangle,
  FileDown,
  RotateCcw,
  Eye,
  ShieldCheck,
  Activity,
  Layers,
  Thermometer,
  BookOpen,
  Info,
  HelpCircle,
} from 'lucide-react';
import type { PredictionResult } from '../services/api';

interface DiagnosisResultProps {
  result: PredictionResult;
  uploadedImageUrl: string | null;
  onReset: () => void;
}

export const DiagnosisResult: React.FC<DiagnosisResultProps> = ({
  result,
  uploadedImageUrl,
  onReset,
}) => {
  const [showGradCam, setShowGradCam] = useState(true);

  const confidencePct = Math.round(result.confidence * 100);

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 print:p-0">
      {/* Top Banner Action */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 print:hidden">
        <div>
          <span className="text-xs font-bold text-agri-700 uppercase tracking-wider bg-agri-100 px-2.5 py-0.5 rounded-full">
            Step 4 of 4 — Complete Diagnosis
          </span>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 mt-1">
            Plant Pathology Assessment
          </h2>
        </div>

        <div className="flex items-center gap-2.5">
          <button
            onClick={handlePrint}
            className="px-4 py-2 rounded-xl text-xs font-bold bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 transition flex items-center gap-1.5 shadow-sm"
          >
            <FileDown className="w-4 h-4 text-slate-500" /> Export / Print Report
          </button>
          <button
            onClick={onReset}
            className="px-4 py-2 rounded-xl text-xs font-bold bg-agri-600 text-white hover:bg-agri-700 transition flex items-center gap-1.5 shadow-sm"
          >
            <RotateCcw className="w-4 h-4" /> Diagnose Another
          </button>
        </div>
      </div>

      {/* Uncertainty Alert if Unreliable */}
      {!result.is_reliable && (
        <div className="p-4 sm:p-5 rounded-2xl bg-amber-50 border-2 border-amber-300 flex items-start gap-4 text-amber-900">
          <AlertTriangle className="w-6 h-6 text-amber-600 flex-shrink-0 mt-0.5" />
          <div className="space-y-1 text-sm">
            <h4 className="font-bold text-amber-950">Diagnostic Uncertainty Warning</h4>
            <p className="text-amber-800 leading-relaxed">
              The model detected high entropy ({result.entropy.toFixed(2)}) or low diagnostic confidence ({confidencePct}%).
              This photograph may be blurred, out-of-distribution, or contain non-target objects. Please review the guidance below or consult an agronomist before applying chemical treatments.
            </p>
          </div>
        </div>
      )}

      {/* Primary Diagnosis Card */}
      <div className="bg-white rounded-3xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="p-6 sm:p-8 bg-gradient-to-br from-slate-50 to-white border-b border-slate-100">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div className="flex items-center gap-2 text-xs font-semibold text-slate-500">
              <span className="uppercase tracking-wider">{result.category.replace(/_/g, ' ')}</span>
              <span>•</span>
              <span className="text-slate-700 font-bold uppercase tracking-wider">{result.crop.replace(/_/g, ' ')}</span>
              <span>•</span>
              <span className="text-slate-400">ID: {result.prediction_id}</span>
            </div>

            <div className="flex items-center gap-2">
              <span className="text-xs text-slate-500">Inference Latency:</span>
              <span className="text-xs font-bold text-slate-700">{result.processing_time_ms} ms</span>
            </div>
          </div>

          <div className="mt-4 flex flex-col md:flex-row md:items-center justify-between gap-6">
            <div>
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider block mb-1">
                Detected Condition
              </span>
              <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900">
                {result.display_name}
              </h1>
              <p className="text-sm font-medium text-slate-500 mt-1 italic">
                Organ Part: {result.plant_part.toUpperCase()}
              </p>
            </div>

            {/* Confidence Gauge */}
            <div className="p-4 rounded-2xl bg-white border border-slate-200 flex items-center gap-4 min-w-[200px] shadow-sm">
              <div className="relative w-14 h-14 flex items-center justify-center">
                <svg className="w-14 h-14 transform -rotate-90">
                  <circle
                    cx="28"
                    cy="28"
                    r="24"
                    stroke="#e2e8f0"
                    strokeWidth="5"
                    fill="transparent"
                  />
                  <circle
                    cx="28"
                    cy="28"
                    r="24"
                    stroke={confidencePct >= 70 ? '#16a34a' : confidencePct >= 50 ? '#d97706' : '#dc2626'}
                    strokeWidth="5"
                    strokeDasharray={150}
                    strokeDashoffset={150 - (150 * confidencePct) / 100}
                    strokeLinecap="round"
                    fill="transparent"
                  />
                </svg>
                <span className="absolute text-xs font-black text-slate-900">
                  {confidencePct}%
                </span>
              </div>
              <div>
                <span className="text-xs font-bold text-slate-900 block">
                  {confidencePct >= 70 ? 'High Confidence' : confidencePct >= 50 ? 'Moderate' : 'Uncertain'}
                </span>
                <span className="text-[11px] text-slate-500 block">Softmax probability</span>
              </div>
            </div>
          </div>
        </div>

        {/* Visual Inspection & Grad-CAM Heatmap */}
        <div className="p-6 sm:p-8 border-b border-slate-100">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
              <Eye className="w-4 h-4 text-agri-600" />
              <span>Image Attention & Visual Verification</span>
            </h3>
            {result.gradcam_heatmap && (
              <button
                onClick={() => setShowGradCam(!showGradCam)}
                className="text-xs font-bold text-agri-700 hover:text-agri-800 flex items-center gap-1.5"
              >
                <Layers className="w-3.5 h-3.5" />
                <span>{showGradCam ? 'Hide Heatmap' : 'Show Grad-CAM Heatmap'}</span>
              </button>
            )}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-1.5">
              <span className="text-[11px] font-bold text-slate-500 uppercase tracking-wider block">
                Uploaded Leaf Photograph
              </span>
              <div className="rounded-2xl overflow-hidden border border-slate-200 bg-slate-950 aspect-video flex items-center justify-center">
                {uploadedImageUrl ? (
                  <img src={uploadedImageUrl} alt="Uploaded" className="w-full h-full object-contain" />
                ) : (
                  <span className="text-xs text-slate-400">Image Preview</span>
                )}
              </div>
            </div>

            <div className="space-y-1.5">
              <span className="text-[11px] font-bold text-slate-500 uppercase tracking-wider block">
                Grad-CAM Neural Attention Overlay
              </span>
              <div className="rounded-2xl overflow-hidden border border-slate-200 bg-slate-950 aspect-video flex items-center justify-center relative">
                {result.gradcam_heatmap && showGradCam ? (
                  <img
                    src={`data:image/jpeg;base64,${result.gradcam_heatmap}`}
                    alt="Grad-CAM"
                    className="w-full h-full object-contain"
                  />
                ) : (
                  <div className="p-4 text-center text-xs text-slate-400">
                    {result.gradcam_heatmap
                      ? 'Heatmap hidden'
                      : 'Attention heatmap unavailable for low-confidence or rejected predictions.'}
                  </div>
                )}
              </div>
            </div>
          </div>

          <p className="mt-3 text-[11px] text-slate-500 italic flex items-center gap-1">
            <Info className="w-3.5 h-3.5 flex-shrink-0" />
            Notice: Grad-CAM heatmap illustrates the convolutional feature activations influencing the model decision. It is an explanation aid, not a laboratory lesion demarcation.
          </p>
        </div>

        {/* Severity Assessment & Alternative Predictions */}
        <div className="grid grid-cols-1 md:grid-cols-2 divide-y md:divide-y-0 md:divide-x divide-slate-100 border-b border-slate-100">
          {/* Severity */}
          <div className="p-6 sm:p-8 space-y-4">
            <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
              <Thermometer className="w-4 h-4 text-agri-600" />
              <span>Severity Estimation</span>
            </h3>

            <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-slate-500">Estimated Level:</span>
                <span
                  className={`text-xs font-bold px-2.5 py-0.5 rounded-full ${
                    result.severity.level === 'Mild'
                      ? 'bg-blue-100 text-blue-800'
                      : result.severity.level === 'Moderate'
                      ? 'bg-amber-100 text-amber-800'
                      : result.severity.level === 'Severe'
                      ? 'bg-rose-100 text-rose-800'
                      : 'bg-slate-200 text-slate-700'
                  }`}
                >
                  {result.severity.level || 'Unavailable'}
                </span>
              </div>

              {result.severity.lesion_percentage !== null && (
                <div className="flex items-center justify-between">
                  <span className="text-xs font-semibold text-slate-500">Lesion Tissue Area:</span>
                  <span className="text-sm font-black text-slate-900">
                    {result.severity.lesion_percentage}%
                  </span>
                </div>
              )}

              <p className="text-[11px] text-slate-600 leading-relaxed pt-1">
                {result.severity.notes}
              </p>
              <span className="text-[10px] text-slate-400 block">
                Methodology: {result.severity.methodology}
              </span>
            </div>
          </div>

          {/* Alternative Predictions */}
          <div className="p-6 sm:p-8 space-y-4">
            <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
              <Activity className="w-4 h-4 text-agri-600" />
              <span>Alternative Probabilities</span>
            </h3>

            <div className="space-y-3">
              {result.alternative_predictions.map((alt) => {
                const altPct = Math.round(alt.confidence * 100);
                return (
                  <div key={alt.condition} className="space-y-1">
                    <div className="flex items-center justify-between text-xs">
                      <span className="font-semibold text-slate-700">{alt.display_name}</span>
                      <span className="font-bold text-slate-900">{altPct}%</span>
                    </div>
                    <div className="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                      <div
                        className="bg-agri-500 h-full rounded-full transition-all duration-300"
                        style={{ width: `${altPct}%` }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        {/* Symptoms & Pathogen Info */}
        <div className="p-6 sm:p-8 space-y-6">
          <div>
            <h3 className="text-base font-bold text-slate-900 mb-2 flex items-center gap-2">
              <BookOpen className="w-4 h-4 text-agri-600" />
              <span>Visible Symptoms & Etiology</span>
            </h3>
            <p className="text-sm text-slate-700 leading-relaxed">{result.symptoms}</p>
          </div>

          {result.causes && (
            <div>
              <span className="text-xs font-bold text-slate-500 uppercase tracking-wider block mb-1">
                Pathogen & Causes:
              </span>
              <p className="text-sm text-slate-700 leading-relaxed">{result.causes}</p>
            </div>
          )}

          {/* Prevention & Practical Management */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-4 border-t border-slate-100">
            <div>
              <span className="text-xs font-bold text-emerald-800 uppercase tracking-wider block mb-2">
                Preventive Measures
              </span>
              <ul className="space-y-2">
                {result.prevention.map((item, idx) => (
                  <li key={idx} className="text-xs text-slate-700 flex items-start gap-2">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 flex-shrink-0 mt-0.5" />
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div>
              <span className="text-xs font-bold text-agri-800 uppercase tracking-wider block mb-2">
                Field Management Advice
              </span>
              <ul className="space-y-2">
                {result.management.map((item, idx) => (
                  <li key={idx} className="text-xs text-slate-700 flex items-start gap-2">
                    <ShieldCheck className="w-3.5 h-3.5 text-agri-600 flex-shrink-0 mt-0.5" />
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* Expert Consultation Box */}
          <div className="p-4 rounded-2xl bg-amber-50/70 border border-amber-200 flex items-start gap-3">
            <HelpCircle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
            <div className="text-xs text-amber-900 space-y-1">
              <span className="font-bold block">When to Consult an Agricultural Extension Officer:</span>
              <p className="leading-relaxed">{result.consult_expert_when}</p>
            </div>
          </div>

          {/* Citations & Disclaimers */}
          <div className="pt-4 border-t border-slate-100 text-[11px] text-slate-400 space-y-1">
            <p><span className="font-semibold text-slate-500">Verified Evidence Base:</span> {result.references}</p>
            <p><span className="font-semibold text-slate-500">Model Architecture:</span> {result.model_metadata.model_name} (v{result.model_metadata.model_version}) on {result.model_metadata.device.toUpperCase()}</p>
            <p className="text-[10px] text-slate-400">
              Disclaimer: AgriGuard AI provides diagnostic assistance based on visual patterns. Field diagnoses must always be correlated with crop history, weather conditions, and regional agricultural extension advisories.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
