# DataGuard-PII-Detector
This repository hosts the DataGuard DLP Project's Machine Learning Models. These models (using the BERT NLP Family) have been trained and fine-tuned on datasets up to the size of 100k and tested with different versions. Used BERT: Base, Small, Tiny. The latest versions are ready for use and can be fine-tuned further as needed.

---

# Ã°Å¸â€ºÂ¡Ã¯Â¸Â DataGuard: Contextual PII Detection System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Hugging Face](https://img.shields.io/badge/Models-Hugging%20Face-yellow?logo=huggingface&logoColor=black)](https://huggingface.co/theinvinciblehasnainali/DataGuard-Weights)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)]()

**DataGuard** is a Deep Learning-based Data Leakage Prevention (DLP) engine designed specifically for identifying sensitive Pakistani Personally Identifiable Information (PII) with high contextual awareness.

Unlike traditional Regex-based scanners that blindly flag every 13-digit number, DataGuard uses **BERT Sequence Classification** to understand the *intent* behind the data. It accurately distinguishes between a harmless serial number and a genuine CNIC leak.

---

## Ã°Å¸Å’Å¸ Key Features

* **Context-Aware Analysis:** uses the `bert-base-uncased` architecture to analyze the surrounding words of a potential leak.
    * *Example:* "Order ID 42101..." Ã¢Å¾Â¡Ã¯Â¸Â **Ã°Å¸Å¸Â¢ SAFE**
    * *Example:* "User CNIC is 42101..." Ã¢Å¾Â¡Ã¯Â¸Â **Ã°Å¸â€Â´ LEAK**
* **High-Precision Models:** Achieves **99.96% confidence** on validation datasets containing mixed Pakistani PII (CNIC, IBAN, Phone Numbers).
* **Multi-Tier Architecture:** Deployable on everything from cloud servers to edge devices.
    * **Base (v4):** Maximum Accuracy (Server-grade).
    * **Small (v7):** Balanced performance.
    * **Tiny (v4):** Ultra-fast inference for real-time streams.
* **Automated Weight Management:** Built-in scripts to sync heavy model weights (4GB+) directly from Hugging Face.

---

## Ã°Å¸Ââ€”Ã¯Â¸Â Architecture & Performance

DataGuard moves beyond simple Named Entity Recognition (NER) by utilizing **Sequence Classification**. The model evaluates the entire semantic structure of a sentence to determine if it constitutes a security risk.

| Model Tier | Backbone | Size | Use Case | Accuracy |
| :--- | :--- | :--- | :--- | :--- |
| **DataGuard Base** | BERT-Base | ~420 MB | Deep Audits / Forensics | **99.96%** |
| **DataGuard Small** | DistilBERT | ~260 MB | Real-time API | 97.5% |
| **DataGuard Tiny** | MobileBERT | ~120 MB | Browser / Edge / Mobile | 94.2% |

---

## Ã°Å¸â€˜Â¥ Project Team

This project is the result of a collaborative effort to bring advanced AI security to the DataGuard ecosystem.

| Name | Role | Contribution |
| :--- | :--- | :--- |
| **Hasnain Ali** | **Lead AI Engineer & UI/UX** | Model Training (BERT Fine-tuning), Inference Logic, & Frontend Design. |
| **Hassan Naseer** | Project Manager | Project Architecture, Roadmap Planning, and Resource Management. |
| **Sayyad Ali Naqi** | Backend Engineer | API Integration, Database Management, and Server Deployment. |
| **Feroz u Din** | ML Operations (MLOps) | Pipeline Automation, Model Versioning, and Deployment Strategy. |
| **Hafiz M. Imdadullah Chishti** | Frontend Engineer | Dashboard Implementation and Client-Side Logic. |

---

## Ã°Å¸Å¡â‚¬ Installation & Setup

### Prerequisites
* Python 3.8 or higher
* Git
* Internet connection (for downloading weights)

### 1. Clone the Repository
```bash
git clone https://github.com/theinvinciblehasnainali/DataGuard-PII-Detector.git
cd DataGuard-PII-Detector

```

### 2. Install Dependencies

We recommend using a virtual environment.

```bash
# Create and activate virtual environment (Windows)
python -m venv venv
.\venv\Scripts\activate

# Install requirements
pip install -r requirements.txt

```

### 3. Download Model Weights (Automated)

Since the model weights (~4.30 GB) are too large for GitHub, they are hosted on Hugging Face. We have provided a setup script to handle this automatically.

```bash
python -m src.setup_models --tier all

```

*This script will fetch the `base`, `small`, and `tiny` models from [Hugging Face](https://huggingface.co/theinvinciblehasnainali/DataGuard-Weights) and place them in the `models/` directory.*

---

## Ã°Å¸â€™Â» Usage

### Quick Audit (Command Line)

To test the model immediately on a sample string:

```bash
python -m src.inference --tier base --version v4 --threshold 0.60 --text "User CNIC is 42101-1234567-1"

```

### Python API Integration

You can easily import DataGuard into your own Python scripts:

```python
from src.inference import PIIDetector

# Initialize the detector (Choose 'base', 'small', or 'tiny')
detector = PIIDetector(tier="base", version="v4")

# Run a prediction
text = "The user with CNIC 42101-1234567-1 accessed the system."
result = detector.predict(text)

print(result)
# Output:
# {
#   "status": "LEAK",
#   "confidence": "99.96%",
#   "label_id": 1
#   "reason": "model_prediction"
# }

```

---

## Ã°Å¸â€Â® Roadmap & Future Enhancements

We are constantly improving DataGuard. Here is what's coming next:

* **[ ] PDF & Document Scanning:** Direct support for scanning invoices, resumes, and legal documents.
* **[ ] OCR Integration:** Detecting PII inside images and scanned IDs.
* **[ ] API Containerization:** Docker support for easy cloud deployment (AWS/Azure).

---

## Ã°Å¸â€œâ€ž License

This project is licensed under the **MIT License** - see the [LICENSE](https://www.google.com/search?q=LICENSE) file for details.

---

## Ã°Å¸â„¢Â Acknowledgments

* **Hugging Face:** For hosting the model weights and providing the `transformers` library.
* **Google Research:** For the original BERT architecture.


### Advanced Commands

```bash
# Download only one tier to save bandwidth/disk
python -m src.setup_models --tier tiny

# Disable placeholder override (strict model decision)
python -m src.inference --no-placeholder-filter --text "dummy CNIC 42101-1234567-1"

# Run benchmark with custom timing controls
python -m src.benchmark --iterations 30 --warmup 3 --threshold 0.55
```

---

## Testing

```bash
pytest -q
```

## Advanced CLI Usage

```bash
# Single inference in JSON mode
python -m src.inference --json --tier base --version v4 --threshold 0.60 --text "User CNIC is 42101-1234567-1"

# Batch inference in JSON mode
python -m src.inference --json --texts "dummy CNIC 42101-1234567-1" "Order ID 12345" --batch-size 8

# Disable placeholder override
python -m src.inference --no-placeholder-filter --text "dummy CNIC 42101-1234567-1"
```

## REST API Service (FastAPI)

```bash
# Start API server
uvicorn src.api:app --host 0.0.0.0 --port 8000
```

```bash
# Health check
curl http://127.0.0.1:8000/health

# Single prediction
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"User CNIC is 42101-1234567-1","tier":"base","version":"v4","threshold":0.6,"placeholder_filter":true}'

# Batch prediction
curl -X POST http://127.0.0.1:8000/predict-batch \
  -H "Content-Type: application/json" \
  -d '{"texts":["dummy CNIC 42101-1234567-1","Order ID 12345"],"tier":"base","version":"v4","threshold":0.5,"placeholder_filter":true,"batch_size":8}'
```
