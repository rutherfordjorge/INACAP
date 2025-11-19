"""Main window for the Cliente management UI."""
from __future__ import annotations

from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QPushButton, QTableView, QToolBar

from app.infrastructure.database.oracle_connection import OracleConnection
from app.infrastructure.repositories.cliente_repository import ClienteRepository
from app.ui.cliente_table_model import ClienteTableModel
from app.viewmodels.cliente_viewmodel import ClienteViewModel


class MainWindow(QMainWindow):
    """Application's main window."""

    def __init__(self, settings_path: Path) -> None:
        super().__init__()
        self.setWindowTitle("Gestión de Clientes")
        self.resize(1000, 500)

        connection = OracleConnection.from_settings(settings_path)
        repository = ClienteRepository(connection)
        self._viewmodel = ClienteViewModel(repository)
        self._model = ClienteTableModel()

        self._setup_ui()
        self._connect_signals()
        self._viewmodel.load_clientes()

    def _setup_ui(self) -> None:
        table = QTableView(self)
        table.setModel(self._model)
        table.horizontalHeader().setStretchLastSection(True)
        table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        table.setAlternatingRowColors(True)
        self.setCentralWidget(table)

        toolbar = QToolBar("Acciones", self)
        toolbar.setMovable(False)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

        refresh_button = QPushButton("Recargar", self)
        refresh_button.clicked.connect(self._viewmodel.load_clientes)
        toolbar.addWidget(refresh_button)

        self.statusBar().showMessage("Listo")

    def _connect_signals(self) -> None:
        self._viewmodel.clientes_changed.connect(self._model.update_clientes)
        self._viewmodel.error_occurred.connect(self._show_error)

    def _show_error(self, message: str) -> None:
        QMessageBox.critical(self, "Error", message)

