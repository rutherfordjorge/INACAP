"""Main window for the TablaFake management UI."""
from __future__ import annotations

from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableView,
    QToolBar,
)

from app.domain.models.modeloFake import TablaFake
from app.infrastructure.database.oracle_connection import OracleConnection
from app.infrastructure.repositories.tabla_fake_repository import TablaFakeRepository
from app.ui.dialogs import TablaFakeDetailDialog, TablaFakeFormDialog
from app.ui.tabla_fake_table_model import TablaFakeTableModel
from app.viewmodels.tabla_fake_viewmodel import TablaFakeViewModel


class MainWindow(QMainWindow):
    """Application's main window."""

    def __init__(self, settings_path: Path) -> None:
        super().__init__()
        self.setWindowTitle("TablaFake")
        self.resize(800, 400)

        connection = OracleConnection.from_settings(settings_path)
        repository = TablaFakeRepository(connection)
        self._viewmodel = TablaFakeViewModel(repository)
        self._model = TablaFakeTableModel()

        self._setup_ui()
        self._connect_signals()
        self._viewmodel.load_items()

    def _setup_ui(self) -> None:
        table = QTableView(self)
        table.setModel(self._model)
        table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        table.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        table.setEditTriggers(QAbstractItemView.EditTrigger.AllEditTriggers)
        table.setAlternatingRowColors(True)
        table.doubleClicked.connect(self._show_detail_for_index)
        self.setCentralWidget(table)

        toolbar = QToolBar("Acciones", self)
        toolbar.setMovable(False)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

        refresh_button = QPushButton("Recargar", self)
        refresh_button.clicked.connect(self._viewmodel.load_items)
        toolbar.addWidget(refresh_button)

        new_button = QPushButton("Nuevo", self)
        new_button.clicked.connect(self._open_create_dialog)
        toolbar.addWidget(new_button)

        delete_button = QPushButton("Eliminar", self)
        delete_button.clicked.connect(self._handle_delete_selected)
        toolbar.addWidget(delete_button)

        self.statusBar().showMessage("Listo")

    def _connect_signals(self) -> None:
        self._viewmodel.items_changed.connect(self._model.update_filas)
        self._viewmodel.error_occurred.connect(self._show_error)

    def _show_error(self, message: str) -> None:
        QMessageBox.critical(self, "Error", message)

    def _open_create_dialog(self) -> None:
        dialog = TablaFakeFormDialog(self)
        if dialog.exec() != dialog.DialogCode.Accepted:
            return
        data = dialog.get_data()
        fila = TablaFake(id=None, columna=data["columna"])
        self._viewmodel.add_item(fila)
        self._model.clear_selection()
        self.statusBar().showMessage("Fila creada (implementa la logica en el ViewModel/Repositorio)", 5000)

    def _handle_delete_selected(self) -> None:
        selected_ids = self._model.get_selected_ids()
        if not selected_ids:
            QMessageBox.information(self, "Eliminar", "Debe seleccionar al menos una fila.")
            return

        confirm = QMessageBox.question(
            self,
            "Eliminar filas",
            f"Eliminar {len(selected_ids)} fila(s) seleccionadas?",
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return

        self._viewmodel.delete_items(selected_ids)
        self._model.clear_selection()
        self.statusBar().showMessage("Filas eliminadas (implementa la logica en el ViewModel/Repositorio)", 5000)

    def _show_detail_for_index(self, index) -> None:
        fila = self._model.fila_at(index.row())
        if not fila:
            return
        dialog = TablaFakeDetailDialog(fila, self)
        dialog.exec()
