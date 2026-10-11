# AgriGuard AI — REST API Reference

The FastAPI backend runs on `http://localhost:8000`. Interactive OpenAPI documentation is available at `http://localhost:8000/docs`.

### 1. Health Check
`GET /api/v1/health`
Returns system status, device, and service version.

### 2. Primary Categories
`GET /api/v1/categories`
Returns the 6 registered agricultural categories (`fruit`, `fruit_leaf`, `vegetable`, `vegetable_leaf`, `grain`, `grain_crop_leaf`).

### 3. Crops By Category
`GET /api/v1/crops/{category_id}`
Returns crops registered in the category along with operational status (`ready`, `experimental`, `planned`) and active classes.

### 4. Platform Capabilities
`GET /api/v1/capabilities`
Returns allowed formats, upload size limits (10 MB), and count of active operational models.

### 5. Benchmark Evaluations
`GET /api/v1/evaluations`
Returns verified test metrics, confusion matrices, and latency reports.

### 6. Disease Inference
`POST /api/v1/predict`
Multipart Form:
- `category`: string (e.g. `grain_crop_leaf`)
- `crop`: string (e.g. `rice_leaf`)
- `file`: image file (JPEG, PNG, WebP)

Returns structured JSON containing:
- `prediction_id`: Unique diagnosis tracking ID
- `predicted_condition`: Canonical condition code
- `display_name`: Human-friendly condition title
- `confidence`: Softmax probability score
- `is_reliable`: Boolean (false if confidence < threshold or entropy > threshold)
- `alternative_predictions`: Top-3 class probabilities
- `severity`: Empirical lesion percentage and clinical level
- `gradcam_heatmap`: Base64-encoded JPEG image showing neural attention
- `symptoms`, `causes`, `prevention`, `management`, `consult_expert_when`, `references`
- `model_metadata` and `processing_time_ms`
