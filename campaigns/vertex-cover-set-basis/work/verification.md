# Independent finite verification — 2026-09-26

Candidate: `algorithm.py` and `proof.md` in this directory, reconstructed from the five-set gadget cited in the proof. The prepared checker invokes both command modes as separate subprocesses, obtains target outputs from the independent SCIP 10.1.0 feasibility oracle, validates them by direct unions, and checks recovered covers against the source definition and exhaustive source ground truth. The separate `verify.py` does not import either the candidate or `check.py`; it enumerates all nonempty subsets of small target family members, solves its own Boolean model with locked Z3 4.16.0, and checks both outputs directly.

Commands from the repository root:

```
uv sync --locked
uv run --locked python campaigns/vertex-cover-set-basis/work/test_check.py
uv run --locked python campaigns/vertex-cover-set-basis/work/test_algorithm.py
uv run --locked python campaigns/vertex-cover-set-basis/work/check.py --self-test
uv run --locked python campaigns/vertex-cover-set-basis/work/check.py --candidate campaigns/vertex-cover-set-basis/work/algorithm.py
uv run --locked python campaigns/vertex-cover-set-basis/work/verify.py --candidate campaigns/vertex-cover-set-basis/work/algorithm.py
```

Results: the prepared corpus passed with 112 distinct source cases (80 YES, 32 NO), 112 primary valid target outputs and one alternate basis output; every extracted answer was valid. The separate verifier passed seven further cases, including empty input, a graph with 100 labeled vertices but one edge, one-edge YES/NO, a two-edge path YES/NO, and disjoint edges YES/NO. It solved nine target outputs: six basis witnesses, three `NO-SOLUTION`, with two instances having alternate basis witnesses. This exercises edge-gadget composition and both recovery branches. All target answers came from solvers, not the candidate.

Limits: the largest prepared graph has six vertices; the separate verifier has at most two edges. Finite tests cannot establish the universal counting lemma or literature novelty. The proof gives the general argument. The earlier generic Z3 and Kissat oracle runs were interrupted during difficult NO cases and count as execution failures only. SCIP completed the full prepared corpus. No solver or subprocess timeouts were used.
