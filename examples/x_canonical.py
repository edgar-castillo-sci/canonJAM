"""
x_canonical.py

Run x.jam with the canonical method activated.

This script monkey-patches disc_equivalents in xjam2 to use
filter_duplicates from canonJAM. It then executes x.jam
as if nothing had changed.

Requirements:
  - xjam2 must be importable (installed or in PYTHONPATH)
  - A valid JAM.inp must exist in the current directory

xjam2 is NOT a dependency of canonJAM. This file is an optional
integration example for users who already have xjam2 installed.
If xjam2 is missing, the script exits with a clear message.

Usage:
    python3 x_canonical.py
"""

import os
import sys

# 1. Import xjam2 (optional, with a clear error if missing)
try:
    import xjam.libjamstd as std
    import xjam.libjamtdm as tdm
except ImportError:
    print(
        "x_canonical.py requires xjam2 to be installed.\n"
        "canonJAM itself does NOT depend on xjam2; this file is only\n"
        "an optional integration example for users who already have it.\n\n"
        "To install xjam2, see examples/README.md, or:\n"
        "  pip install git+https://github.com/Theochem-merida/xjam2.git\n"
        "  (or export PYTHONPATH=/path/to/xjam2:$PYTHONPATH)"
    )
    sys.exit(1)

# 2. Import the canonical filter
from canonjam import filter_duplicates


# 3. Define the replacement
def disc_equivalents_canonical(stackinglist, optionx, eqnum=None):
    """
    Drop-in replacement for disc_equivalents.

    The canonical method does both passes (eqnum=1 and eqnum=2)
    in a single call, so eqnum is ignored.
    """
    return filter_duplicates(stackinglist, optionx)


# 4. Apply the monkey patch
std.disc_equivalents = disc_equivalents_canonical
tdm.disc_equivalents = disc_equivalents_canonical

print("Canonical method activated for xjam2.")
print()

# 5. Execute x.jam from the current working directory
xjam_script = os.path.join(os.getcwd(), "x.jam")
if not os.path.isfile(xjam_script):
    print(f"Error: no x.jam found in {os.getcwd()}")
    sys.exit(1)

exec(open(xjam_script).read())
