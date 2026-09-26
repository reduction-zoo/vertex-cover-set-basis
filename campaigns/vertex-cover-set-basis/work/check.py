"""Independent finite oracles and injected-case runner for the fixed problems."""

import argparse
from itertools import combinations
import json
from pathlib import Path
import random
import subprocess
import sys

from z3 import And, Bool, Or, Solver, is_true, sat, unsat


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
NO = {"no_solution": True}


def valid_source(x, answer):
    if answer == NO:
        return solve_source(x) == NO
    if not isinstance(answer, dict) or set(answer) != {"cover"}:
        return False
    cover = answer["cover"]
    return (isinstance(cover, list) and all(type(v) is int and 0 <= v < x["n"] for v in cover)
            and len(cover) == len(set(cover)) and len(cover) <= x["k"]
            and all(a in cover or b in cover for a, b in x["edges"]))


def solve_source(x):
    for size in range(min(x["k"], x["n"]) + 1):
        for vertices in combinations(range(x["n"]), size):
            if all(a in vertices or b in vertices for a, b in x["edges"]):
                return {"cover": list(vertices)}
    return NO


def target_solver(x):
    universe, family, count = x["universe"], x["family"], x["K"]
    solver = Solver()
    basis = [[Bool(f"b_{j}_{u}") for u in range(universe)] for j in range(count)]
    use = [[Bool(f"use_{i}_{j}") for j in range(count)] for i in range(len(family))]
    for i, member in enumerate(family):
        elements = set(member)
        for j in range(count):
            for u in range(universe):
                if u not in elements:
                    solver.add(Or(~use[i][j], ~basis[j][u]))
        for u in elements:
            solver.add(Or(*[And(use[i][j], basis[j][u]) for j in range(count)]))
    return solver, basis, use


def solve_target(x):
    solver, basis, _ = target_solver(x)
    result = solver.check()
    if result == unsat:
        return NO
    if result != sat:
        raise RuntimeError(f"Target oracle inconclusive: {result}")
    model = solver.model()
    sets = [[u for u, bit in enumerate(row) if is_true(model.eval(bit))] for row in basis]
    return {"basis": [members for members in sets if members]}


def valid_target(x, answer):
    if answer == NO:
        return solve_target(x) == NO
    if not isinstance(answer, dict) or set(answer) != {"basis"}:
        return False
    basis = answer["basis"]
    if not isinstance(basis, list) or len(basis) > x["K"]:
        return False
    if any(not isinstance(s, list) or len(s) != len(set(map(str, s)))
           or any(type(u) is not int or not 0 <= u < x["universe"] for u in s) for s in basis):
        return False
    return all(set().union(*(set(s) for s in basis if set(s) <= set(member))) == set(member)
               for member in x["family"])


def random_source(seed):
    rng = random.Random(seed)
    n = 2 + seed % 5
    edges = [[a, b] for a in range(n) for b in range(a + 1, n) if rng.random() < 0.35 + 0.1 * (seed % 3)]
    return {"n": n, "edges": edges, "k": rng.randrange(n + 1)}


def make_cases():
    examples = [
        (0, [], 0), (1, [], 0), (1, [], 1), (2, [], 0),
        (2, [[0, 1]], 0), (2, [[0, 1]], 1), (2, [[0, 1]], 2),
        (3, [[0, 1], [1, 2]], 0), (3, [[0, 1], [1, 2]], 1),
        (3, [[0, 1], [1, 2]], 2), (3, [[0, 1], [0, 2], [1, 2]], 1),
        (3, [[0, 1], [0, 2], [1, 2]], 2),
    ]
    cases = []
    seen = set()
    for n, edges, k in examples:
        x = {"n": n, "edges": edges, "k": k}
        cases.append({"source": x, "kind": "edge", "expected": solve_source(x)})
        seen.add(json.dumps(x, sort_keys=True))
    for seed in range(1000):
        x = random_source(seed)
        key = json.dumps(x, sort_keys=True)
        if key in seen:
            continue
        cases.append({"source": x, "kind": "random", "seed": seed, "expected": solve_source(x)})
        seen.add(key)
        if len(cases) >= 112:
            break
    assert len(cases) == 112
    return cases


def self_test():
    subprocess.run([sys.executable, str(ROOT / "research/validate_preparation.py"), str(HERE / "cases.json")], check=True)
    cases = json.loads((HERE / "cases.json").read_text())
    assert cases == make_cases(), "Corpus or seeds differ from fixed generator"
    for case in cases:
        x = case["source"]
        assert case["expected"] == solve_source(x)
        assert valid_source(x, case["expected"])
    assert not valid_source({"n": 2, "edges": [[0, 1]], "k": 1}, {"cover": []})
    assert not valid_source({"n": 2, "edges": [[0, 1]], "k": 1}, NO)
    assert not valid_target({"universe": 2, "family": [[0], [1]], "K": 2}, {"basis": [[0, 1]]})
    assert not valid_target({"universe": 1, "family": [[0]], "K": 1}, NO)
    print(f"Self-test passed: {len(cases)} cases")


def run_candidate(path):
    cases = json.loads((HERE / "cases.json").read_text())
    outputs = 0
    for case in cases:
        x = case["source"]
        target = json.loads(subprocess.run([sys.executable, str(path)], input=json.dumps(x), text=True,
                                           capture_output=True, check=True).stdout)
        answer = solve_target(target)
        assert valid_target(target, answer)
        recovered = json.loads(subprocess.run([sys.executable, str(path), "--extract"],
                              input=json.dumps({"source": x, "target_solution": answer}), text=True,
                              capture_output=True, check=True).stdout)
        assert valid_source(x, recovered), (x, target, answer, recovered)
        outputs += 1
    print(f"Candidate passed: {len(cases)} source instances, {outputs} target outputs")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--generate", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--candidate", type=Path)
    args = parser.parse_args()
    if args.generate:
        (HERE / "cases.json").write_text(json.dumps(make_cases(), indent=2) + "\n")
    if args.self_test:
        self_test()
    if args.candidate:
        run_candidate(args.candidate.resolve())
