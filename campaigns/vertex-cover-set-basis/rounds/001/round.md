# Round 001 — published construction search

## Plan

Gap: no verified explicit Vertex Cover → Set Basis construction. Scope: the cited problem-reductions issue, the original Set Basis hardness reference, and primary papers on Boolean matrix factorization/biclique cover. First check: locate an explicit polynomial instance map and decoding argument, or a chain of fully specified reductions. A complete source can be reconstructed and tested in this attempt; absence in this finite search does not establish novelty.

## Evidence and diagnosis

Primary source found: Björklund and Martens, *The Tractability Frontier for NFA Minimization* (2008), Lemmas 4–5, pp. 6–10, https://people.cs.umu.se/henrikb/papers/icalp08.pdf. Lemma 4 gives the five-set gadget, citing Jiang and Ravikumar; Lemma 5 proves equivalence of ordinary and normal Set Basis on its constructed family. The paper's condition `k < |E|−3` serves a downstream automata reduction, not the gadget proof. The original Stockmeyer (1975) five-page report was located bibliographically but not obtained. The project issue https://github.com/CodingThrust/problem-reductions/issues/383 explicitly admits its illustrative construction fails; it supplies no rule.

I reconstructed the gadget in [algorithm.py](../../work/algorithm.py) and derived a direct counting decoder in [proof.md](../../work/proof.md). The first end-to-end run exposed expansion of isolated vertices from binary `n`; a failing regression preceded compression to active vertices. A generic Z3 slot encoding and then closure-set Z3/Kissat encodings were interrupted on hard NO cases; these are execution failures. The prepared oracle now uses SCIP's exact binary model. [Verification](../../work/verification.md) records 112 corpus instances, 113 prepared target outputs including an alternate, and nine separately obtained target outputs. No mismatch remains.

The mechanism is reconstructed, not novel. Its concrete contribution here is an executable search reduction with decoding from arbitrary target witnesses and a direct proof that does not call a normal-basis conversion. Significance is reproducibility and clarification of the upstream issue, not a new hardness classification. Review 001 accepted the mathematical proof but found Python's 4300-digit JSON integer limit. A failing 4301-digit regression was added before the CLI repair; the forward map, extraction, 112-case loop, and separate verifier all pass after disabling that cap. This is a same-strategy repair in round 001.

## Next action

Request focused fresh-context follow-up review of the executable repair, reusing unaffected review evidence. If it advances, write and inspect a Typst manuscript. Experience extraction: none yet; this is a known gadget and the direct counting lemma is fully campaign-specific.
