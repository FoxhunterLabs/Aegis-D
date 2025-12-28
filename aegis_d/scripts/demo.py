from aegis_d.assessment import select_most_concerning
from aegis_d.temporal import TemporalAggregator, TemporalStrategy
from aegis_d.actions import recommend_action


def main():
    print("=" * 80)
    print("AEGIS-D DEMO (Deterministic Risk Assessment Kernel)")
    print("=" * 80)

    detections = [
        {"distance_m": 4.0, "ttc_s": 6.0},
        {"distance_m": 1.8, "ttc_s": 8.0},  # distance triggers CRITICAL
        {"distance_m": 6.0, "ttc_s": 1.5},  # ttc triggers CRITICAL
    ]

    assessment = select_most_concerning(detections)
    print("\nMost concerning assessment:")
    print(f"  risk_level:   {assessment.risk_level}")
    print(f"  risk_score:   {assessment.risk_score:.3f}")
    print(f"  distance_m:   {assessment.distance_m}")
    print(f"  ttc_s:        {assessment.ttc_s}")
    print(f"  input_hash:   {assessment.input_hash[:16]}...")

    rec = recommend_action(assessment)
    print("\nRecommendation:")
    print(f"  recommendation: {rec.recommendation}")
    print(f"  rationale:      {rec.rationale}")
    print(f"  human_gate:     {rec.requires_human_approval}")

    print("\nTemporal aggregation (MAX default):")
    agg = TemporalAggregator(window_size=5, strategy=TemporalStrategy.MAX)
    for i in range(3):
        a = select_most_concerning(detections)
        out = agg.update(a)
        print(f"  update {i+1}: level={out.risk_level}, score={out.risk_score:.3f}")

    print("\n" + "=" * 80)
    print("NOTE: Research prototype. Not for operational use.")
    print("=" * 80)


if __name__ == "__main__":
    main()
