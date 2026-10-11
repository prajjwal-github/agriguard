import React from 'react';

export const DatasetAuditPage: React.FC = () => {
  return (
    <div className="max-w-5xl mx-auto space-y-8">
      <div>
        <span className="text-xs font-bold text-agri-700 uppercase tracking-wider bg-agri-100 px-3 py-1 rounded-full">
          Quality Readiness Gates
        </span>
        <h1 className="text-3xl font-extrabold text-slate-900 mt-2">
          Dataset Engineering & Audit Logs
        </h1>
        <p className="text-sm sm:text-base text-slate-600 mt-1 max-w-3xl">
          Complete audit trail of acquired agricultural images, validation results, deduplication metrics, and leakage-resistant dataset partitions.
        </p>
      </div>

      {/* Rice Leaf Audit Card */}
      <div className="bg-white rounded-3xl border border-slate-200 shadow-sm p-6 sm:p-8 space-y-6">
        <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-slate-100">
          <div>
            <span className="text-xs font-bold px-2.5 py-0.5 rounded-full bg-emerald-100 text-emerald-800 border border-emerald-200">
              Quality Gate Passed
            </span>
            <h3 className="text-xl font-bold text-slate-900 mt-1">
              Rice / Paddy Leaf Dataset Audit (`rice_leaf`)
            </h3>
            <p className="text-xs text-slate-500">
              Category: Grain Crop / Leaf • Prajapati Benchmark
            </p>
          </div>

          <div className="text-right">
            <span className="text-xs font-bold text-emerald-700 block">ZERO Leakage Verified</span>
            <span className="text-[11px] text-slate-500">MD5 & Perceptual dHash Clustered</span>
          </div>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200">
            <span className="text-xs text-slate-500 block">Total Acquired</span>
            <span className="text-2xl font-black text-slate-900">105</span>
          </div>
          <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200">
            <span className="text-xs text-slate-500 block">Quarantined / Corrupt</span>
            <span className="text-2xl font-black text-rose-600">14</span>
            <span className="text-[10px] text-slate-400">Aspect ratio &gt; 3.5</span>
          </div>
          <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200">
            <span className="text-xs text-slate-500 block">Usable Verified</span>
            <span className="text-2xl font-black text-emerald-600">91</span>
          </div>
          <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200">
            <span className="text-xs text-slate-500 block">Imbalance Ratio</span>
            <span className="text-2xl font-black text-slate-900">1.25:1</span>
          </div>
        </div>

        <div>
          <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-3">
            Split Distribution (Train 70% / Val 15% / Test 15%)
          </h4>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border border-slate-100 rounded-xl overflow-hidden">
              <thead className="bg-slate-50 text-slate-600">
                <tr>
                  <th className="py-2.5 px-3">Split</th>
                  <th className="py-2.5 px-3">Sample Count</th>
                  <th className="py-2.5 px-3">Percentage</th>
                  <th className="py-2.5 px-3">Cluster Separation</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                <tr className="hover:bg-slate-50/50">
                  <td className="py-2 px-3 font-semibold text-slate-800">Train</td>
                  <td className="py-2 px-3">62</td>
                  <td className="py-2 px-3">68.1%</td>
                  <td className="py-2 px-3 text-emerald-600 font-semibold">Isolated</td>
                </tr>
                <tr className="hover:bg-slate-50/50">
                  <td className="py-2 px-3 font-semibold text-slate-800">Validation</td>
                  <td className="py-2 px-3">13</td>
                  <td className="py-2 px-3">14.3%</td>
                  <td className="py-2 px-3 text-emerald-600 font-semibold">Isolated</td>
                </tr>
                <tr className="hover:bg-slate-50/50">
                  <td className="py-2 px-3 font-semibold text-slate-800">Test (Held-Out)</td>
                  <td className="py-2 px-3">16</td>
                  <td className="py-2 px-3">17.6%</td>
                  <td className="py-2 px-3 text-emerald-600 font-semibold">Isolated</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Six Categories Matrix */}
      <div className="bg-white rounded-3xl border border-slate-200 shadow-sm p-6 sm:p-8 space-y-4">
        <h3 className="text-lg font-bold text-slate-900">
          Six Agricultural Categories Coverage Status
        </h3>
        <p className="text-xs text-slate-600">
          AgriGuard AI enforces logical separation between fruit organs, leaves, and grains. Below is the multi-category status:
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 pt-2">
          <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 space-y-1">
            <span className="text-xs font-bold text-slate-900 block">1. Fruit Surface</span>
            <span className="text-[11px] text-amber-700 bg-amber-50 px-2 py-0.5 rounded font-semibold inline-block">
              In Development
            </span>
            <p className="text-[11px] text-slate-500">Apple, Banana, Mango, Orange fruit surfaces.</p>
          </div>

          <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 space-y-1">
            <span className="text-xs font-bold text-slate-900 block">2. Fruit Leaf</span>
            <span className="text-[11px] text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded font-semibold inline-block">
              Benchmark Verified
            </span>
            <p className="text-[11px] text-slate-500">Apple leaf, Grape leaf, Citrus leaf.</p>
          </div>

          <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 space-y-1">
            <span className="text-xs font-bold text-slate-900 block">3. Vegetable Surface</span>
            <span className="text-[11px] text-amber-700 bg-amber-50 px-2 py-0.5 rounded font-semibold inline-block">
              In Development
            </span>
            <p className="text-[11px] text-slate-500">Tomato, Potato tuber, Bell Pepper fruit.</p>
          </div>

          <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 space-y-1">
            <span className="text-xs font-bold text-slate-900 block">4. Vegetable Leaf</span>
            <span className="text-[11px] text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded font-semibold inline-block">
              Benchmark Verified
            </span>
            <p className="text-[11px] text-slate-500">Tomato leaf, Potato leaf, Pepper leaf.</p>
          </div>

          <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 space-y-1">
            <span className="text-xs font-bold text-slate-900 block">5. Grain Kernel</span>
            <span className="text-[11px] text-amber-700 bg-amber-50 px-2 py-0.5 rounded font-semibold inline-block">
              In Development
            </span>
            <p className="text-[11px] text-slate-500">Rice grains, Wheat kernels, Maize seeds.</p>
          </div>

          <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 space-y-1">
            <span className="text-xs font-bold text-slate-900 block">6. Grain Crop / Leaf</span>
            <span className="text-[11px] text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded font-semibold inline-block">
              Operational Checkpoint
            </span>
            <p className="text-[11px] text-slate-500">Rice leaf, Maize leaf, Wheat tillers.</p>
          </div>
        </div>
      </div>
    </div>
  );
};
