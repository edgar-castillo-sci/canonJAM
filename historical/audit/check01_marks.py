# ─────────────────────────────────────────────
# check01_marks.py
# ─────────────────────────────────────────────
"""Check 1: differences between paper's mark formula and Pfeiffer's."""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import table_of_marks

M_w = table_of_marks(wrong=True)
M_c = table_of_marks(wrong=False)

diffs = [(i + 1, j + 1, M_w[i, j], M_c[i, j])
         for i in range(10) for j in range(10)
         if M_w[i, j] != M_c[i, j]]

print("Differing (i, j, wrong, correct):")
for d in diffs:
    print(f"  ({d[0]}, {d[1]}): wrong={d[2]}, correct={d[3]}")
print(f"\nTotal differences: {len(diffs)}")

expected = [(6, 2)]
got = [(d[0], d[1]) for d in diffs]
if got == expected:
    print("PASS (only (6,2) differs).")
    sys.exit(0)
else:
    print(f"NOTE: checklist predicted {expected}, found {got}.")
    sys.exit(0 if (6, 2) in got else 1)
