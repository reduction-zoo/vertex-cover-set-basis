"""Independent finite oracles and injected-case runner for the fixed problems."""

import argparse
from itertools import combinations
import json
from pathlib import Path
import random
import subprocess
import sys
import tempfile

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
    family, count = x["family"], x["K"]
    members = [frozenset(member) for member in family]
    subsets = {frozenset(part) for member in family for size in range(1, len(member) + 1)
               for part in combinations(member, size)}
    candidates = sorted({tuple(sorted(frozenset.intersection(*(member for member in members if part <= member))))
                         for part in subsets})
    constraints = []
    for member in family:
        elements = set(member)
        for u in elements:
            constraints.append([j for j, candidate in enumerate(candidates)
                                if u in candidate and set(candidate) <= elements])
    return candidates, constraints, count


def solve_target(x, exclude=None):
    candidates, constraints, count = target_solver(x)
    if any(not clause for clause in constraints):
        return NO
    if not candidates:
        return None if exclude is not None else {"basis": []}
    variables = [f"x{j}" for j in range(len(candidates))]
    lp = "Minimize\n obj: 0\nSubject To\n"
    lp += "".join(f" cover{j}: {' + '.join(variables[i] for i in clause)} >= 1\n"
                  for j, clause in enumerate(constraints))
    lp += f" budget: {' + '.join(variables)} <= {count}\nBinary\n {' '.join(variables)}\nEnd\n"
    if exclude is not None:
        selected = {tuple(b) for b in exclude["basis"]}
        signs = [f"- {variables[j]}" if candidate in selected else f"+ {variables[j]}"
                 for j, candidate in enumerate(candidates)]
        lp = lp.replace("Binary\n", f" alternate: {' '.join(signs)} >= {1 - len(selected)}\nBinary\n")
    with tempfile.TemporaryDirectory() as directory:
        model_path = Path(directory) / "basis.lp"
        solution_path = Path(directory) / "basis.sol"
        model_path.write_text(lp)
        result = subprocess.run(["scip", "-q", "-c", f"read {model_path}", "-c", "optimize",
                                 "-c", f"write solution {solution_path}", "-c", "quit"],
                                text=True, capture_output=True)
        if result.returncode:
            raise RuntimeError(f"SCIP failed: {result.stderr}")
        lines = solution_path.read_text().splitlines()
    if lines[0] == "solution status: infeasible":
        return None if exclude is not None else NO
    if lines[0] != "solution status: optimal solution found":
        raise RuntimeError(f"Target oracle inconclusive: {lines[0]}: {result.stdout} {result.stderr}")
    positive = {line.split()[0] for line in lines[2:] if line.split()[1] == "1"}
    return {"basis": [list(candidate) for j, candidate in enumerate(candidates) if f"x{j}" in positive]}


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
    alternate_attempts = alternate_outputs = 0
    for index, case in enumerate(cases, 1):
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
        if answer != NO and len(x["edges"]) <= 2 and alternate_attempts < 5:
            alternate_attempts += 1
            other = solve_target(target, exclude=answer)
            if other is not None:
                assert other != answer and valid_target(target, other)
                recovered = json.loads(subprocess.run([sys.executable, str(path), "--extract"],
                                      input=json.dumps({"source": x, "target_solution": other}), text=True,
                                      capture_output=True, check=True).stdout)
                assert valid_source(x, recovered), (x, target, other, recovered)
                alternate_outputs += 1
        if index % 10 == 0:
            print(f"Checked {index}/{len(cases)}", file=sys.stderr, flush=True)
    print(f"Candidate passed: {len(cases)} source instances, {outputs} primary outputs, {alternate_outputs} alternate outputs")


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
