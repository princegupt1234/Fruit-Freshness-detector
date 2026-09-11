from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from pathlib import Path
import uuid

from backend.services.prediction_service import save_prediction_record
from ml.predict import predict_image

router = APIRouter(prefix="/api", tags=["prediction"])
UPLOAD_BASE_DIR = Path("uploads")
UPLOAD_BASE_DIR.mkdir(exist_ok=True, parents=True)


def allowed_extension(filename: str) -> bool:
    allowed = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
    return Path(filename).suffix.lower() in allowed


@router.get("/health")
def route_health():
    return {"status": "ok", "message": "Prediction route is available."}


@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded.")

    if not allowed_extension(file.filename or ""):
        raise HTTPException(status_code=400, detail="Unsupported file type. Please upload an image.")

    file_bytes = await file.read()
    if len(file_bytes) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File exceeds 10 MB size limit.")

    safe_name = f"{uuid.uuid4().hex}{Path(file.filename).suffix.lower()}"
    save_path = UPLOAD_BASE_DIR / safe_name
    save_path.write_bytes(file_bytes)

    try:
        result = predict_image(
            image_path=str(save_path),
            model_path="ml/models/freshness_model.keras",
            class_config_path="classes.json",
            threshold=0.55,
        )
        result["image_path"] = str(save_path)
        result["category"] = result.get("category") or "Unknown"
        save_prediction_record(result)
        return JSONResponse(content=result)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(exc)}")
