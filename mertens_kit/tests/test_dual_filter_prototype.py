import json
import sys
from pathlib import Path


def test_dual_filter_prototype_real_zeros(tmp_path, monkeypatch):
    import s09_dual_filter_prototype as prototype

    output = tmp_path / "dual_filter.json"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "s09_dual_filter_prototype.py",
            "--m", "5",
            "--N", "2",
            "--bits", "160",
            "--external", "8",
            "--dual-k", "3",
            "--dual-window", "16",
            "--output", str(output),
        ],
    )
    prototype.main()
    payload = json.loads(output.read_text(encoding="utf-8"))

    assert payload["parameters"]["m"] == 5
    assert payload["parameters"]["N"] == 2
    assert payload["enumerated_primal_points"] > 0
    assert len(payload["external_results"]) == 8

    for row in payload["external_results"]:
        exact = prototype.Fraction(row["exact_cvp_min_sq"])
        for bound in row["dual_bounds"]:
            if bound["total_lower_sq"] is not None:
                assert prototype.Fraction(bound["total_lower_sq"]) <= exact
