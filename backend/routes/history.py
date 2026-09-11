from fastapi import APIRouter

from backend.services.prediction_service import get_prediction_history

router = APIRouter(prefix="/api/history", tags=["history"])


@router.get("")
def list_history():
    history = get_prediction_history()
    return {
        "history": history,
        "message": "Prediction history loaded from the database." if history else "Prediction history is empty."
    }
