from src.inference import determine_status


def test_threshold_marks_safe_when_below_cutoff():
    status, confidence, reason = determine_status(
        prediction=1,
        probabilities=[0.45, 0.55],
        text="User CNIC 42101-1234567-1",
        leak_threshold=0.80,
        ignore_test_placeholders=True,
    )
    assert status == "SAFE"
    assert reason == "model_prediction"
    assert confidence == 0.45


def test_threshold_marks_leak_when_above_cutoff():
    status, confidence, reason = determine_status(
        prediction=0,
        probabilities=[0.20, 0.80],
        text="User CNIC 42101-1234567-1",
        leak_threshold=0.60,
        ignore_test_placeholders=True,
    )
    assert status == "LEAK"
    assert reason == "model_prediction"
    assert confidence == 0.80


def test_placeholder_override_applies_on_leak():
    status, confidence, reason = determine_status(
        prediction=1,
        probabilities=[0.01, 0.99],
        text="dummy CNIC 42101-1234567-1",
        leak_threshold=0.50,
        ignore_test_placeholders=True,
    )
    assert status == "SAFE"
    assert reason == "placeholder_override"
    assert confidence == 0.99


def test_placeholder_override_can_be_disabled():
    status, confidence, reason = determine_status(
        prediction=1,
        probabilities=[0.01, 0.99],
        text="dummy CNIC 42101-1234567-1",
        leak_threshold=0.50,
        ignore_test_placeholders=False,
    )
    assert status == "LEAK"
    assert reason == "model_prediction"
    assert confidence == 0.99
