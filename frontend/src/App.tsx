import { useEffect, useState } from 'react';
import { Navbar } from './components/Navbar';
import { CategorySelection } from './components/CategorySelection';
import { CropSelection } from './components/CropSelection';
import { ImageUpload } from './components/ImageUpload';
import { DiagnosisResult } from './components/DiagnosisResult';
import { TransparencyPage } from './components/TransparencyPage';
import { DatasetAuditPage } from './components/DatasetAuditPage';
import {
  getCategories,
  getCropsByCategory,
  predictDisease,
} from './services/api';
import type {
  CategoryInfo,
  CropInfo,
  PredictionResult,
} from './services/api';
import { Sparkles, CheckCircle2 } from 'lucide-react';

export function App() {
  const [activeTab, setActiveTab] = useState<'diagnose' | 'transparency' | 'datasets'>('diagnose');
  const [step, setStep] = useState<'categories' | 'crops' | 'upload' | 'result'>('categories');

  const [categories, setCategories] = useState<Record<string, CategoryInfo>>({});
  const [crops, setCrops] = useState<CropInfo[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [selectedCrop, setSelectedCrop] = useState<string | null>(null);

  const [uploadedImageUrl, setUploadedImageUrl] = useState<string | null>(null);
  const [predictionResult, setPredictionResult] = useState<PredictionResult | null>(null);

  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getCategories()
      .then((data) => setCategories(data))
      .catch((err) => {
        console.error('Failed to load categories:', err);
        setError('Could not connect to AgriGuard backend service. Please check API server.');
      });
  }, []);

  const handleSelectCategory = async (catId: string) => {
    setSelectedCategory(catId);
    setError(null);
    setLoading(true);
    try {
      const cropList = await getCropsByCategory(catId);
      setCrops(cropList);
      setStep('crops');
    } catch (err: any) {
      setError(err.message || 'Failed to fetch crops');
    } finally {
      setLoading(false);
    }
  };

  const handleSelectCrop = (cropId: string) => {
    setSelectedCrop(cropId);
    setError(null);
    setStep('upload');
  };

  const handleAnalyze = async (file: File) => {
    if (!selectedCategory || !selectedCrop) return;
    setLoading(true);
    setError(null);

    const previewUrl = URL.createObjectURL(file);
    setUploadedImageUrl(previewUrl);

    try {
      const res = await predictDisease(selectedCategory, selectedCrop, file);
      setPredictionResult(res);
      setStep('result');
    } catch (err: any) {
      setError(err.message || 'Diagnostic inference failed');
    } finally {
      setLoading(false);
    }
  };

  const resetWorkflow = () => {
    setSelectedCategory(null);
    setSelectedCrop(null);
    setUploadedImageUrl(null);
    setPredictionResult(null);
    setError(null);
    setStep('categories');
    setActiveTab('diagnose');
  };

  const selectedCategoryObj = selectedCategory ? categories[selectedCategory] : null;
  const selectedCropObj = crops.find((c) => c.crop_id === selectedCrop);

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 text-slate-900 antialiased selection:bg-agri-200">
      <Navbar
        activeTab={activeTab}
        setActiveTab={(t) => {
          setActiveTab(t as any);
          setError(null);
        }}
        resetWorkflow={resetWorkflow}
      />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
        {activeTab === 'transparency' && <TransparencyPage />}
        {activeTab === 'datasets' && <DatasetAuditPage />}

        {activeTab === 'diagnose' && (
          <div className="space-y-8">
            {step === 'categories' && (
              <>
                {/* Hero Header */}
                <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-agri-900 via-agri-800 to-slate-900 text-white p-8 sm:p-12 shadow-xl mb-10">
                  <div className="relative z-10 max-w-2xl space-y-4">
                    <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-agri-500/20 border border-agri-400/30 text-agri-300 text-xs font-bold tracking-wide">
                      <Sparkles className="w-3.5 h-3.5" />
                      <span>Production AI for Agronomists & Farmers</span>
                    </div>

                    <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight text-white leading-tight">
                      Intelligent Multi-Crop Disease Diagnosis
                    </h1>

                    <p className="text-sm sm:text-base text-slate-300 leading-relaxed">
                      Upload leaf or plant photographs for certified organ-specific disease classification, empirical severity estimation, Grad-CAM neural attention overlays, and verified extension management advice.
                    </p>

                    <div className="pt-2 flex flex-wrap items-center gap-4 text-xs font-semibold text-slate-300">
                      <div className="flex items-center gap-1.5">
                        <CheckCircle2 className="w-4 h-4 text-agri-400" />
                        <span>Zero Synthetic Imagery</span>
                      </div>
                      <div className="flex items-center gap-1.5">
                        <CheckCircle2 className="w-4 h-4 text-agri-400" />
                        <span>OOD Uncertainty Rejection</span>
                      </div>
                      <div className="flex items-center gap-1.5">
                        <CheckCircle2 className="w-4 h-4 text-agri-400" />
                        <span>Authentic Research Datasets</span>
                      </div>
                    </div>
                  </div>

                  <div className="absolute -right-12 -bottom-12 w-96 h-96 rounded-full bg-agri-500/10 blur-3xl pointer-events-none" />
                </div>

                <CategorySelection
                  categories={categories}
                  selectedCategory={selectedCategory}
                  onSelectCategory={handleSelectCategory}
                />
              </>
            )}

            {step === 'crops' && (
              <CropSelection
                categoryName={selectedCategoryObj?.display_name || 'Selected Category'}
                crops={crops}
                selectedCrop={selectedCrop}
                onSelectCrop={handleSelectCrop}
                onBack={() => setStep('categories')}
              />
            )}

            {step === 'upload' && (
              <ImageUpload
                categoryName={selectedCategoryObj?.display_name || ''}
                cropName={selectedCropObj?.display_name || ''}
                onAnalyze={handleAnalyze}
                onBack={() => setStep('crops')}
                isLoading={loading}
                error={error}
              />
            )}

            {step === 'result' && predictionResult && (
              <DiagnosisResult
                result={predictionResult}
                uploadedImageUrl={uploadedImageUrl}
                onReset={resetWorkflow}
              />
            )}
          </div>
        )}
      </main>

      <footer className="border-t border-slate-200 bg-white py-6 text-center text-xs text-slate-500 print:hidden">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
          <p>© 2026 AgriGuard AI. Scientifically Responsible Agricultural Pathology Intelligence.</p>
          <p className="text-[11px] text-slate-400">
            Powered by PyTorch 2.14, FastAPI & MobileNetV3 • CC BY 4.0 Verified Datasets
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
