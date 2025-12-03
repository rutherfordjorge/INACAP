"""Main window for the Cliente management UI."""
from __future__ import annotations

from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QToolBar

from app.infrastructure.database.oracle_connection import OracleConnection
from app.infrastructure.repositories.cliente_repository import ClienteRepository
from app.ui.actions.create_cliente_action import CreateClienteAction
from app.ui.actions.delete_clientes_action import DeleteClientesAction
from app.ui.actions.refresh_clientes_action import RefreshClientesAction
from app.ui.dialogs import ClienteDetailDialog
from app.ui.listing.client_list_view import ClientListView
from app.ui.listing.cliente_table_model import ClienteTableModel
from app.viewmodels.cliente_viewmodel import ClienteViewModel


class MainWindow(QMainWindow):
    """Application's main window."""

    def __init__(self, settings_path: Path) -> None:
        super().__init__()
        self.setWindowTitle("Gestión de Clientes")
        self.resize(1100, 550)

        connection = OracleConnection.from_settings(settings_path)
        repository = ClienteRepository(connection)
        self._viewmodel = ClienteViewModel(repository)
        self._model = ClienteTableModel()

        self._setup_ui()
        self._connect_signals()
        self._viewmodel.load_clientes()

    def _setup_ui(self) -> None:
        self._table_view = ClientListView(self._model, self)
        self.setCentralWidget(self._table_view)

        toolbar = QToolBar("Acciones", self)
        toolbar.setMovable(False)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

        refresh_button = RefreshClientesAction(self._viewmodel, self)
        toolbar.addWidget(refresh_button)

        new_button = CreateClienteAction(self._viewmodel, self._model, self)
        toolbar.addWidget(new_button)

        delete_button = DeleteClientesAction(self._viewmodel, self._model, self)
        toolbar.addWidget(delete_button)

        self.statusBar().showMessage("Listo")

    def _connect_signals(self) -> None:
        self._viewmodel.clientes_changed.connect(self._model.update_clientes)
        self._viewmodel.error_occurred.connect(self._show_error)
        self._table_view.detail_delegate.clicked.connect(self._show_detail_for_row)

    def _show_error(self, message: str) -> None:
        QMessageBox.critical(self, "Error", message)

    def _show_detail_for_row(self, row: int) -> None:
        cliente = self._model.cliente_at(row)
        if not cliente:
            return
        dialog = ClienteDetailDialog(cliente, self)
        dialog.exec()
