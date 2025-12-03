"""Action button to delete selected clientes."""
from __future__ import annotations

from PyQt6.QtWidgets import QMessageBox, QPushButton

from app.ui.listing.cliente_table_model import ClienteTableModel
from app.viewmodels.cliente_viewmodel import ClienteViewModel


class DeleteClientesAction(QPushButton):
    """Button that deletes selected clientes after confirmation."""

    def __init__(self, viewmodel: ClienteViewModel, model: ClienteTableModel, parent=None) -> None:
        super().__init__("Eliminar", parent)
        self._viewmodel = viewmodel
        self._model = model
        self.clicked.connect(self._handle_delete)

    def _handle_delete(self) -> None:
        selected_ids = self._model.get_selected_ids()
        if not selected_ids:
            QMessageBox.information(self, "Eliminar", "Debe seleccionar al menos un cliente.")
            return

        confirm = QMessageBox.question(
            self,
            "Eliminar clientes",
            f"¿Eliminar {len(selected_ids)} cliente(s) seleccionados?",
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return

        if self._viewmodel.delete_clientes(selected_ids):
            self._model.clear_selection()
            QMessageBox.information(self, "Clientes", "Clientes eliminados")
