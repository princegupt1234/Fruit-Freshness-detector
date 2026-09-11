from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func

from backend.database.db import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    produce_name = Column(String(255), nullable=True)
    produce_category = Column(String(50), nullable=True)
    freshness_status = Column(String(50), nullable=True)
    confidence = Column(Float, nullable=True)
    image_path = Column(String(500), nullable=True)
    model_version = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
