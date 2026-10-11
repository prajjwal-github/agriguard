import React, { useState } from 'react';
import { Search, ArrowLeft, CheckCircle2, Clock, AlertCircle, Sparkles } from 'lucide-react';
import type { CropInfo } from '../services/api';

interface CropSelectionProps {
  categoryName: string;
  crops: CropInfo[];
  selectedCrop: string | null;
  onSelectCrop: (cropId: string) => void;
  onBack: () => void;
}

export const CropSelection: React.FC<CropSelectionProps> = ({
  categoryName,
  crops,
  selectedCrop,
  onSelectCrop,
  onBack,
}) => {
  const [search, setSearch] = useState('');

  const filteredCrops = crops.filter((c) =>
    c.display_name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <button
            onClick={onBack}
            className="inline-flex items-center gap-1.5 text-xs font-bold text-slate-600 hover:text-agri-700 mb-2 transition-colors"
          >
            <ArrowLeft className="w-3.5 h-3.5" /> Back to Categories
          </button>
          <div className="flex items-center gap-2">
            <span className="text-xs font-bold text-agri-700 uppercase tracking-wider bg-agri-100 px-2.5 py-0.5 rounded-full">
              Step 2 of 4
            </span>
            <span className="text-xs text-slate-500 font-medium">Category: {categoryName}</span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 mt-1">
            Choose Target Crop
          </h2>
        </div>

        <div className="relative w-full sm:w-64">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Search crops..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-9 pr-3 py-2 text-sm rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-agri-500 bg-white"
          />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredCrops.map((crop) => {
          const isSelected = selectedCrop === crop.crop_id;
          const isReady = crop.is_available;

          return (
            <div
              key={crop.crop_id}
              onClick={() => isReady && onSelectCrop(crop.crop_id)}
              className={`p-5 rounded-2xl border-2 transition-all relative flex flex-col justify-between ${
                !isReady
                  ? 'border-slate-200 bg-slate-50/70 opacity-80 cursor-not-allowed'
                  : isSelected
                  ? 'border-agri-600 bg-agri-50/50 shadow-md ring-2 ring-agri-500/20 cursor-pointer'
                  : 'border-slate-200 bg-white hover:border-agri-400 hover:shadow-sm cursor-pointer'
              }`}
            >
              <div>
                <div className="flex items-start justify-between gap-2 mb-3">
                  <h3 className="text-base font-bold text-slate-900">{crop.display_name}</h3>
                  {isReady ? (
                    <span className="inline-flex items-center gap-1 text-[11px] font-bold px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 border border-emerald-200">
                      <CheckCircle2 className="w-3 h-3 text-emerald-600" /> Operational
                    </span>
                  ) : (
                    <span className="inline-flex items-center gap-1 text-[11px] font-semibold px-2 py-0.5 rounded-full bg-amber-50 text-amber-700 border border-amber-200">
                      <Clock className="w-3 h-3 text-amber-500" /> In Development
                    </span>
                  )}
                </div>

                <div className="text-xs text-slate-600 mb-3">
                  <span className="font-semibold text-slate-700">Supported conditions:</span>{' '}
                  {crop.classes.length > 0 ? (
                    <div className="flex flex-wrap gap-1 mt-1.5">
                      {crop.classes.map((cls) => (
                        <span
                          key={cls}
                          className="px-2 py-0.5 rounded bg-slate-100 text-slate-700 text-[11px] font-medium"
                        >
                          {cls.replace(/_/g, ' ')}
                        </span>
                      ))}
                    </div>
                  ) : (
                    <span className="text-slate-400 italic block mt-1">Pending verified research dataset</span>
                  )}
                </div>
              </div>

              <div className="mt-4 pt-3 border-t border-slate-100">
                {isReady ? (
                  <span className="text-xs font-bold text-agri-700 flex items-center justify-between">
                    <span>Select for diagnosis</span>
                    <Sparkles className="w-3.5 h-3.5 text-agri-600" />
                  </span>
                ) : (
                  <span className="text-[11px] text-slate-500 flex items-center gap-1">
                    <AlertCircle className="w-3 h-3 text-amber-500 flex-shrink-0" />
                    Dataset curation underway (no mock predictions)
                  </span>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
