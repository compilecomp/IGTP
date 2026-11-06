#!/usr/bin/env python3
"""Demo experiment: end-to-end run of the IGTP reference pipeline.

Runs the pipeline over the demo manifold and the propositional task battery,
writes the run record to experiments/results/demo_run.json, emits the Lean
certificate to dep/out/lean/demo_certificate.lean, and compares the run
record against the golden artifact experiments/results/demo_golden.json.

Design (DEP&CC 2.0, Chapter 28):
  Status: exploratory (explicitly declared; there is no pre-registration).
  Estimand: the exact rational search energies and the derivation statistics
    of the reference pipeline on the declared demo instance.
  Determinism: the golden comparison covers every field except wall-clock
    timings, which are recorded under "informational" and are never
    load-bearing (arithmetic class: heuristic-numeric, Chapter 18.1).
  Seeds: the pipeline is fully deterministic; no sampling is performed.

Exit codes: 0 comparison passed; 1 mismatch or error; the run record and the
certificate are written in either case.

Usage: run_demo.py [--update-golden]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "bridges"))

from igtp_engine import pipeline  # noqa: E402
from igtp_engine.lean_bridge import LeanTask, emit_lean_certificate  # noqa: E402

GOLDEN = REPO / "experiments" / "results" / "demo_golden.json"
RUN = REPO / "experiments" / "results" / "demo_run.json"
CERT = REPO / "dep" / "out" / "lean" / "demo_certificate.lean"


def _canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--update-golden",
        action="store_true",
        help="replace the golden artifact with the current run record",
    )
    args = parser.parse_args()

    timings: dict[str, float] = {}
    start = time.perf_counter()
    run = pipeline.run_pipeline()
    timings["pipeline_seconds"] = round(time.perf_counter() - start, 6)

    lean_tasks: list[LeanTask] = []
    for task in pipeline.build_logic_tasks():
        lean_tasks.append(
            LeanTask(
                name="igtp_demo_" + task["id"].replace(":", "_"),
                prop_vars=task["vars"],
                hypotheses=[pipeline._formula_to_lean(h) for h in task["hypotheses"]],
                conclusion=pipeline._formula_to_lean(task["conclusion"]),
            )
        )
    certificate = emit_lean_certificate(lean_tasks)
    CERT.parent.mkdir(parents=True, exist_ok=True)
    CERT.write_text(certificate)

    record = {
        "run": run,
        "informational": {
            "wall_seconds": timings,
            "arithmetic_class": "exact (Fraction); timings are heuristic-numeric",
            "design_status": "exploratory",
        },
        "certificate_sha256": hashlib.sha256(certificate.encode()).hexdigest(),
    }
    RUN.parent.mkdir(parents=True, exist_ok=True)
    RUN.write_text(_canonical(record) + "\n")

    if args.update_golden:
        GOLDEN.write_text(_canonical(record) + "\n")
        print(f"golden updated: {GOLDEN}")
        return 0

    if not GOLDEN.exists():
        print(f"golden artifact missing: {GOLDEN}", file=sys.stderr)
        return 1
    golden = json.loads(GOLDEN.read_text())
    # The golden comparison covers the deterministic fields only:
    # `run` and `certificate_sha256`. Wall-clock timings live under
    # `informational` and are excluded by declared policy.
    deterministic = {"run": record["run"], "certificate_sha256": record["certificate_sha256"]}
    golden_deterministic = {
        "run": golden["run"], "certificate_sha256": golden["certificate_sha256"]
    }
    if _canonical(golden_deterministic) != _canonical(deterministic):
        print("GOLDEN MISMATCH: the run record differs from the golden artifact",
              file=sys.stderr)
        return 1
    print("demo passed: run record matches the golden artifact "
          f"({len(record['run']['tasks'])} tasks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
