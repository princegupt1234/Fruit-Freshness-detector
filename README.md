<<<<<<< HEAD
# Universal Fruit & Vegetable Freshness Detection System

This project is being built in stages, following the requirement specification for a production-style AI freshness detection application.

## Stage-by-stage development plan

1. Stage 1 — Architecture, technology choices, project scaffold, API design, and ML planning
2. Stage 2 — Dataset validation and preprocessing
3. Stage 3 — Model training
4. Stage 4 — Model evaluation and reporting
5. Stage 5 — Prediction and inference pipeline
6. Stage 6 — FastAPI backend
7. Stage 7 — MySQL integration and persistence
8. Stage 8 — Frontend UI
9. Stage 9 — Camera capture
10. Stage 10 — Dashboard and prediction history
11. Stage 11 — Grad-CAM explainability
12. Stage 12 — Integration, testing, and deployment readiness

## Architecture summary

- Frontend: static HTML/CSS/JS pages served locally or through FastAPI
- Backend: FastAPI REST API
- ML pipeline: TensorFlow/Keras transfer learning using MobileNetV2 or EfficientNetB0/B1
- Database: MySQL for prediction records and statistics
- Storage: local uploads folder for development; S3-ready structure for AWS deployment
- Model config: dynamic class mapping via classes.json, not hard-coded UI logic

## Project structure

```text
fruit-freshness-detector/
├── frontend/
│   ├── index.html
│   ├── predict.html
│   ├── history.html
│   ├── dashboard.html
│   ├── model.html
│   ├── css/
│   └── js/
├── backend/
│   ├── main.py
│   ├── routes/
│   │   ├── prediction.py
│   │   ├── history.py
│   │   └── dashboard.py
│   ├── services/
│   ├── database/
│   ├── models/
│   └── utils/
├── ml/
│   ├── dataset/
│   ├── preprocessing/
│   ├── models/
│   ├── notebooks/
│   ├── train.py
│   ├── evaluate.py
│   ├── predict.py
│   ├── gradcam.py
│   └── dataset_validator.py
├── uploads/
├── results/
├── classes.json
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── docs/
    └── stage-01-architecture.md
```

## Recommended ML approach

The project will use transfer learning instead of training a CNN from scratch. The preferred models are:

- MobileNetV2
- EfficientNetB0
- EfficientNetB1

The implementation will select the model based on dataset scale, training time, accuracy, and inference speed. The final choice will be documented after evaluation.

## Database schema

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

## API design

- GET /health
- POST /predict
- GET /history
- GET /statistics
- GET /supported-produce
- GET /model-info

## Key principles

- No hard-coded fruit or freshness rules
- Model-driven predictions only
- Unknown/unsupported images handled via threshold logic
- Dynamic class loading from model configuration
- Dataset-independent training pipeline
- Local development first, AWS-ready future deployment

## Stage 1 status

This stage establishes the project architecture and scaffold. The next stage will implement dataset validation and preprocessing.
=======
# Fruit-Freshness-detector
>>>>>>> 071b58945478a69608e24ee45094cfbbbc8d353a
