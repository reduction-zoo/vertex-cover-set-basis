"""Regression for explicit edge input with many isolated vertices."""

import unittest

from algorithm import construct


class EncodingSize(unittest.TestCase):
    def test_isolated_vertices_do_not_expand_binary_input(self):
        target = construct({"n": 100, "edges": [[0, 99]], "k": 1})
        self.assertLessEqual(target["universe"], 8)
        self.assertLessEqual(len(target["family"]), 7)


if __name__ == "__main__":
    unittest.main()
