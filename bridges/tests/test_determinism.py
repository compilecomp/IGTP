"""End-to-end determinism: identical pipeline runs produce identical bytes."""

import json

from igtp_engine import pipeline


def _canonical(run: dict) -> str:
    return json.dumps(run, sort_keys=True, separators=(",", ":"))


def test_pipeline_is_deterministic() -> None:
    first = _canonical(pipeline.run_pipeline())
    second = _canonical(pipeline.run_pipeline())
    assert first == second


def test_pipeline_output_structure_is_complete() -> None:
    parsed = json.loads(_canonical(pipeline.run_pipeline()))
    assert set(parsed) == {"engine_version", "z3_version", "graph", "tasks",
                           "lean_certificate_sha256"}
    assert len(parsed["tasks"]) == 3
    assert len(parsed["graph"]["nodes"]) == 12
    assert len(parsed["graph"]["edges"]) == 15


def test_all_resolutions_sound_and_smt_agrees() -> None:
    parsed = json.loads(_canonical(pipeline.run_pipeline()))
    for task in parsed["tasks"]:
        assert task["resolution"]["sound"] is True
        assert task["resolution"]["refuted"] is True
        assert task["smt"]["status"] == "unsat"
