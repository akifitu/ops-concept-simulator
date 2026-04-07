"""Load scenario data."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


Scenario = Dict[str, Any]


def load_scenarios(data_file: Path | str) -> List[Scenario]:
    """Load concept-of-operations scenarios from JSON."""
    return json.loads(Path(data_file).read_text(encoding="utf-8"))
