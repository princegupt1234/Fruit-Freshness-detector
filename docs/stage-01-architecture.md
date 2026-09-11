# Stage 1: Architecture and Design

## 1. Architecture Overview

The application is structured as a modular full-stack system with a dedicated ML training and inference pipeline. The frontend is responsible for image upload and display, the backend handles API routes and persistence, and the ML layer performs preprocessing, training, evaluation, and inference. This separation keeps the project extensible and makes it easier to support additional produce types later.

## 2. Technology Choices

- Frontend: HTML, CSS, JavaScript
- API: FastAPI
- ML: TensorFlow/Keras with transfer learning
- Data processing: OpenCV, NumPy, Pandas, PIL
- Model evaluation: scikit-learn
- Database: MySQL
- Visualization: Chart.js for dashboard analytics
- Deployment readiness: environment-driven configuration, modular services, AWS-friendly design

## 3. ML Approach

The project will avoid manual image rules and instead use a deep learning model trained on actual produce images. A transfer-learning architecture is preferred because it typically gives better accuracy with less training time and less data than training a CNN from scratch.

Candidate models:

- MobileNetV2
- EfficientNetB0
- EfficientNetB1

The final model will be selected based on accuracy, training time, model size, and inference speed.

## 4. Dataset Strategy

The training pipeline will accept multiple folder layouts:

- produce_name/class directories
- produce_name_fresh and produce_name_rotten labels
- combined class names such as apple_fresh, banana_rotten, etc.

The dataset loader will inspect directory structure, validate image counts, flag missing classes, detect corrupt files, and generate a dynamic class map for training and inference.

## 5. Database Design

The project uses a MySQL table to store each prediction record. This enables the dashboard, history screen, and statistics computations to use real persisted data.

### Table structure

```sql
CREATE TABLE predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    produce_name VARCHAR(255),
    produce_category VARCHAR(50),
    freshness_status VARCHAR(50),
    confidence DECIMAL(5,4),
    image_path VARCHAR(500),
    model_version VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 6. API Design

The backend exposes endpoints for health checks, prediction requests, historical queries, statistics, supported produce retrieval, and model metadata.

### Required endpoints

- GET /health
- POST /predict
- GET /history
- GET /statistics
- GET /supported-produce
- GET /model-info

## 7. Frontend Design

The frontend includes:

- Home page with hero section and upload controls
- Prediction result page with image preview and confidence output
- History page with saved records
- Dashboard with charts and summary cards
- Model performance page for evaluation metrics

## 8. Security and Validation

The system will validate uploaded files before processing. It will check extension, MIME type, file size, safe names, secure upload path, and malicious-file handling. Uploaded content is never executed.

## 9. Unknown / Unsupported Image Handling

If the image does not appear to be a supported fruit or vegetable, the system returns an unknown result instead of a forced class. The decision uses model confidence and threshold logic, not rule-based color detection.

## 10. Deployment Readiness

The project is designed to work locally and remain AWS-ready. Local development uses standard environment variables and local file storage, while the architecture can later integrate with Amazon RDS and S3.

## 11. Migration to Stage 2

The next stage is to build a dataset validator and preprocessing script that can inspect folder data, validate image integrity, and create a dynamic mapping of supported classes before training begins.
