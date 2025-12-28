from aegis_d.assessment import select_most_concerning
from aegis_d.temporal import TemporalAggregator, TemporalStrategy
from aegis_d.actions import recommend_action


def assert_equal(a, b, msg):
    if a != b:
        raise AssertionError(f"{msg}\n  A={a}\n  B={b}")


def test_determinism():
    detections = [
        {"distance_m": 3.0, "ttc_s": 4.0},
        {"distance_m": 8.0, "ttc_s": 2.5},
    ]
    a1 = select_most_concerning(detections)
    a2 = select_most_concerning(detections)

    assert_equal(a1.risk_level, a2.risk_level, "Risk level not deterministic")
    assert_equal(a1.risk_score, a2.risk_score, "Risk score not deterministic")
    assert_equal(a1.input_hash, a2.input_hash, "Hash not deterministic")


def test_input_order_independence():
    detections_a = [
        {"distance_m": 3.0, "ttc_s": 4.0},
        {"distance_m": 1.9, "ttc_s": 9.0},
    ]
    detections_b = list(reversed(detections_a))

    a = select_most_concerning(detections_a)
    b = select_most_concerning(detections_b)

    assert_equal(a.risk_level, b.risk_level, "Order changed risk level")
    assert_equal(a.distance_m, b.distance_m, "Order changed selected distance")
    assert_equal(a.ttc_s, b.ttc_s, "Order changed selected TTC")


def test_temporal_conservative_default():
    detections_low = [{"distance_m": 9.0, "ttc_s": 9.0}]
    detections_spike = [{"distance_m": 1.5, "ttc_s": 9.0}]  # critical via distance

    agg = TemporalAggregator(window_size=3, strategy=TemporalStrategy.MAX)

    a1 = agg.update(select_most_concerning(detections_low))
    a2 = agg.update(select_most_concerning(detections_spike))
    a3 = agg.update(select_most_concerning(detections_low))

    # MAX should preserve the spike within window
    assert a2.risk_level == a3.risk_level, "MAX aggregation hid spike"


def test_human_gate():
    detections = [{"distance_m": 1.5, "ttc_s": 9.0}]  # critical
    a = select_most_concerning(detections)
    rec = recommend_action(a)
    assert rec.requires_human_approval is True, "Critical risk must require human approval"


def main():
    print("Running AEGIS-D validations...\n")

    test_determinism()
    print("✓ determinism")

    test_input_order_independence()
    print("✓ input-order independence")

    test_temporal_conservative_default()
    print("✓ temporal conservative default (MAX)")

    test_human_gate()
    print("✓ human approval gate")

    print("\nAll validations passed.")


if __name__ == "__main__":
    main()
