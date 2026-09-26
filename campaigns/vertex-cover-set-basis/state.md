# Campaign state

Status: `ready_for_expert_review` (agent assessment, not human certification).
Budget: 20 rounds. Used: 1. Remaining: 19. Discovery stops because the fixed rule is complete; no further construction round is needed.
Board source: 6c7d3bd9c0a8f595279969a9c0a4d1853a3f5c17.

Capability probe (2026-09-26): Python 3.12.14 at `/Users/xiweipan/.local/bin/python3`; uv 0.12.17 at `/Users/xiweipan/.local/bin/uv`; SCIP 10.1.0 at `/opt/homebrew/bin/scip` selected for the prepared target oracle; Z3 executable 5.1.0 at `/opt/homebrew/bin/z3`, Kissat 4.0.4 at `/opt/homebrew/bin/kissat`; locked Python `z3-solver` 4.16.0 used for separate verification; Typst 0.15.1 at `/opt/homebrew/bin/typst`; Lean 4.34.1 and Lake 5.0.0 at `/opt/homebrew/bin/lean` and `/opt/homebrew/bin/lake`. No campaign Mathlib project has been set up; the sci-brain technical-writing skill is available at `/Users/xiweipan/.codex/plugins/cache/sci-brain/sci-brain/0.5.0/skills/how-to-technical-writing/SKILL.md`.
Prepare: completed; [foundation](work/preparation.md), [112 fixed cases](work/cases.json), [contract](work/contract.md).
Current claim: executable F/G reconstruct the published five-set gadget and decode every valid Set Basis output by a direct counting argument; [proof](work/proof.md), [verification](work/verification.md), [manuscript](work/manuscript.pdf). Correctness: independent [review 001](reviews/001/review.md) accepted the proof but found the JSON integer cap; [review 002](reviews/002/review.md) advanced the repaired executable rule. Novelty: known gadget and core endpoint argument; no new hardness theorem claimed. Significance: a reproducible completion of the fixed rule. Prospects for expert acceptance: high (uncalibrated; independent advance review and complete manuscript, with original historical proofs uninspected).
Checks: 112 prepared source cases (80 YES, 32 NO), 113 prepared target outputs; seven separate source cases, nine separate target outputs including alternate bases and NO; 4301-digit parameter regression and independent long-label check. The Typst PDF compiled and all four pages were visually inspected. Formalization was not requested and remains pending; the inaccessible original Stockmeyer and Jiang–Ravikumar proofs remain uninspected.
Experience extraction (2026-09-26): 0 created, 0 updated, 0 pending; see [round 001](rounds/001/round.md). One distinct mechanism: published five-set edge gadget. Next action: expert review. No remote, publication, or board edit was made.

| Round | Mechanism / scope | First check | Outcome | Evidence |
|---|---|---|---|---|
| 001 | Primary five-set gadget literature and reconstruction | Locate explicit F/G argument | Complete; follow-up review advanced; paper inspected | [round](rounds/001/round.md) |
