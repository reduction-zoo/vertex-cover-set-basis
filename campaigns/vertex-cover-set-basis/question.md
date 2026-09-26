# Fixed question

```json
{
  "source": "Vertex Cover",
  "target": "Set Basis",
  "category": "Construction open",
  "summary": "A reconstructed rule connects covering to reusable set representations and Boolean data decomposition.",
  "source_definition": "Given a finite simple undirected graph and a nonnegative integer k, return a vertex set of size at most k meeting every edge. Return NO-SOLUTION exactly when no such witness exists. Graphs, families and strings are explicit; numerical parameters use binary encodings.",
  "target_definition": "Given an explicit family C of subsets of a finite universe and K, return at most K basis subsets such that every member of C is the union of some of the basis subsets. A valid output is a witness satisfying these conditions, or NO-SOLUTION exactly when none exists.",
  "required_result": "Construct deterministic polynomial-time maps F and G. F must produce a legal target instance, and G(x,y) must return a valid source output for every valid target output y, including NO-SOLUTION. A complete rule may reconstruct a published construction or give a new one; it must specify every gadget, numerical parameter and decoding step.",
  "acceptance": "Deliver executable instance construction and output recovery, a general proof covering all legal inputs and target outputs, and worst-case polynomial time and encoding-size bounds. Cite the actual proof used, or identify a newly derived argument. Check small positive and negative instances with independent solvers; finite tests alone do not establish correctness.",
  "importance": "A reconstructed rule connects covering to reusable set representations and Boolean data decomposition.",
  "difficulty": "Difficulty is not yet established by a construction attempt. Basis sets can be reused across several input sets, so simple singleton-and-edge constructions need a complete converse argument.",
  "openness": "This is a rule-completion task from the imported catalog. The requested contribution is a complete, reproducible construction, proof and implementation; the existing hardness attribution is not presented as an unsolved complexity classification. The references are leads to check, not a verified solution.",
  "literature_checked": "2026-09-18",
  "coverage": "Import inventory review of the cited sources. Primary proofs have not been independently re-audited; availability of a complete reconstruction elsewhere remains unassessed.",
  "references": [
    {
      "title": "Problem-Reductions: Vertex Cover \u2192 Set Basis",
      "url": "https://github.com/CodingThrust/problem-reductions/issues/383",
      "note": "Upstream task and discussion checked on 2026-09-18. Reported reference: Garey & Johnson, *Computers and Intractability*, SP7, p.222"
    }
  ],
  "solutions": [],
  "equation": ""
}
```
