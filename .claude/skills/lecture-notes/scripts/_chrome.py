"""Headless Chrome, shared by render_preview.py and finalize.py.

Don't pass --user-data-dir: headless Chrome already gives each instance its own throwaway
profile (parallel runs are fine), and an explicit profile makes pages that load network
resources hang on this machine.
"""

import os
import shutil
import signal
import subprocess
import sys

CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "google-chrome",
    "chromium",
]

BASE_FLAGS = ["--headless=new", "--disable-gpu", "--no-first-run", "--allow-file-access-from-files"]


def find_chrome():
    for c in CANDIDATES:
        path = c if os.path.isabs(c) else shutil.which(c)
        if path and os.path.exists(path):
            return path
    sys.exit("Google Chrome not found; it is needed to render previews and convert figures.")


def run_chrome(args, timeout=60):
    """Run headless Chrome with `args`; return stdout. On a hang, kill the whole process
    group (Chrome's helper processes included) and exit with a readable message."""
    proc = subprocess.Popen([find_chrome(), *BASE_FLAGS, *args], stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace",
                            start_new_session=True)
    try:
        out, _ = proc.communicate(timeout=timeout)
        return out
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid, signal.SIGKILL)
        proc.communicate()
        sys.exit(f"Chrome did not finish in {timeout} s (no network for the CDN scripts?). "
                 "Nothing was written; try again.")
