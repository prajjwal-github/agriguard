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
