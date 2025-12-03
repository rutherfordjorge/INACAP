"""Refresh action button for the clientes listing."""
from __future__ import annotations

from PyQt6.QtWidgets import QPushButton

from app.viewmodels.cliente_viewmodel import ClienteViewModel


class RefreshClientesAction(QPushButton):
    """Button that reloads clientes through the viewmodel."""

    def __init__(self, viewmodel: ClienteViewModel, parent=None) -> None:
        super().__init__("Recargar", parent)
        self.clicked.connect(viewmodel.load_clientes)
