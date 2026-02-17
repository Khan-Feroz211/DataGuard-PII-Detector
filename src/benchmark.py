"""Simple benchmark utility for DataGuard model tiers."""

import argparse
import time

from src.inference import PIIDetector


def run_benchmark(iterations=10, warmup=1, threshold=0.5):
    test_sample = "Please transfer funds to IBAN PK12BANK0000001234567890 for CNIC 42101-1111111-1."
    tiers = [("base", "v4"), ("small", "v7"), ("tiny", "v4")]

    print(f"{'Tier':<10} | {'Load(s)':<10} | {'Avg Infer(ms)':<14} | {'Status':<6} | {'Conf':<8}")
    print("-" * 70)

    for tier, version in tiers:
        load_start = time.perf_counter()
        detector = PIIDetector(tier=tier, version=version, leak_threshold=threshold)
        load_seconds = time.perf_counter() - load_start

        for _ in range(warmup):
            detector.predict(test_sample)

        infer_start = time.perf_counter()
        last_result = None
        for _ in range(iterations):
            last_result = detector.predict(test_sample)
        infer_seconds = time.perf_counter() - infer_start

        avg_infer_ms = (infer_seconds / iterations) * 1000
        print(
            f"{tier:<10} | {load_seconds:<10.4f} | {avg_infer_ms:<14.2f} | "
            f"{last_result['status']:<6} | {last_result['confidence']:<8}"
        )


def build_parser():
    parser = argparse.ArgumentParser(description="Benchmark DataGuard model tiers.")
    parser.add_argument("--iterations", type=int, default=10, help="Timed inference runs per tier.")
    parser.add_argument("--warmup", type=int, default=1, help="Warmup runs per tier before timing.")
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.5,
        help="Leak threshold forwarded to PIIDetector.",
    )
    return parser


def main():
    args = build_parser().parse_args()
    run_benchmark(iterations=args.iterations, warmup=args.warmup, threshold=args.threshold)


if __name__ == "__main__":
    main()
