# DataGuard Change Report

## Scope
This report summarizes all enhancements implemented during this improvement pass.

## Completed Changes
1. Inference post-processing controls
- Added `determine_status(...)` to centralize decision logic.
- Added configurable `leak_threshold` support.
- Preserved practical placeholder override (`fake`, `dummy`, `test case`) with on/off switch.
- Included `reason` and `leak_threshold` in outputs.

2. Throughput support
- Added `PIIDetector.predict_many(texts, batch_size=...)` for batched inference.
- Added input validation for batch mode.

3. CLI pipeline integration
- Added `--json` output mode for machine-readable output.
- Added `--texts` and `--batch-size` for batch CLI usage.

4. Model setup improvements
- Added tier-selective download in `src.setup_models` via `--tier all|base|small|tiny`.

5. Production service layer
- Added `src/api.py` using FastAPI.
- Endpoints:
  - `GET /health`
  - `POST /predict`
  - `POST /predict-batch`
- Added detector caching for repeated tier/version/threshold/filter combinations.

6. Testing
- Added pytest cases for:
  - threshold-driven SAFE/LEAK behavior
  - placeholder override enabled behavior
  - placeholder override disabled behavior

7. Dependencies and docs
- Added runtime dependencies: `fastapi`, `uvicorn`, `pytest`.
- Extended README with testing commands, advanced CLI examples, and API usage examples.
- Added `ARCHITECTURE.md` including full working-process diagram.

## Files Added
- `src/api.py`
- `tests/test_inference_post_processing.py`
- `ARCHITECTURE.md`
- `CHANGE_REPORT.md`

## Files Updated
- `src/inference.py`
- `src/setup_models.py`
- `src/benchmark.py`
- `requirements.txt`
- `README.md`
- plus previously updated: `src/config.py`, `src/model_loader.py`

## Validation Summary
- Python syntax check passed for updated modules.
- Unit tests added; execution requires environment dependencies available.

## Runbook
```bash
pip install -r requirements.txt
python -m src.setup_models --tier all
pytest -q
python -m src.inference --json --text "User CNIC is 42101-1234567-1"
uvicorn src.api:app --host 0.0.0.0 --port 8000
```
