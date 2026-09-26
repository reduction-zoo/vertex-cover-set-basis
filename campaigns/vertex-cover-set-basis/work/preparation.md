# Prepare evidence — 2026-09-26

The fixed corpus has 112 distinct legal source instances: 12 hand-designed edge cases and 100 seeded random graphs (seeds 0–138, with duplicates skipped). Vertex counts are 0–6. There are 80 YES and 32 NO instances; 12/17/26/28/27 cases have 2/3/4/5/6 vertices respectively, plus edge cases with 0–3 vertices. `check.py --generate` reproduces the JSON corpus from the recorded seeds.

The source oracle enumerates all vertex subsets in increasing cardinality and validates its returned witness against the edge definition. The target oracle uses the locked `z3-solver` 4.16.0 Python binding. For each of `K` basis slots it chooses universe bits; each family member has use bits. A use bit forces the basis slot to be contained in that member, and every member element must be covered by a used slot. SAT yields a basis witness, UNSAT yields `NO-SOLUTION`; any other status raises an error. Witnesses are checked again with the direct union predicate. The independent hand examples and exhaustive enumeration of all families over a two-element universe check this encoding. This solver is a test oracle, not part of a candidate reduction.

Before implementing the oracle, `uv run --locked python campaigns/vertex-cover-set-basis/work/test_check.py` failed with `ModuleNotFoundError: check`, as expected. After implementation:

```
uv sync --locked
uv run --locked python campaigns/vertex-cover-set-basis/work/test_check.py
uv run --locked python campaigns/vertex-cover-set-basis/work/check.py --generate --self-test
```

The tests passed (3 definition-level tests; 112 corpus cases). The self-test starts with `research/validate_preparation.py`, regenerates every case from its seed, recomputes every source answer, validates witnesses, and rejects deliberately wrong source and target outputs. The corpus is fixed before candidate construction. All verification here is finite; the source oracle is intended for small graphs only. No target instance from a proposed reduction has been tested yet.
