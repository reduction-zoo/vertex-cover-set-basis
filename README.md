# Vertex Cover → Set Basis

Independent research campaign. The completed rule reconstructs a published five-set gadget and recovers a Vertex Cover answer from every valid Set Basis output. An independent follow-up review advanced it for expert review; no new hardness theorem is claimed.

[State](campaigns/vertex-cover-set-basis/state.md) · [Question](campaigns/vertex-cover-set-basis/question.md)

[Paper (PDF)](campaigns/vertex-cover-set-basis/work/manuscript.pdf) · [Typst source](campaigns/vertex-cover-set-basis/work/manuscript.typ) · [Proof](campaigns/vertex-cover-set-basis/work/proof.md) · [Verification](campaigns/vertex-cover-set-basis/work/verification.md) · [Round 001](campaigns/vertex-cover-set-basis/rounds/001/round.md)

Reproduce with `uv sync --locked`, then run `uv run --locked python campaigns/vertex-cover-set-basis/work/check.py --self-test` and `uv run --locked python campaigns/vertex-cover-set-basis/work/check.py --candidate campaigns/vertex-cover-set-basis/work/algorithm.py`. The prepared target oracle requires SCIP 10.1.0 on `PATH`; further commands and checked counts appear in the paper appendix.

Board source commit: 6c7d3bd9c0a8f595279969a9c0a4d1853a3f5c17.
