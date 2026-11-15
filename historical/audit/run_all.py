# ─────────────────────────────────────────────
# run_all.py — update to show 16 checks
# ─────────────────────────────────────────────
"""Run all session-1 checks and print a summary."""

import subprocess, sys, os
from pathlib import Path

HERE = Path(__file__).parent
CHECKS = sorted(HERE.glob("check*.py"))

results = []
for script in CHECKS:
    print("\n" + "=" * 70)
    print(f"Running {script.name}")
    print("=" * 70)
    r = subprocess.run([sys.executable, str(script)])
    results.append((script.name, r.returncode))

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
for name, code in results:
    print(f"  {name}: {'PASS' if code == 0 else f'FAIL (exit {code})'}")

sys.exit(0 if all(c == 0 for _, c in results) else 1)
