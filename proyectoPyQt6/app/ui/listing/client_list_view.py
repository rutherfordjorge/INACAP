"""Composable table view for clientes listing."""
from __future__ import annotations

from PyQt6.QtWidgets import QAbstractItemView, QTableView

from app.ui.listing.cliente_table_model import ClienteTableModel
from app.ui.listing.delegates import DetailButtonDelegate


class ClientListView(QTableView):
    """Preconfigured table to list clientes with action delegate."""

    def __init__(self, model: ClienteTableModel, parent=None) -> None:
        super().__init__(parent)
        self.setModel(model)
        self.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.setEditTriggers(QAbstractItemView.EditTrigger.AllEditTriggers)
        self.setAlternatingRowColors(True)
        self.horizontalHeader().setStretchLastSection(True)
        self._delegate = DetailButtonDelegate(self)
        self.setItemDelegateForColumn(ClienteTableModel.ACTION_COLUMN, self._delegate)

    @property
    def detail_delegate(self) -> DetailButtonDelegate:
        """Expose the detail delegate so callers can subscribe to clicks."""

        return self._delegate
