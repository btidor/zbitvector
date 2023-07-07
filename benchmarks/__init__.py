import os
import sys
from pathlib import Path

if os.getenv("ZBITVECTOR_PROD") is None:
    sys.path.insert(0, str(Path(__file__).parent.parent))
