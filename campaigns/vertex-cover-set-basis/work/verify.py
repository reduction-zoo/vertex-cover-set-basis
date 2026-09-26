"""Separate small-instance verification using Z3 and direct definitions."""

import argparse
from itertools import combinations
import json
from pathlib import Path
import subprocess
import sys

from z3 import AtMost, Bool, Or, Solver, is_true, sat, unsat


NO = {"no_solution": True}


def source_answer(x):
    active = sorted({v for edge in x["edges"] for v in edge})
    for size in range(min(x["k"], len(active)) + 1):
        for cover in combinations(active, size):
            if all(i in cover or j in cover for i, j in x["edges"]):
                return {"cover": list(cover)}
    return NO


def valid_source(x, y):
    if y == NO:
        return source_answer(x) == NO
    cover = y.get("cover")
    return (isinstance(cover, list) and len(cover) == len(set(cover)) <= x["k"]
            and all(type(v) is int and 0 <= v < x["n"] for v in cover)
            and all(i in cover or j in cover for i, j in x["edges"]))


def valid_basis(x, y):
    basis = y.get("basis")
    if not isinstance(basis, list) or len(basis) > x["K"]:
        return False
    if any(not isinstance(b, list) or any(type(u) is not int or not 0 <= u < x["universe"] for u in b)
           for b in basis):
        return False
    return all(set().union(*(set(b) for b in basis if set(b) <= set(c))) == set(c)
               for c in x["family"])


def target_answers(x):
    rows = [set(c) for c in x["family"]]
    candidates = sorted({tuple(sorted(part)) for row in rows for size in range(1, len(row) + 1)
                         for part in combinations(sorted(row), size)})
    bits = [Bool(f"basis_{i}") for i in range(len(candidates))]
    solver = Solver()
    if bits:
        solver.add(AtMost(*bits, x["K"]))
    for row in rows:
        for u in row:
            solver.add(Or(*[bits[i] for i, part in enumerate(candidates)
                            if u in part and set(part) <= row]))
    outputs = []
    for _ in range(2):
        result = solver.check()
        if result == unsat:
            break
        if result != sat:
            raise RuntimeError(f"Z3 inconclusive: {result}")
        model = solver.model()
        chosen = [is_true(model.eval(bit)) for bit in bits]
        outputs.append({"basis": [list(candidates[i]) for i, flag in enumerate(chosen) if flag]})
        solver.add(Or(*[bit != flag for bit, flag in zip(bits, chosen)]))
    return outputs or [NO]


def invoke(candidate, payload, extract=False):
    cmd = [sys.executable, str(candidate)] + (["--extract"] if extract else [])
    return json.loads(subprocess.run(cmd, input=json.dumps(payload), text=True,
                                     capture_output=True, check=True).stdout)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=Path, required=True)
    args = parser.parse_args()
    cases = [
        {"n": 0, "edges": [], "k": 0},
        {"n": 100, "edges": [[0, 99]], "k": 0},
        {"n": 100, "edges": [[0, 99]], "k": 1},
        {"n": 3, "edges": [[0, 1], [1, 2]], "k": 0},
        {"n": 3, "edges": [[0, 1], [1, 2]], "k": 1},
        {"n": 4, "edges": [[0, 1], [2, 3]], "k": 1},
        {"n": 4, "edges": [[0, 1], [2, 3]], "k": 2},
    ]
    yes = no = alternate = 0
    for x in cases:
        target = invoke(args.candidate.resolve(), x)
        answers = target_answers(target)
        expected = source_answer(x)
        assert (answers[0] == NO) == (expected == NO), (x, answers[0], expected)
        for answer in answers:
            assert answer == NO or valid_basis(target, answer), (x, target, answer)
            recovered = invoke(args.candidate.resolve(), {"source": x, "target_solution": answer}, True)
            assert valid_source(x, recovered), (x, target, answer, recovered)
            if answer == NO:
                no += 1
            else:
                yes += 1
        alternate += len(answers) == 2
    print(f"Verified {len(cases)} instances, {yes} basis outputs, {no} NO outputs, {alternate} alternate witnesses")


if __name__ == "__main__":
    main()
