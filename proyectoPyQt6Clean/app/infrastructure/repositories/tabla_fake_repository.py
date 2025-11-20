"""Repository layer for TablaFake entity."""
from __future__ import annotations

from typing import Iterable, List, Optional, Sequence

from app.domain.models.modeloFake import TablaFake
from app.infrastructure.database.oracle_connection import OracleConnection


class TablaFakeRepository:
    """CRUD stub for TablaFake; students should implement DB logic."""

    def __init__(self, connection_factory: OracleConnection) -> None:
        self._connection_factory = connection_factory

    def get_all(self) -> List[TablaFake]:
        """Return every row of TablaFake."""

        pass

    def get_by_id(self, tabla_id: int) -> Optional[TablaFake]:
        """Return a single row by ID."""

        pass

    def add(self, fila: TablaFake) -> int:
        """Insert a new row and return the generated ID."""

        pass

    def update(self, fila: TablaFake) -> None:
        """Update an existing row."""

        pass

    def delete(self, tabla_id: int) -> None:
        """Delete a single row by ID."""

        pass

    def delete_many(self, tabla_ids: Iterable[int]) -> None:
        """Delete multiple rows."""

        pass
