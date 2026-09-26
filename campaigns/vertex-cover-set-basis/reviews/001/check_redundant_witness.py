"""Independent check of recovery from a redundant valid Set Basis witness."""

import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[4]
CANDIDATE = ROOT / "campaigns/vertex-cover-set-basis/work/algorithm.py"


def call(payload, extract=False):
    args = [sys.executable, str(CANDIDATE)] + (["--extract"] if extract else [])
    return json.loads(subprocess.run(args, input=json.dumps(payload), text=True,
                                     capture_output=True, check=True).stdout)


def valid_basis(target, basis):
    if len(basis) > target["K"]:
        return False
    return all(set().union(*(set(b) for b in basis if set(b) <= set(c))) == set(c)
               for c in target["family"])


source = {"n": 10**30, "edges": [[1, 9]], "k": 5}
target = call(source)
assert target["universe"] == 8 and len(target["family"]) == 7
# Cover {1}: both vertex singletons, the other vertex pair, four edge sets.
basis = [[0], [1], [2, 3], [4, 5], [6, 7], [3, 5, 6], [2, 4, 7]]
# Pair plus singleton, a duplicate, empty set and an unusable cross-vertex set.
basis += [[0, 1], [0], [], [0, 2]]
assert valid_basis(target, basis)
answer = call({"source": source, "target_solution": {"basis": basis}}, True)
cover = answer["cover"]
assert len(cover) == len(set(cover)) <= source["k"]
assert all(a in cover or b in cover for a, b in source["edges"])
print("Redundant-witness recovery passed")
