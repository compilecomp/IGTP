"""Tests for the Lean certificate emitter: determinism and structural policy."""

from igtp_engine.lean_bridge import LeanTask, emit_lean_certificate

TASKS = [
    LeanTask(
        name="igtp_demo_logic_1",
        prop_vars=["P", "Q", "R"],
        hypotheses=["(P → Q)", "(Q → R)", "P"],
        conclusion="R",
    ),
    LeanTask(
        name="igtp_demo_logic_2",
        prop_vars=["P", "Q"],
        hypotheses=["(P ∨ Q)", "¬ P"],
        conclusion="Q",
    ),
    LeanTask(
        name="igtp_demo_logic_3",
        prop_vars=["P"],
        hypotheses=[],
        conclusion="(P ∨ ¬ P)",
    ),
]


def test_output_is_deterministic() -> None:
    assert emit_lean_certificate(TASKS) == emit_lean_certificate(TASKS)
    assert emit_lean_certificate(list(reversed(TASKS))) == emit_lean_certificate(TASKS)


def test_output_contains_sorted_theorems() -> None:
    text = emit_lean_certificate(TASKS)
    names = [line.split()[1] for line in text.splitlines() if line.startswith("theorem")]
    assert names == sorted(names) == [
        "igtp_demo_logic_1",
        "igtp_demo_logic_2",
        "igtp_demo_logic_3",
    ]


def test_every_theorem_uses_tauto() -> None:
    text = emit_lean_certificate(TASKS)
    for block in text.split("theorem ")[1:]:
        assert ":= by\n  tauto" in block


def test_header_present_and_no_sorry() -> None:
    text = emit_lean_certificate(TASKS)
    assert text.startswith("/-")
    assert "DO NOT EDIT" in text
    assert "sorry" not in text
    assert "admit" not in text


def test_hypothesis_binders_in_order() -> None:
    text = emit_lean_certificate(TASKS)
    assert "(h1 : (P → Q)) (h2 : (Q → R)) (h3 : P)" in text
