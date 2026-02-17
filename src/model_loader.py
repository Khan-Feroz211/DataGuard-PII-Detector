"""Model loading utilities for DataGuard."""

from transformers import AutoModelForSequenceClassification, AutoTokenizer

from src.config import MODEL_BASE_PATH, get_supported_tiers, get_supported_versions, is_valid_model_combo


def resolve_model_path(model_tier, version):
    if not is_valid_model_combo(model_tier, version):
        supported_tiers = ", ".join(get_supported_tiers())
        supported_versions = ", ".join(get_supported_versions(model_tier)) or "none"
        raise ValueError(
            f"Unsupported model selection tier='{model_tier}', version='{version}'. "
            f"Supported tiers: {supported_tiers}. "
            f"Supported versions for '{model_tier}': {supported_versions}."
        )

    return (MODEL_BASE_PATH / model_tier / version).resolve()


def load_pii_model(model_tier, version):
    model_path = resolve_model_path(model_tier, version)
    if not model_path.exists():
        raise FileNotFoundError(
            f"Model weights not found at '{model_path}'. "
            "Run `python -m src.setup_models` to download weights first."
        )

    print(f"Loading sequence classifier from: {model_path}")
    tokenizer = AutoTokenizer.from_pretrained(str(model_path))
    model = AutoModelForSequenceClassification.from_pretrained(str(model_path))
    return tokenizer, model
