"""Qt table model for TablaFake data."""
from __future__ import annotations

from typing import List, Sequence, Set

from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt, QVariant

from app.domain.models.modeloFake import TablaFake


class TablaFakeTableModel(QAbstractTableModel):
    """Model that adapts TablaFake objects to a QTableView."""

    HEADERS: Sequence[str] = ("Seleccionar", "ID", "Columna")
    SELECT_COLUMN = 0

    def __init__(self, filas: List[TablaFake] | None = None) -> None:
        super().__init__()
        self._filas: List[TablaFake] = filas or []
        self._selected_ids: Set[int] = set()

    def rowCount(self, parent: QModelIndex | None = None) -> int:  # noqa: N802
        return len(self._filas)

    def columnCount(self, parent: QModelIndex | None = None) -> int:  # noqa: N802
        return len(self.HEADERS)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> QVariant:  # noqa: N802
        if not index.isValid():
            return QVariant()

        fila = self._filas[index.row()]
        column = index.column()

        if column == self.SELECT_COLUMN and role == Qt.ItemDataRole.CheckStateRole:
            if fila.id is None:
                return QVariant(Qt.CheckState.Unchecked)
            return QVariant(Qt.CheckState.Checked if fila.id in self._selected_ids else Qt.CheckState.Unchecked)

        if role not in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
            return QVariant()

        values = {
            1: fila.id,
            2: fila.columna,
        }
        value = values.get(column, "")
        return QVariant("" if value is None else value)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole) -> QVariant:  # noqa: N802
        if role != Qt.ItemDataRole.DisplayRole:
            return QVariant()
        if orientation == Qt.Orientation.Horizontal:
            return QVariant(self.HEADERS[section])
        return QVariant(str(section + 1))

    def flags(self, index: QModelIndex) -> Qt.ItemFlag:  # noqa: N802
        base_flags = super().flags(index)
        if not index.isValid():
            return base_flags

        if index.column() == self.SELECT_COLUMN:
            return (
                Qt.ItemFlag.ItemIsEnabled
                | Qt.ItemFlag.ItemIsEditable
                | Qt.ItemFlag.ItemIsUserCheckable
                | Qt.ItemFlag.ItemIsSelectable
            )
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable

    def setData(self, index: QModelIndex, value: QVariant, role: int = Qt.ItemDataRole.EditRole) -> bool:  # noqa: N802
        if not index.isValid() or index.column() != self.SELECT_COLUMN:
            return False
        if role not in (Qt.ItemDataRole.CheckStateRole, Qt.ItemDataRole.EditRole):
            return False

        fila = self._filas[index.row()]
        if fila.id is None:
            return False

        state = Qt.CheckState(value)
        if state == Qt.CheckState.Checked:
            self._selected_ids.add(fila.id)
        else:
            self._selected_ids.discard(fila.id)

        self.dataChanged.emit(index, index, [Qt.ItemDataRole.CheckStateRole])
        return True

    def update_filas(self, filas: List[TablaFake]) -> None:
        """Replace the internal list and notify views."""

        self.beginResetModel()
        self._filas = filas
        current_ids = {fila.id for fila in filas if fila.id is not None}
        self._selected_ids.intersection_update(current_ids)
        self.endResetModel()

    def get_selected_ids(self) -> List[int]:
        """Return selected IDs."""

        return list(self._selected_ids)

    def clear_selection(self) -> None:
        """Clear any checkbox selections."""

        if not self._selected_ids:
            return
        self._selected_ids.clear()
        if self.rowCount() == 0:
            return
        top_left = self.index(0, self.SELECT_COLUMN)
        bottom_right = self.index(self.rowCount() - 1, self.SELECT_COLUMN)
        self.dataChanged.emit(top_left, bottom_right, [Qt.ItemDataRole.CheckStateRole])

    def fila_at(self, row: int) -> TablaFake | None:
        """Return TablaFake for the provided row."""

        if 0 <= row < len(self._filas):
            return self._filas[row]
        return None
