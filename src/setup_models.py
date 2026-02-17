"""Download model weights from Hugging Face into the local models directory."""

import argparse
from pathlib import Path

from huggingface_hub import snapshot_download


REPO_ID = "theinvinciblehasnainali/DataGuard-Weights"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOCAL_MODELS_DIR = PROJECT_ROOT / "models"


def _allow_patterns_for_tier(tier):
    if tier == "all":
        return None
    return [f"{tier}/**"]


def download_weights(tier="all"):
    print(f"Starting download from Hugging Face repo: {REPO_ID}")
    print(f"Destination: {LOCAL_MODELS_DIR}")
    print(f"Tier selection: {tier}")

    try:
        snapshot_download(
            repo_id=REPO_ID,
            local_dir=str(LOCAL_MODELS_DIR),
            local_dir_use_symlinks=False,
            repo_type="model",
            allow_patterns=_allow_patterns_for_tier(tier),
        )
        print("Success: model weights downloaded and ready for inference.")
    except Exception as exc:
        print(f"Error downloading models: {exc}")
        print("Verify repository visibility or authenticate with Hugging Face CLI.")


def build_parser():
    parser = argparse.ArgumentParser(description="Download DataGuard model weights.")
    parser.add_argument(
        "--tier",
        choices=["all", "base", "small", "tiny"],
        default="all",
        help="Download only one model tier or all tiers.",
    )
    return parser


def main():
    args = build_parser().parse_args()
    download_weights(tier=args.tier)


if __name__ == "__main__":
    main()
