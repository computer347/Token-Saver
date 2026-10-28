import sys
from pathlib import Path

# hidden tests live in <work>/_hidden; make the package importable
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
