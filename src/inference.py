"""Inference entrypoint for DataGuard sequence classification."""

import argparse
import json

import torch
import torch.nn.functional as F

from src.model_loader import load_pii_model


def determine_status(
    prediction,
    probabilities,
    text,
    leak_threshold=0.5,
    ignore_test_placeholders=True,
):
    if not 0.0 <= leak_threshold <= 1.0:
        raise ValueError("`leak_threshold` must be between 0.0 and 1.0.")

    if len(probabilities) == 2:
        leak_probability = float(probabilities[1])
        is_leak = leak_probability >= leak_threshold
        confidence = leak_probability if is_leak else 1.0 - leak_probability
    else:
        is_leak = int(prediction) == 1
        confidence = float(probabilities[int(prediction)])

    contains_test_placeholder = any(
        token in text.lower() for token in ("fake", "dummy", "test case")
    )

    if is_leak and ignore_test_placeholders and contains_test_placeholder:
        return "SAFE", confidence, "placeholder_override"

    return ("LEAK" if is_leak else "SAFE"), confidence, "model_prediction"


class PIIDetector:
    def __init__(
        self,
        tier="base",
        version="v4",
        ignore_test_placeholders=True,
        leak_threshold=0.5,
    ):
        if not 0.0 <= leak_threshold <= 1.0:
            raise ValueError("`leak_threshold` must be between 0.0 and 1.0.")

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.ignore_test_placeholders = ignore_test_placeholders
        self.leak_threshold = leak_threshold
        self.tokenizer, self.model = load_pii_model(tier, version)
        self.model.to(self.device)
        self.model.eval()

    def _build_result(self, prediction, probabilities, text):
        status, confidence, reason = determine_status(
            prediction=prediction,
            probabilities=probabilities,
            text=text,
            leak_threshold=self.leak_threshold,
            ignore_test_placeholders=self.ignore_test_placeholders,
        )
        return {
            "status": status,
            "confidence": f"{confidence:.2%}",
            "label_id": int(prediction),
            "reason": reason,
            "leak_threshold": self.leak_threshold,
        }

    def predict(self, text):
        if not isinstance(text, str) or not text.strip():
            raise ValueError("`text` must be a non-empty string.")

        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=128,
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs)

        probs = F.softmax(outputs.logits, dim=-1)
        prediction = int(torch.argmax(probs, dim=-1).item())
        probabilities = probs[0].tolist()
        return self._build_result(prediction, probabilities, text)

    def predict_many(self, texts, batch_size=16):
        if not isinstance(texts, list) or not texts:
            raise ValueError("`texts` must be a non-empty list of strings.")
        if any(not isinstance(t, str) or not t.strip() for t in texts):
            raise ValueError("All items in `texts` must be non-empty strings.")
        if batch_size <= 0:
            raise ValueError("`batch_size` must be greater than 0.")

        results = []
        for start in range(0, len(texts), batch_size):
            chunk = texts[start : start + batch_size]
            inputs = self.tokenizer(
                chunk,
                return_tensors="pt",
                truncation=True,
                padding=True,
                max_length=128,
            ).to(self.device)

            with torch.no_grad():
                outputs = self.model(**inputs)

            probs = F.softmax(outputs.logits, dim=-1)
            predictions = torch.argmax(probs, dim=-1).tolist()
            for idx, text in enumerate(chunk):
                results.append(self._build_result(predictions[idx], probs[idx].tolist(), text))

        return results


def build_parser():
    parser = argparse.ArgumentParser(description="Run DataGuard inference on text.")
    parser.add_argument("--tier", default="base", help="Model tier: base, small, tiny")
    parser.add_argument("--version", default="v4", help="Model version, e.g. v4")
    parser.add_argument(
        "--text",
        default="User Hasan logged in with CNIC 42101-1234567-1",
        help="Single text to classify.",
    )
    parser.add_argument(
        "--texts",
        nargs="+",
        help="Batch texts to classify. If set, batch mode is used.",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=16,
        help="Batch size for --texts mode.",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.5,
        help="Leak probability threshold for binary classifiers (0.0 to 1.0).",
    )
    parser.add_argument(
        "--no-placeholder-filter",
        action="store_true",
        help="Disable post-filter that marks fake/dummy/test-case leaks as SAFE.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON output for pipeline integrations.",
    )
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    detector = PIIDetector(
        tier=args.tier,
        version=args.version,
        ignore_test_placeholders=not args.no_placeholder_filter,
        leak_threshold=args.threshold,
    )

    if args.texts:
        result = detector.predict_many(args.texts, batch_size=args.batch_size)
    else:
        result = detector.predict(args.text)

    if args.json:
        print(json.dumps(result))
        return

    if isinstance(result, list):
        for idx, item in enumerate(result, start=1):
            print(
                f"[{idx}] {item['status']} | Confidence: {item['confidence']} | "
                f"Reason: {item['reason']} | Threshold: {item['leak_threshold']:.2f}"
            )
    else:
        print(
            f"Audit: {result['status']} | Confidence: {result['confidence']} | "
            f"Reason: {result['reason']} | Threshold: {result['leak_threshold']:.2f}"
        )


if __name__ == "__main__":
    main()
