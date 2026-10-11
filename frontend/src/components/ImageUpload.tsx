import React, { useRef, useState } from 'react';
import { UploadCloud, X, ArrowLeft, Loader2, AlertCircle, Camera, Check } from 'lucide-react';

interface ImageUploadProps {
  categoryName: string;
  cropName: string;
  onAnalyze: (file: File) => Promise<void>;
  onBack: () => void;
  isLoading: boolean;
  error: string | null;
}

export const ImageUpload: React.FC<ImageUploadProps> = ({
  categoryName,
  cropName,
  onAnalyze,
  onBack,
  isLoading,
  error,
}) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [dragOver, setDragOver] = useState(false);
  const [clientError, setClientError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const cameraInputRef = useRef<HTMLInputElement>(null);

  const handleFile = (file: File) => {
    setClientError(null);
    if (!file.type.match(/^image\/(jpeg|jpg|png|webp)$/i)) {
      setClientError('Please upload a valid image file (JPEG, PNG, or WebP).');
      return;
    }
    if (file.size > 10 * 1024 * 1024) {
      setClientError('Image size exceeds 10 MB limit. Please select a smaller photo.');
      return;
    }

    setSelectedFile(file);
    const url = URL.createObjectURL(file);
    setPreviewUrl(url);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const clearImage = () => {
    setSelectedFile(null);
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    setPreviewUrl(null);
    setClientError(null);
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <button
        onClick={onBack}
        disabled={isLoading}
        className="inline-flex items-center gap-1.5 text-xs font-bold text-slate-600 hover:text-agri-700 transition-colors disabled:opacity-50"
      >
        <ArrowLeft className="w-3.5 h-3.5" /> Back to Crop Selection
      </button>

      <div className="bg-white rounded-3xl border border-slate-200 shadow-sm p-6 sm:p-8">
        <div className="flex flex-wrap items-center justify-between gap-3 pb-6 border-b border-slate-100">
          <div>
            <span className="text-xs font-bold text-agri-700 uppercase tracking-wider bg-agri-100 px-2.5 py-0.5 rounded-full">
              Step 3 of 4
            </span>
            <h2 className="text-2xl font-extrabold text-slate-900 mt-1">Upload Foliage Photograph</h2>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-xs font-semibold px-3 py-1 rounded-full bg-slate-100 text-slate-700 border border-slate-200">
              {categoryName}
            </span>
            <span className="text-xs font-bold px-3 py-1 rounded-full bg-agri-100 text-agri-800 border border-agri-200">
              {cropName}
            </span>
          </div>
        </div>

        {(error || clientError) && (
          <div className="mt-4 p-4 rounded-xl bg-rose-50 border border-rose-200 flex items-start gap-3 text-rose-800 text-sm">
            <AlertCircle className="w-5 h-5 flex-shrink-0 text-rose-600 mt-0.5" />
            <div>
              <span className="font-bold">Upload Error:</span> {error || clientError}
            </div>
          </div>
        )}

        <div className="mt-6">
          {!previewUrl ? (
            <div
              onDragOver={(e) => {
                e.preventDefault();
                setDragOver(true);
              }}
              onDragLeave={() => setDragOver(false)}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
              className={`border-2 border-dashed rounded-2xl p-8 sm:p-12 text-center cursor-pointer transition-all ${
                dragOver
                  ? 'border-agri-500 bg-agri-50/50 scale-[0.99]'
                  : 'border-slate-300 hover:border-agri-400 hover:bg-slate-50/50'
              }`}
            >
              <input
                ref={fileInputRef}
                type="file"
                accept="image/jpeg,image/png,image/webp"
                className="hidden"
                onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0])}
              />
              <input
                ref={cameraInputRef}
                type="file"
                accept="image/*"
                capture="environment"
                className="hidden"
                onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0])}
              />

              <div className="w-16 h-16 rounded-2xl bg-agri-50 border border-agri-100 text-agri-600 flex items-center justify-center mx-auto mb-4">
                <UploadCloud className="w-8 h-8" />
              </div>

              <h3 className="text-lg font-bold text-slate-800 mb-1">
                Drag and drop your photograph here
              </h3>
              <p className="text-xs text-slate-500 max-w-sm mx-auto mb-5">
                Ensure good lighting, sharp focus on affected leaf margins, and minimal background clutter.
              </p>

              <div className="flex flex-wrap items-center justify-center gap-3">
                <button
                  type="button"
                  onClick={(e) => {
                    e.stopPropagation();
                    fileInputRef.current?.click();
                  }}
                  className="px-4 py-2 rounded-xl text-xs font-bold bg-slate-900 text-white hover:bg-slate-800 transition"
                >
                  Browse Files
                </button>

                <button
                  type="button"
                  onClick={(e) => {
                    e.stopPropagation();
                    cameraInputRef.current?.click();
                  }}
                  className="px-4 py-2 rounded-xl text-xs font-bold bg-agri-600 text-white hover:bg-agri-700 transition flex items-center gap-1.5"
                >
                  <Camera className="w-4 h-4" /> Take Photo
                </button>
              </div>

              <span className="block mt-4 text-[11px] text-slate-400">
                Supports JPG, PNG, WebP up to 10 MB
              </span>
            </div>
          ) : (
            <div className="space-y-4">
              <div className="relative rounded-2xl overflow-hidden border border-slate-200 bg-slate-900 aspect-video max-h-96 flex items-center justify-center">
                <img
                  src={previewUrl}
                  alt="Crop Preview"
                  className="w-full h-full object-contain"
                />
                <button
                  onClick={clearImage}
                  disabled={isLoading}
                  className="absolute top-3 right-3 p-2 rounded-full bg-slate-900/70 text-white hover:bg-slate-900 transition backdrop-blur-sm"
                  title="Remove image"
                >
                  <X className="w-4 h-4" />
                </button>

                <div className="absolute bottom-3 left-3 bg-slate-900/80 backdrop-blur-md px-3 py-1.5 rounded-lg text-xs text-white flex items-center gap-2">
                  <Check className="w-3.5 h-3.5 text-emerald-400" />
                  <span>
                    {selectedFile?.name} ({(selectedFile!.size / (1024 * 1024)).toFixed(2)} MB)
                  </span>
                </div>
              </div>

              <div className="flex items-center justify-end gap-3 pt-2">
                <button
                  onClick={clearImage}
                  disabled={isLoading}
                  className="px-4 py-2.5 rounded-xl text-xs font-bold text-slate-600 hover:bg-slate-100 transition"
                >
                  Choose Different Image
                </button>

                <button
                  onClick={() => selectedFile && onAnalyze(selectedFile)}
                  disabled={isLoading || !selectedFile}
                  className="px-6 py-2.5 rounded-xl text-xs sm:text-sm font-bold bg-agri-600 text-white hover:bg-agri-700 disabled:opacity-50 transition shadow-sm flex items-center gap-2"
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      <span>Executing Neural Inference...</span>
                    </>
                  ) : (
                    <span>Analyze Disease & Symptoms</span>
                  )}
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
