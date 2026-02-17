"""FastAPI service exposing DataGuard inference endpoints."""

from functools import lru_cache
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.inference import PIIDetector

app = FastAPI(title="DataGuard API", version="1.0.0")


class PredictRequest(BaseModel):
    text: str = Field(..., min_length=1)
    tier: str = "base"
    version: str = "v4"
    threshold: float = Field(0.5, ge=0.0, le=1.0)
    placeholder_filter: bool = True


class BatchPredictRequest(BaseModel):
    texts: List[str] = Field(..., min_length=1)
    tier: str = "base"
    version: str = "v4"
    threshold: float = Field(0.5, ge=0.0, le=1.0)
    placeholder_filter: bool = True
    batch_size: int = Field(16, gt=0)


@lru_cache(maxsize=32)
def _get_detector(tier, version, threshold, placeholder_filter):
    return PIIDetector(
        tier=tier,
        version=version,
        leak_threshold=threshold,
        ignore_test_placeholders=placeholder_filter,
    )


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(payload: PredictRequest):
    try:
        detector = _get_detector(
            payload.tier,
            payload.version,
            payload.threshold,
            payload.placeholder_filter,
        )
        return detector.predict(payload.text)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/predict-batch")
def predict_batch(payload: BatchPredictRequest):
    try:
        detector = _get_detector(
            payload.tier,
            payload.version,
            payload.threshold,
            payload.placeholder_filter,
        )
        return {"results": detector.predict_many(payload.texts, batch_size=payload.batch_size)}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
