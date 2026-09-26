"""Definition-level examples fixed before any reduction is built."""

import unittest
from itertools import combinations

from check import solve_source, solve_target, valid_source, valid_target


class OracleExamples(unittest.TestCase):
    def test_vertex_cover_yes_and_no(self):
        graph = {"n": 3, "edges": [[0, 1], [1, 2]], "k": 1}
        self.assertEqual(solve_source(graph), {"cover": [1]})
        self.assertTrue(valid_source(graph, {"cover": [1]}))
        self.assertFalse(valid_source(graph, {"cover": [0]}))
        graph["k"] = 0
        self.assertEqual(solve_source(graph), {"no_solution": True})

    def test_set_basis_yes_no_and_empty(self):
        instance = {"universe": 2, "family": [[0], [1], [0, 1]], "K": 2}
        answer = solve_target(instance)
        self.assertTrue(valid_target(instance, answer))
        self.assertFalse(valid_target(instance, {"basis": [[0, 1]]}))
        instance["K"] = 1
        self.assertEqual(solve_target(instance), {"no_solution": True})
        self.assertEqual(solve_target({"universe": 0, "family": [[]], "K": 0}), {"basis": []})

    def test_target_solver_against_enumeration(self):
        possible_sets = [[], [0], [1], [0, 1]]
        for family_size in range(4):
            for family in combinations(possible_sets, family_size):
                for limit in range(3):
                    instance = {"universe": 2, "family": list(family), "K": limit}
                    expected = any(valid_target(instance, {"basis": list(basis)})
                                   for size in range(limit + 1)
                                   for basis in combinations(possible_sets, size))
                    self.assertEqual(solve_target(instance) != {"no_solution": True}, expected)

    def test_alternate_basis_witness(self):
        instance = {"universe": 3, "family": [[0, 1], [1, 2], [0, 2]], "K": 3}
        first = solve_target(instance)
        second = solve_target(instance, exclude=first)
        self.assertNotEqual(first, second)
        self.assertTrue(valid_target(instance, second))


if __name__ == "__main__":
    unittest.main()
