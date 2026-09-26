"""Exercise the repaired CLI with large vertex labels and a large budget."""

import json
from pathlib import Path
import subprocess
import sys


sys.set_int_max_str_digits(0)
candidate = Path(__file__).resolve().parents[2] / "work/algorithm.py"
large = 10 ** 4300
vertex_bound = 10 ** 4301
source = {"n": vertex_bound, "edges": [[vertex_bound - 2, vertex_bound - 1]],
          "k": large}


def run(payload, *args):
    process = subprocess.run([sys.executable, str(candidate), *args],
                             input=json.dumps(payload), text=True,
                             capture_output=True, check=True)
    return json.loads(process.stdout)


target = run(source)
assert target["universe"] == 8
assert len(target["family"]) == 7
assert target["K"] == large + 6
basis = target["family"]
assert len(basis) <= target["K"]
assert all(set().union(*(set(b) for b in basis if set(b) <= set(c))) == set(c)
           for c in target["family"])
answer = run({"source": source, "target_solution": {"basis": basis}}, "--extract")
assert answer == {"cover": [vertex_bound - 2]}
print("Large-label and large-budget CLI recovery passed")
