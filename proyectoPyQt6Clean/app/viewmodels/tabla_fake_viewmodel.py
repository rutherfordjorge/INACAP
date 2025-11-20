"""ViewModel for TablaFake listing."""
from __future__ import annotations

from typing import List, Sequence

from PyQt6.QtCore import QObject, pyqtSignal

from app.domain.models.modeloFake import TablaFake
from app.infrastructure.repositories.tabla_fake_repository import TablaFakeRepository


class TablaFakeViewModel(QObject):
    """Coordinates UI updates for TablaFake data."""

    items_changed = pyqtSignal(list)
    error_occurred = pyqtSignal(str)

    def __init__(self, repository: TablaFakeRepository) -> None:
        super().__init__()
        self._repository = repository
        self._items: List[TablaFake] = []

    def load_items(self) -> None:
        """Placeholder to fetch rows from the repository."""

        pass

    def add_item(self, item: TablaFake) -> bool:
        """Placeholder to persist a new row."""

        pass

    def delete_items(self, item_ids: Sequence[int]) -> bool:
        """Placeholder to delete entries."""

        pass

    @property
    def items(self) -> List[TablaFake]:
        """Return cached rows."""

        return self._items
