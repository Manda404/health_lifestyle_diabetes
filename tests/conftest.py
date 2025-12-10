import sys
from pathlib import Path

# Ensure the project src directory is on the path for tests
ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = ROOT / "src"
if SRC_PATH.exists():
    sys.path.insert(0, str(SRC_PATH))
