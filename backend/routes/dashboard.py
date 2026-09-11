import json
from pathlib import Path

from fastapi import APIRouter

from backend.services.prediction_service import get_dashboard_statistics

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/statistics")
def statistics():
    return get_dashboard_statistics()


@router.get("/supported-produce")
def supported_produce():
    config_path = Path("classes.json")
    if not config_path.exists():
        return {"supported_produce": [], "message": "No class configuration found."}

    with config_path.open("r", encoding="utf-8") as handle:
        config = json.load(handle)

    labels = config.get("labels", {})
    supported = []
    for index in sorted((int(key) for key in labels.keys())):
        label = labels[str(index)]
        if label and label != "Unknown":
            supported.append(label)

    return {"supported_produce": supported, "message": "Supported produce loaded from the class configuration."}


@router.get("/model-info")
def model_info():
    model_path = Path("ml/models/freshness_model.keras")
    config_path = Path("classes.json")
    title = "transfer_learning_freshness_detector"
    version = "v1.0"

    if model_path.exists() and config_path.exists():
        return {
            "model_name": title,
            "model_version": version,
            "status": "trained",
            "message": "Model is trained and ready for inference."
        }

    return {
        "model_name": title,
        "model_version": version,
        "status": "not_trained",
        "message": "Model not trained. Please train the model using the provided dataset."
    }
