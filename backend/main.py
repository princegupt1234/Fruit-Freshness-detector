from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from backend.database.db import Base, engine
from backend.database.init_db import init_database
from backend.routes.dashboard import router as dashboard_router
from backend.routes.history import router as history_router
from backend.routes.prediction import router as prediction_router

load_dotenv()

app = FastAPI(title="AI FreshCheck API", version=os.getenv("MODEL_VERSION", "v1.0"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_database()

app.include_router(prediction_router)
app.include_router(history_router)
app.include_router(dashboard_router)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "AI FreshCheck",
        "version": os.getenv("MODEL_VERSION", "v1.0")
    }
