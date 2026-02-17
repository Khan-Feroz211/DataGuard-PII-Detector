"""Project configuration for model metadata and paths."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_BASE_PATH = PROJECT_ROOT / "models"

MODEL_VERSIONS = {
    "tiny": {
        "versions": ["v1", "v2", "v4"],
        "dataset_size": {"v1": "20k", "v2": "20k", "v4": "50k"},
        "description": "Fastest, lowest latency, lower contextual depth.",
    },
    "small": {
        "versions": ["v4", "v5", "v6", "v7"],
        "dataset_size": "50k",
        "description": "Balanced performance and accuracy.",
    },
    "base": {
        "versions": ["v2", "v4"],
        "dataset_size": "100k",
        "description": "Highest accuracy, best for complex PII validation.",
    },
}

LABELS = [
    "O",             # Outside (No PII)
    "B-CNIC",        # Pakistani CNIC
    "B-IBAN",        # Bank IBAN
    "B-PHONE",       # Phone Number
    "B-CREDIT_CARD", # Credit Card
    "B-EMAIL",       # Email Address
    "B-SECRET_KEY",  # API/Secret Keys
]


def get_supported_tiers():
    return sorted(MODEL_VERSIONS.keys())


def get_supported_versions(model_tier):
    tier_meta = MODEL_VERSIONS.get(model_tier)
    if not tier_meta:
        return []
    return tier_meta.get("versions", [])


def is_valid_model_combo(model_tier, version):
    return version in get_supported_versions(model_tier)
