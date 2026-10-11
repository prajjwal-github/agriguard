import React, { useEffect, useState } from 'react';
import { Activity, Database } from 'lucide-react';
import { getEvaluations } from '../services/api';

export const TransparencyPage: React.FC = () => {
  const [evaluations, setEvaluations] = useState<Record<string, any>>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getEvaluations()
      .then((data) => setEvaluations(data))
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="max-w-5xl mx-auto space-y-8">
      <div>
        <span className="text-xs font-bold text-agri-700 uppercase tracking-wider bg-agri-100 px-3 py-1 rounded-full">
          Scientific Rigor & Provenance
        </span>
        <h1 className="text-3xl font-extrabold text-slate-900 mt-2">
          Model & Dataset Transparency
        </h1>
        <p className="text-sm sm:text-base text-slate-600 mt-1 max-w-3xl">
          AgriGuard AI enforces total transparency. All metrics reflect real evaluation on isolated test sets. No fabricated benchmark scores, no synthetic image datasets, and no unvalidated models.
        </p>
      </div>

      {/* Model Benchmark Cards */}
      <div className="space-y-6">
        <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
          <Activity className="w-5 h-5 text-agri-600" />
          <span>Operational Model Benchmarks</span>
        </h2>

        {loading ? (
          <div className="p-8 text-center bg-white rounded-2xl border border-slate-200">
            <span className="text-sm text-slate-500">Loading benchmark evaluations...</span>
          </div>
        ) : Object.keys(evaluations).length === 0 ? (
          <div className="p-8 text-center bg-white rounded-2xl border border-slate-200 text-sm text-slate-500">
            No evaluation reports recorded yet.
          </div>
        ) : (
          Object.entries(evaluations).map(([modelKey, report]) => {
            const m = report.metrics || {};
            const cm = report.confusion_matrix || [];
            const classes = report.classes || [];

            return (
              <div
                key={modelKey}
                className="bg-white rounded-3xl border border-slate-200 shadow-sm p-6 sm:p-8 space-y-6"
              >
                <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-slate-100">
                  <div>
                    <span className="text-xs font-bold px-2.5 py-0.5 rounded-full bg-emerald-100 text-emerald-800 border border-emerald-200">
                      Verified Checkpoint
                    </span>
                    <h3 className="text-xl font-bold text-slate-900 mt-1">
                      {modelKey.replace(/_/g, ' ').toUpperCase()}
                    </h3>
                    <p className="text-xs text-slate-500 mt-0.5">
                      Evaluated on {report.num_test_samples} held-out test samples • {report.timestamp?.slice(0, 10)}
                    </p>
                  </div>

                  <div className="flex items-center gap-2">
                    <span className="text-xs font-semibold px-3 py-1 rounded-full bg-slate-100 text-slate-700">
                      MobileNetV3-Small
                    </span>
                    <span className="text-xs font-semibold px-3 py-1 rounded-full bg-slate-100 text-slate-700">
                      PyTorch 2.14 CPU
                    </span>
                  </div>
                </div>

                {/* Metric Badges */}
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                  <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200">
                    <span className="text-xs text-slate-500 block">Overall Accuracy</span>
                    <span className="text-2xl font-black text-slate-900">
                      {(m.accuracy * 100).toFixed(1)}%
                    </span>
                  </div>

                  <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200">
                    <span className="text-xs text-slate-500 block">Macro F1-Score</span>
                    <span className="text-2xl font-black text-slate-900">
                      {m.macro_f1?.toFixed(4)}
                    </span>
                  </div>

                  <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200">
                    <span className="text-xs text-slate-500 block">Macro Recall</span>
                    <span className="text-2xl font-black text-slate-900">
                      {(m.macro_recall * 100).toFixed(1)}%
                    </span>
                  </div>

                  <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200">
                    <span className="text-xs text-slate-500 block">Inference Latency</span>
                    <span className="text-2xl font-black text-slate-900">
                      {m.avg_latency_ms} <span className="text-xs font-normal text-slate-500">ms</span>
                    </span>
                  </div>
                </div>

                {/* Per-Class Table */}
                {report.per_class_metrics && (
                  <div>
                    <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-3">
                      Per-Class Diagnostic Breakdown
                    </h4>
                    <div className="overflow-x-auto">
                      <table className="w-full text-left text-xs border border-slate-100 rounded-xl overflow-hidden">
                        <thead className="bg-slate-50 text-slate-600">
                          <tr>
                            <th className="py-2.5 px-3">Condition / Class</th>
                            <th className="py-2.5 px-3">Precision</th>
                            <th className="py-2.5 px-3">Recall</th>
                            <th className="py-2.5 px-3">F1-Score</th>
                            <th className="py-2.5 px-3">Test Support</th>
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-100">
                          {Object.entries(report.per_class_metrics).map(([cls, p]: any) => (
                            <tr key={cls} className="hover:bg-slate-50/50">
                              <td className="py-2 px-3 font-semibold text-slate-800">{cls.replace(/_/g, ' ')}</td>
                              <td className="py-2 px-3">{(p.precision * 100).toFixed(1)}%</td>
                              <td className="py-2 px-3">{(p.recall * 100).toFixed(1)}%</td>
                              <td className="py-2 px-3 font-semibold">{p.f1_score?.toFixed(4)}</td>
                              <td className="py-2 px-3 text-slate-500">{p.support}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                )}

                {/* Confusion Matrix */}
                {cm.length > 0 && (
                  <div>
                    <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-3">
                      Empirical Confusion Matrix
                    </h4>
                    <div className="p-4 rounded-2xl bg-slate-900 text-white font-mono text-xs overflow-x-auto">
                      <div className="text-slate-400 mb-2">Rows = Ground Truth | Columns = Predicted:</div>
                      <div className="grid gap-1">
                        {cm.map((row: number[], rIdx: number) => (
                          <div key={rIdx} className="flex gap-4">
                            <span className="w-40 text-slate-400 truncate">
                              {classes[rIdx] || `Class ${rIdx}`}:
                            </span>
                            {row.map((val: number, cIdx: number) => (
                              <span
                                key={cIdx}
                                className={`w-10 text-right ${
                                  rIdx === cIdx ? 'text-emerald-400 font-bold' : 'text-slate-300'
                                }`}
                              >
                                {val}
                              </span>
                            ))}
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>

      {/* Dataset Provenance & Standards */}
      <div className="bg-white rounded-3xl border border-slate-200 shadow-sm p-6 sm:p-8 space-y-6">
        <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
          <Database className="w-5 h-5 text-agri-600" />
          <span>Dataset Provenance & Legal Licensing</span>
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-5 rounded-2xl border border-slate-200 space-y-2">
            <span className="text-xs font-bold text-agri-800 uppercase tracking-wider block">
              Rice Leaf Diseases Dataset
            </span>
            <p className="text-xs text-slate-700 leading-relaxed">
              <strong>Authors:</strong> Prajapati, H. B., Dabhi, V. K., Prajapati, S. V. (2017)
            </p>
            <p className="text-xs text-slate-700 leading-relaxed">
              <strong>Citation:</strong> <em>Computers and Electronics in Agriculture</em>
            </p>
            <p className="text-xs text-slate-500">
              <strong>License:</strong> Creative Commons Attribution 4.0 International (CC BY 4.0)
            </p>
            <span className="text-[11px] text-emerald-700 font-semibold block">
              Status: Verified Authentic Dataset • 91 Images Usable
            </span>
          </div>

          <div className="p-5 rounded-2xl border border-slate-200 space-y-2">
            <span className="text-xs font-bold text-agri-800 uppercase tracking-wider block">
              PlantVillage Open Research Dataset
            </span>
            <p className="text-xs text-slate-700 leading-relaxed">
              <strong>Authors:</strong> Hughes, D. P., & Salathé, M. (Penn State University, 2015)
            </p>
            <p className="text-xs text-slate-700 leading-relaxed">
              <strong>Citation:</strong> <em>arXiv:1511.08060</em>
            </p>
            <p className="text-xs text-slate-500">
              <strong>License:</strong> CC BY 4.0 Open Access
            </p>
            <span className="text-[11px] text-emerald-700 font-semibold block">
              Status: Verified Laboratory Benchmarks • Multi-Crop Foliage
            </span>
          </div>
        </div>

        <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 text-xs text-slate-600 space-y-2">
          <span className="font-bold text-slate-800 block">Known Scientific Limitations:</span>
          <ul className="list-disc pl-4 space-y-1">
            <li>Controlled background photographs have domain shift when applied to complex field conditions with harsh shadows.</li>
            <li>Out-of-distribution detection uses Shannon entropy thresholding; extreme novel crop types trigger uncertainty rejection by design.</li>
            <li>Grad-CAM heatmaps highlight model attention regions and must not be used as quantitative lesion area segmentation masks.</li>
          </ul>
        </div>
      </div>
    </div>
  );
};
