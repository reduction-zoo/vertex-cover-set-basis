# A complete Vertex Cover → Set Basis rule

This is a reconstruction of the five-set gadget in Björklund and Martens, *The Tractability Frontier for NFA Minimization* (2008), Lemmas 4–5, pp. 6–10, https://people.cs.umu.se/henrikb/papers/icalp08.pdf. Their construction is attributed to Jiang and Ravikumar. The decoder and the direct counting proof below are derived here; the source's normal-basis normalization is not needed. No novelty is claimed for the gadget.

## Construction

Let `A` be the sorted list of vertices incident to an input edge, with `q=|A|`, and relabel these vertices `0,...,q−1`. Isolated vertices are discarded: they never affect vertex-cover feasibility. Let `m=|E|`. The target universe contains `x_i,y_i` for each active vertex and four private elements `a_e,b_e,d_e,e_e` for each edge. For every active vertex, put `c_i={x_i,y_i}` in the target family. For every edge `e={i,j}`, `i<j`, put in the five sets

```
c1={x_i,a_e,b_e}    c2={y_j,b_e,d_e}    c3={y_i,d_e,e_e}
c4={x_j,a_e,e_e}    c5={a_e,b_e,d_e,e_e}.
```

Set the basis budget to `K=q+4m+k`. `algorithm.py` uses integer labels `x_i=2i`, `y_i=2i+1`, and `a_e,...,e_e=2q+4h,...,2q+4h+3` for the edge at input position `h`. These are legal subsets of a universe of size `2q+4m`; the family has `q+5m` members.

## If a cover exists

For each vertex in a cover `T`, take `{x_i}` and `{y_i}`. For each other active vertex, take `{x_i,y_i}`. This costs `q+|T|`. For each edge `e={i,j}` with `i<j`, if `i∈T`, take `{a,b}`, `{d,e}`, `{y_j,b,d}`, `{x_j,a,e}`; otherwise `j∈T`, and take `{a,e}`, `{b,d}`, `{x_i,a,b}`, `{y_i,d,e}`. This costs four sets per edge. In the first case, `c1` and `c3` are unions of the vertex singletons with the first two edge sets; `c2,c4` are basis sets; `c5={a,b}∪{d,e}`. The second case is symmetric: `c2,c4` use `y_j,x_j` and the first two edge sets; `c1,c3` are basis sets; `c5={a,e}∪{b,d}`. Hence the target has a basis of size `q+4m+|T|≤K`.

## Any target basis gives a cover

Let `B` be any valid target basis of size at most `K`. Delete empty and duplicate sets, and sets not contained in any family member, since none can contribute to a union. If `B` contains both `{x_i,y_i}` and `{x_i}`, replace the pair by `{y_i}`; do the symmetric replacement when it contains `{y_i}`. The pair is contained in no family member other than `c_i`, so these changes preserve validity and never increase size. Repeat for each vertex. The resulting basis is normalized: for each vertex it contains either the pair alone or both singletons. Let `T` be the vertices of the second type and `t=|T|`. These vertex-only basis sets number exactly `q+t`; every other useful basis set contains a private edge element and belongs to one edge gadget only.

Fix an edge gadget. At least four edge-local basis sets are needed. Consider the four required element occurrences `(c1,a)`, `(c2,b)`, `(c3,d)`, `(c4,e)`. No one basis set can cover two of them: it would have to be contained in both corresponding family members and contain both designated elements, but for every pair at least one designated element is absent from the other member. The four witnessing basis sets are therefore distinct and edge-local.

If neither endpoint lies in `T`, neither endpoint has a singleton vertex basis set. Each of `c1,c2,c3,c4` needs an edge-local basis set containing its own vertex symbol. These four sets are distinct, since each edge row has only one vertex symbol and the four symbols differ. None is contained in `c5`, which has no vertex symbol. At least one further edge-local basis set is required to represent `c5`. Thus an edge outside `T` needs at least five edge-local sets; every other edge needs at least four.

Let `u` be the number of edges uncovered by `T`. Because edge-local sets cannot be shared between gadgets, `|B|≥q+t+4m+u`. Since `|B|≤q+4m+k`, we have `t+u≤k`. The decoder outputs `T` and one endpoint of each of those `u` edges. It covers every edge and has at most `t+u≤k` vertices. The executable decoder reconstructs the active-vertex labels from the source instance; it uses no state from the forward run. If the valid target answer is `NO-SOLUTION`, the forward direction shows that the source has no cover, so the decoder returns `NO-SOLUTION` too. This proves recovery from every valid target output.

## Bounds and scope

There are at most `2m` active vertices, so the target has `O(m)` universe elements, family members and incidences. Integer labels use `O(log(m+1))` bits; `K=q+4m+k` uses `O(log(k+m+1))` bits. Thus the forward output length and deterministic runtime are polynomial in the explicit edge-list input length, even if the JSON `n` or binary `k` is large. Extraction scans the encoded basis and reconstructed family polynomially in `|x|+|y|`; no optimization or source solving occurs. Its output has at most `2m` vertex labels of `O(log(n+1))` bits. The proof covers empty graphs, oversized `k`, all valid basis witnesses, and the no-solution answer. It asserts neither an optimal basis size beyond the budget equivalence nor practical efficiency of the independent solver.
