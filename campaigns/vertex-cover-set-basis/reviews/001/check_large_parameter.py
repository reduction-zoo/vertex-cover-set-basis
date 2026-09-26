"""Reproduce the default Python JSON integer length boundary."""

from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[4]
CANDIDATE = ROOT / "campaigns/vertex-cover-set-basis/work/algorithm.py"
payload = '{"n":0,"edges":[],"k":' + '1' + '0' * 4300 + '}'
result = subprocess.run([sys.executable, str(CANDIDATE)], input=payload,
                        text=True, capture_output=True)
assert result.returncode != 0
assert "Exceeds the limit" in result.stderr
print(result.stderr.strip())
