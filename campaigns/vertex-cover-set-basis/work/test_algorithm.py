"""Regression for explicit edge input with many isolated vertices."""

import unittest
import json
from pathlib import Path
import subprocess
import sys

from algorithm import construct


class EncodingSize(unittest.TestCase):
    def test_isolated_vertices_do_not_expand_binary_input(self):
        target = construct({"n": 100, "edges": [[0, 99]], "k": 1})
        self.assertLessEqual(target["universe"], 8)
        self.assertLessEqual(len(target["family"]), 7)

    def test_large_parameter_survives_both_cli_modes(self):
        sys.set_int_max_str_digits(0)
        source = '{"n":0,"edges":[],"k":' + '1' + '0' * 4300 + '}'
        candidate = Path(__file__).with_name("algorithm.py")
        forward = subprocess.run([sys.executable, str(candidate)], input=source,
                                 text=True, capture_output=True)
        self.assertEqual(forward.returncode, 0, forward.stderr)
        target = json.loads(forward.stdout)
        self.assertEqual(target["family"], [])
        self.assertEqual(target["K"], 10 ** 4300)
        request = '{"source":' + source + ',"target_solution":{"basis":[]}}'
        backward = subprocess.run([sys.executable, str(candidate), "--extract"],
                                  input=request, text=True, capture_output=True)
        self.assertEqual(backward.returncode, 0, backward.stderr)
        self.assertEqual(json.loads(backward.stdout), {"cover": []})


if __name__ == "__main__":
    unittest.main()
