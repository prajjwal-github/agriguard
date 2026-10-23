import { useState } from 'react';
import { Navbar } from './components/Navbar';
import { TransparencyPage } from './components/TransparencyPage';
import { DatasetAuditPage } from './components/DatasetAuditPage';
import { RealtimePrototype } from './components/RealtimePrototype';

export function App() {
  const [activeTab, setActiveTab] = useState<'diagnose' | 'transparency' | 'datasets'>('diagnose');

  const resetWorkflow = () => {
    setActiveTab('diagnose');
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 text-slate-900 antialiased selection:bg-agri-200">
      <Navbar
        activeTab={activeTab}
        setActiveTab={(t) => setActiveTab(t as any)}
        resetWorkflow={resetWorkflow}
      />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
        {activeTab === 'transparency' && <TransparencyPage />}
        {activeTab === 'datasets' && <DatasetAuditPage />}
        {activeTab === 'diagnose' && <RealtimePrototype />}
      </main>

      <footer className="border-t border-slate-200 bg-white py-6 text-center text-xs text-slate-500 print:hidden">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
          <p>© 2026 AgriGuard AI. Scientifically Responsible Agricultural Pathology Intelligence.</p>
          <p className="text-[11px] text-slate-400">
            Powered by PyTorch 2.14, FastAPI & MobileNetV3/ResNet18 • CC BY 4.0 Verified Datasets
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
