"""Pytest bootstrap: make `igtp_engine` importable from the bridges directory."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
