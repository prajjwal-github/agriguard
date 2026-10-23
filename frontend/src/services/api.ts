/**
 * AgriGuard AI Backend API Client
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080';

export interface CategoryInfo {
  category_id: string;
  display_name: string;
  description: string;
  supported_crops_count: number;
}

export interface CropInfo {
  crop_id: string;
  display_name: string;
  status: 'ready' | 'experimental' | 'planned';
  is_available: boolean;
  task: string;
  classes: string[];
}

export interface AlternativePrediction {
  condition: string;
  display_name: string;
  confidence: number;
}

export interface SeverityInfo {
  supported: boolean;
  level: string | null;
  lesion_percentage: number | null;
  methodology: string;
  notes: string;
}

export interface ModelMetadata {
  model_name: string;
  architecture: string;
  model_version: string;
  device: string;
}

export interface PredictionResult {
  prediction_id: string;
  category: string;
  crop: string;
  plant_part: string;
  predicted_condition: string;
  display_name: string;
  is_reliable: boolean;
  confidence: number;
  entropy: number;
  alternative_predictions: AlternativePrediction[];
  severity: SeverityInfo;
  symptoms: string;
  causes: string;
  favorable_conditions: string;
  prevention: string[];
  management: string[];
  consult_expert_when: string;
  references: string;
  model_metadata: ModelMetadata;
  gradcam_heatmap: string | null;
  warnings: string[];
  processing_time_ms: number;
}

export async function getCategories(): Promise<Record<string, CategoryInfo>> {
  const res = await fetch(`${API_BASE_URL}/api/v1/categories`);
  if (!res.ok) throw new Error(`Failed to load categories: ${res.statusText}`);
  return res.json();
}

export async function getCropsByCategory(categoryId: string): Promise<CropInfo[]> {
  const res = await fetch(`${API_BASE_URL}/api/v1/crops/${categoryId}`);
  if (!res.ok) throw new Error(`Failed to load crops for ${categoryId}: ${res.statusText}`);
  return res.json();
}

export async function getCapabilities(): Promise<any> {
  const res = await fetch(`${API_BASE_URL}/api/v1/capabilities`);
  if (!res.ok) throw new Error(`Failed to load capabilities: ${res.statusText}`);
  return res.json();
}

export async function getEvaluations(): Promise<Record<string, any>> {
  const res = await fetch(`${API_BASE_URL}/api/v1/evaluations`);
  if (!res.ok) throw new Error(`Failed to load evaluations: ${res.statusText}`);
  return res.json();
}

export async function predictDisease(
  category: string,
  crop: string,
  file: File
): Promise<PredictionResult> {
  const formData = new FormData();
  formData.append('category', category);
  formData.append('crop', crop);
  formData.append('file', file);

  const res = await fetch(`${API_BASE_URL}/api/v1/predict`, {
    method: 'POST',
    body: formData,
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(errorData.detail || 'Inference prediction failed');
  }

  return res.json();
}

export function getSampleImageUrl(crop: string): string {
  return `${API_BASE_URL}/api/v1/sample/${crop}`;
}

export async function fetchSampleImageFile(crop: string): Promise<File> {
  const url = getSampleImageUrl(crop);
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Could not load test sample for ${crop}`);
  const blob = await res.blob();
  return new File([blob], `${crop}_test_sample.jpg`, { type: 'image/jpeg' });
}

export interface SystemTelemetry {
  status: string;
  device: string;
  torch_version: string;
  total_models: number;
  average_accuracy: number;
  accuracy_range: string;
  data_leakage_pct: number;
  timestamp: string;
}

export interface RecentInference {
  timestamp: string;
  prediction_id: string;
  crop: string;
  crop_name: string;
  plant_part: string;
  predicted_condition: string;
  display_name: string;
  confidence: number;
  latency_ms: number;
  entropy: number;
  is_reliable: boolean;
}

export interface DashboardStats {
  status: string;
  system: SystemTelemetry;
  splits: {
    total_images: number;
    train_count: number;
    train_pct: number;
    val_count: number;
    val_pct: number;
    test_count: number;
    test_pct: number;
    leakage_overlap: number;
  };
  category_counts: Record<string, number>;
  models: Array<{
    crop: string;
    display_name: string;
    category: string;
    architecture: string;
    test_samples: number;
    classes: string[];
    accuracy: number;
    macro_f1: number;
    macro_precision: number;
    macro_recall: number;
    latency_ms: number;
  }>;
  histories: Record<string, any>;
  recent_inferences: RecentInference[];
}

export async function getDashboardStats(): Promise<DashboardStats> {
  const res = await fetch(`${API_BASE_URL}/api/v1/dashboard/stats`);
  if (!res.ok) throw new Error(`Failed to load dashboard stats: ${res.statusText}`);
  return res.json();
}

export interface DatasetCropAudit {
  timestamp: string;
  crop: string;
  category: string;
  total_images: number;
  usable_images: number;
  corrupt_images: number;
  duplicate_images: number;
  num_classes: number;
  class_distribution: Record<string, number>;
  split_distribution: {
    train: number;
    val: number;
    test: number;
  };
  imbalance_ratio: number;
  resolution_stats: {
    min_width: number;
    max_width: number;
    avg_width: number;
    min_height: number;
    max_height: number;
    avg_height: number;
  };
  quality_gate: {
    passed: boolean;
    warnings: string[];
    failures: string[];
  };
}

export interface DatasetAuditResponse {
  status: string;
  splits: {
    total_images: number;
    train_count: number;
    train_pct: number;
    val_count: number;
    val_pct: number;
    test_count: number;
    test_pct: number;
    leakage_overlap: number;
  };
  crops: Record<string, DatasetCropAudit>;
  coverage: any;
}

export async function getDatasetAudit(): Promise<DatasetAuditResponse> {
  const res = await fetch(`${API_BASE_URL}/api/v1/dataset/audit`);
  if (!res.ok) throw new Error(`Failed to load dataset audit: ${res.statusText}`);
  return res.json();
}

export async function getRecentInferences(): Promise<RecentInference[]> {
  const res = await fetch(`${API_BASE_URL}/api/v1/inferences/recent`);
  if (!res.ok) throw new Error(`Failed to load recent inferences: ${res.statusText}`);
  return res.json();
}

