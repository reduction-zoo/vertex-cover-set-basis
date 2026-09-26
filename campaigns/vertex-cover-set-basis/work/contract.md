# Executable contract

Input to `algorithm.py`: one JSON object `{"n":n,"edges":[[u,v],...],"k":k}` on stdin. Vertices are `0,...,n-1`; edges are distinct unordered pairs with `0 <= u < v < n`; `n,k` are nonnegative integers. The graph is simple. Output is one JSON target object `{"universe":m,"family":[[u,...],...],"K":K}` with nonnegative integer `m,K`, distinct canonical members in each subset, and elements in `0,...,m-1`. Repeated family members are allowed.

Source outputs are `{"cover":[v,...]}` with distinct vertices, at most `k`, meeting every edge, or `{"no_solution":true}` exactly when no cover exists. Target outputs are `{"basis":[[u,...],...]}` with at most `K` subsets whose unions represent each family member, or the same no-solution object exactly when no basis exists. Empty unions represent the empty set.

`python3 algorithm.py` reads one source instance and writes one target instance. `python3 algorithm.py --extract` reads `{"source":x,"target_solution":y}` and writes one source output. Each command uses a fresh process; errors exit nonzero and diagnostics go to stderr. The independent validators in `check.py` define the executable membership tests.
