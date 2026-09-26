"""Vertex Cover to Set Basis via the five-set edge gadget."""

import json
import sys


NO = {"no_solution": True}


def construct(source):
    n, edges, k = source["n"], source["edges"], source["k"]
    if type(n) is not int or type(k) is not int or min(n, k) < 0:
        raise ValueError("n and k must be nonnegative integers")
    if any(len(edge) != 2 or any(type(v) is not int for v in edge)
           or not 0 <= edge[0] < edge[1] < n for edge in edges):
        raise ValueError("edges must be canonical simple-graph pairs")
    if len({tuple(edge) for edge in edges}) != len(edges):
        raise ValueError("duplicate edge")
    active = sorted({v for edge in edges for v in edge})
    index = {v: i for i, v in enumerate(active)}
    q = len(active)
    family = [[2 * i, 2 * i + 1] for i in range(q)]
    for h, (i, j) in enumerate(edges):
        i, j = index[i], index[j]
        a, b, d, e = range(2 * q + 4 * h, 2 * q + 4 * h + 4)
        family.extend(([2 * i, a, b], [2 * j + 1, b, d], [2 * i + 1, d, e],
                       [2 * j, a, e], [a, b, d, e]))
    return {"universe": 2 * q + 4 * len(edges), "family": family,
            "K": q + 4 * len(edges) + k}


def extract(source, target_solution):
    if target_solution == NO:
        return NO
    target = construct(source)
    raw = target_solution["basis"]
    if len(raw) > target["K"]:
        raise ValueError("too many basis sets")
    family = [set(c) for c in target["family"]]
    universe = target["universe"]
    if any(any(type(u) is not int or not 0 <= u < universe for u in b) for b in raw):
        raise ValueError("basis element outside the universe")
    basis = {frozenset(b) for b in raw if b}
    if any(set().union(*(b for b in basis if b <= c)) != c for c in family):
        raise ValueError("invalid target witness")
    basis = {b for b in basis if any(b <= c for c in family)}
    active = sorted({v for edge in source["edges"] for v in edge})
    split = set()
    for i in range(len(active)):
        x, y = frozenset([2 * i]), frozenset([2 * i + 1])
        pair = x | y
        if pair in basis and x in basis:
            basis.remove(pair)
            basis.add(y)
        elif pair in basis and y in basis:
            basis.remove(pair)
            basis.add(x)
        if x in basis and y in basis:
            split.add(active[i])
    cover = set(split)
    for i, j in source["edges"]:
        if i not in cover and j not in cover:
            cover.add(i)
    if len(cover) > source["k"]:
        raise AssertionError("gadget count violated")
    return {"cover": sorted(cover)}


if __name__ == "__main__":
    try:
        payload = json.load(sys.stdin)
        result = extract(payload["source"], payload["target_solution"]) if sys.argv[1:] == ["--extract"] else construct(payload)
        print(json.dumps(result))
    except (KeyError, TypeError, ValueError, AssertionError) as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)
