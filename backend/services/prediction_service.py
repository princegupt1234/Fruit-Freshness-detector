from typing import Any, Dict, List

from sqlalchemy.orm import Session

from backend.database.db import SessionLocal
from backend.models.prediction import Prediction


def save_prediction_record(data: Dict[str, Any]) -> Prediction:
    db: Session = SessionLocal()
    try:
        record = Prediction(
            produce_name=data.get("produce"),
            produce_category=data.get("category"),
            freshness_status=data.get("freshness"),
            confidence=float(data.get("confidence", 0.0) or 0.0),
            image_path=data.get("image_path"),
            model_version=data.get("model_version", "v1.0"),
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record
    finally:
        db.close()


def get_prediction_history() -> List[Dict[str, Any]]:
    db: Session = SessionLocal()
    try:
        rows = db.query(Prediction).order_by(Prediction.created_at.desc()).all()
        return [
            {
                "id": row.id,
                "produce_name": row.produce_name,
                "produce_category": row.produce_category,
                "freshness_status": row.freshness_status,
                "confidence": row.confidence,
                "image_path": row.image_path,
                "model_version": row.model_version,
                "created_at": row.created_at.isoformat() if row.created_at else None,
            }
            for row in rows
        ]
    finally:
        db.close()


def get_dashboard_statistics() -> Dict[str, Any]:
    db: Session = SessionLocal()
    try:
        rows = db.query(Prediction).all()
        total_predictions = len(rows)
        fresh_predictions = 0
        moderately_fresh_predictions = 0
        rotten_predictions = 0
        unknown_predictions = 0
        total_confidence = 0.0

        for row in rows:
            status = (row.freshness_status or "").strip().lower()
            if status in {"fresh"}:
                fresh_predictions += 1
            elif status in {"moderately fresh", "moderately_fresh", "moderatelyfresh"}:
                moderately_fresh_predictions += 1
            elif status in {"rotten", "spoiled"}:
                rotten_predictions += 1
            elif status in {"unknown", ""}:
                unknown_predictions += 1
            else:
                unknown_predictions += 1

            total_confidence += float(row.confidence or 0.0)

        average_confidence = round(total_confidence / total_predictions, 2) if total_predictions else 0.0

        return {
            "total_predictions": total_predictions,
            "fresh_predictions": fresh_predictions,
            "moderately_fresh_predictions": moderately_fresh_predictions,
            "rotten_predictions": rotten_predictions,
            "unknown_predictions": unknown_predictions,
            "average_confidence": average_confidence,
            "message": "Prediction statistics loaded from the database." if total_predictions else "No prediction data available yet.",
        }
    finally:
        db.close()
