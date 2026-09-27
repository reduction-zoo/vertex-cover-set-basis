# Research instructions

Read the [fixed question](campaigns/vertex-cover-set-basis/question.md), [prior state](campaigns/vertex-cover-set-basis/state.md) and [preparation notes](campaigns/vertex-cover-set-basis/work/preparation.md). The fixed [test corpus](campaigns/vertex-cover-set-basis/work/cases.json) and [verifier](campaigns/vertex-cover-set-basis/work/check.py) are the starting evidence; the preparation notes state their coverage and any pending checks.

Run `uv sync --locked`, then `uv run --locked python campaigns/vertex-cover-set-basis/work/check.py --self-test` before relying on that evidence. Follow the current user's AutoResearch pipeline. Scope and budgets in the state describe earlier work and do not limit a new campaign. Preserve prior evidence, commit new work incrementally and make only evidence-backed claims.
