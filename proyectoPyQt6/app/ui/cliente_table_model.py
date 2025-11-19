"""Qt table model for Cliente data."""
from __future__ import annotations

from typing import List, Sequence

from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt, QVariant

from app.domain.models.cliente import Cliente


class ClienteTableModel(QAbstractTableModel):
    """Model that adapts Cliente objects to a QTableView."""

    HEADERS: Sequence[str] = (
        "ID",
        "RUT",
        "DV",
        "Nombre",
        "Apellido",
        "Fecha Nac.",
        "Email",
        "Teléfono",
        "Dirección",
        "Estado",
        "Límite Crédito",
    )

    def __init__(self, clientes: List[Cliente] | None = None) -> None:
        super().__init__()
        self._clientes: List[Cliente] = clientes or []

    def rowCount(self, parent: QModelIndex | None = None) -> int:  # noqa: N802
        return len(self._clientes)

    def columnCount(self, parent: QModelIndex | None = None) -> int:  # noqa: N802
        return len(self.HEADERS)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> QVariant:  # noqa: N802
        if not index.isValid() or role not in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
            return QVariant()

        cliente = self._clientes[index.row()]
        column = index.column()
        value = {
            0: cliente.id,
            1: cliente.rut,
            2: cliente.dv,
            3: cliente.nombre,
            4: cliente.apellido,
            5: cliente.fecha_nac.isoformat() if cliente.fecha_nac else "",
            6: cliente.email,
            7: cliente.telefono,
            8: cliente.direccion,
            9: cliente.estado_cliente,
            10: cliente.limite_credito,
        }.get(column, "")
        return QVariant(str(value) if value is not None else "")

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole) -> QVariant:  # noqa: N802
        if role != Qt.ItemDataRole.DisplayRole:
            return QVariant()
        if orientation == Qt.Orientation.Horizontal:
            return QVariant(self.HEADERS[section])
        return QVariant(str(section + 1))

    def update_clientes(self, clientes: List[Cliente]) -> None:
        """Replace the internal list and notify views."""

        self.beginResetModel()
        self._clientes = clientes
        self.endResetModel()

