from backend.database.db import Base, engine
from backend.models.prediction import Prediction


def init_database() -> None:
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully.")
