import React, { useEffect, useState } from 'react';
import { Sprout, ShieldCheck, Activity, Database } from 'lucide-react';

interface NavbarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  resetWorkflow: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({ activeTab, setActiveTab, resetWorkflow }) => {
  const [backendOnline, setBackendOnline] = useState<boolean | null>(null);

  useEffect(() => {
    fetch('http://localhost:8080/api/v1/health')
      .then((res) => setBackendOnline(res.ok))
      .catch(() => setBackendOnline(false));
  }, []);

  return (
    <header className="sticky top-0 z-50 bg-white/95 backdrop-blur-md border-b border-slate-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div
            className="flex items-center gap-3 cursor-pointer select-none"
            onClick={resetWorkflow}
          >
            <div className="w-10 h-10 rounded-xl bg-agri-600 flex items-center justify-center text-white shadow-sm">
              <Sprout className="w-6 h-6" />
            </div>
            <div>
              <span className="text-xl font-bold tracking-tight text-slate-900 flex items-center gap-1.5">
                AgriGuard <span className="text-agri-600 font-extrabold text-sm uppercase px-1.5 py-0.5 bg-agri-100 rounded">AI</span>
              </span>
              <p className="text-[11px] text-slate-500 font-medium">Multi-Crop Health Intelligence</p>
            </div>
          </div>

          <nav className="flex items-center gap-1 sm:gap-2">
            <button
              onClick={() => setActiveTab('diagnose')}
              className={`px-3 py-2 rounded-lg text-sm font-semibold transition-all flex items-center gap-1.5 ${
                activeTab === 'diagnose'
                  ? 'bg-agri-50 text-agri-700 font-bold'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
              }`}
            >
              <ShieldCheck className="w-4 h-4" />
              <span>Live Dashboard</span>
            </button>

            <button
              onClick={() => setActiveTab('transparency')}
              className={`px-3 py-2 rounded-lg text-sm font-semibold transition-all flex items-center gap-1.5 ${
                activeTab === 'transparency'
                  ? 'bg-agri-50 text-agri-700 font-bold'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
              }`}
            >
              <Activity className="w-4 h-4" />
              <span>Model Benchmarks</span>
            </button>

            <button
              onClick={() => setActiveTab('datasets')}
              className={`px-3 py-2 rounded-lg text-sm font-semibold transition-all flex items-center gap-1.5 ${
                activeTab === 'datasets'
                  ? 'bg-agri-50 text-agri-700 font-bold'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
              }`}
            >
              <Database className="w-4 h-4" />
              <span>Dataset Audits</span>
            </button>
          </nav>

          <div className="hidden sm:flex items-center gap-2">
            <div
              className={`flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold ${
                backendOnline === true
                  ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                  : backendOnline === false
                  ? 'bg-rose-50 text-rose-700 border border-rose-200'
                  : 'bg-slate-100 text-slate-600'
              }`}
            >
              <span
                className={`w-2 h-2 rounded-full ${
                  backendOnline === true ? 'bg-emerald-500 animate-pulse' : 'bg-rose-500'
                }`}
              />
              {backendOnline === true ? 'API Connected' : backendOnline === false ? 'API Offline' : 'Connecting...'}
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};
