# DataGuard Architecture

## Overview
DataGuard uses a sequence-classification model pipeline with post-processing controls for practical DLP behavior.

## End-to-End Working Flow
```mermaid
flowchart TD
    A[Input Text or Batch] --> B[Tokenizer]
    B --> C[Model Inference\nBERT/DistilBERT/MobileBERT]
    C --> D[Softmax Probabilities]
    D --> E{Binary Head?}
    E -- Yes --> F[Apply Leak Threshold]
    E -- No --> G[Use Predicted Class]
    F --> H[Placeholder Override Check\nfake/dummy/test case]
    G --> H
    H --> I[Result Object\nstatus, confidence, label_id, reason, threshold]
    I --> J1[CLI Output\nplain or --json]
    I --> J2[Batch Output\npredict_many]
    I --> J3[FastAPI Response\n/predict or /predict-batch]
```

## Components
- `src/model_loader.py`: validates tier/version and loads tokenizer/model from `models/`.
- `src/inference.py`: single/batch inference, thresholding, placeholder override, JSON CLI mode.
- `src/setup_models.py`: full or tier-specific weight download from Hugging Face.
- `src/benchmark.py`: benchmark with warmup/iterations and threshold passthrough.
- `src/api.py`: production-friendly REST endpoints.
- `tests/test_inference_post_processing.py`: behavior tests for threshold and override logic.
