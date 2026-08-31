"""
check_effort_reproduction.py — effort-accounting thread

Verifies that the v28 reproduction archive rebuilds the frozen final empirical
outputs on this machine.

Method: copies archive_v28's scripts/, inputs/, and expected/ into a fresh
temporary build directory (the pristine archive tree in the repo is never
written to), runs the archive's own 00_reproduce_all.py and
99_verify_reproduction.py there unmodified, and propagates the verdict.
The five numeric comparisons (C28, DQ, S1, DF19, DF21) are the archive's own;
this wrapper adds nothing to them and hides nothing from them.

Run from the repo root:
    ./venv/Scripts/python.exe effort-accounting/checks/check_effort_reproduction.py
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ARCHIVE = Path(__file__).resolve().parent.parent / "archive_v28"


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="effort_repro_check_"))
    env = dict(os.environ, MPLBACKEND="Agg")
    try:
        for d in ("scripts", "inputs", "expected"):
            shutil.copytree(ARCHIVE / d, tmp / d)
        for step, script in (("BUILD", "00_reproduce_all.py"),
                             ("VERIFY", "99_verify_reproduction.py")):
            r = subprocess.run([sys.executable, str(tmp / "scripts" / script)],
                               capture_output=True, text=True, env=env)
            sys.stdout.write(r.stdout)
            if r.stderr:
                sys.stderr.write(r.stderr)
            if r.returncode != 0:
                print(f"RED — {step} step failed (exit {r.returncode})")
                return 1
        print("GREEN — archive_v28 rebuilds the frozen final outputs on this machine")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
