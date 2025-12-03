"""Action button to create a new cliente entry."""
from __future__ import annotations

from PyQt6.QtWidgets import QMessageBox, QPushButton

from app.domain.models.cliente import Cliente
from app.ui.dialogs import ClienteFormDialog
from app.ui.listing.cliente_table_model import ClienteTableModel
from app.viewmodels.cliente_viewmodel import ClienteViewModel


class CreateClienteAction(QPushButton):
    """Button that opens the creation dialog and persists the cliente."""

    def __init__(self, viewmodel: ClienteViewModel, model: ClienteTableModel, parent=None) -> None:
        super().__init__("Nuevo", parent)
        self._viewmodel = viewmodel
        self._model = model
        self.clicked.connect(self._open_dialog)

    def _open_dialog(self) -> None:
        dialog = ClienteFormDialog(self)
        if dialog.exec() != dialog.DialogCode.Accepted:
            return
        data = dialog.get_data()
        cliente = Cliente(
            id=None,
            rut=data["rut"],
            dv=data["dv"],
            nombre=data["nombre"],
            apellido=data["apellido"],
            fecha_nac=data["fecha_nac"],
            email=data["email"],
            telefono=data["telefono"],
            direccion=data["direccion"],
            estado_cliente=data["estado_cliente"],
            limite_credito=data["limite_credito"],
        )
        if self._viewmodel.add_cliente(cliente):
            self._model.clear_selection()
            QMessageBox.information(self, "Clientes", "Cliente creado correctamente")
