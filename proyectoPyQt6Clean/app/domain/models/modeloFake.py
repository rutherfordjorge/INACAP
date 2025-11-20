"""Domain model for TablaFake entity."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class TablaFake:
    """Placeholder record with two fields for student exercises."""

    id: Optional[int]
    columna: str
