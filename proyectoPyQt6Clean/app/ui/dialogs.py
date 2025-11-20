"""Dialog windows for TablaFake workflows."""
from __future__ import annotations

from typing import Dict

from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QVBoxLayout,
)

from app.domain.models.modeloFake import TablaFake


class TablaFakeFormDialog(QDialog):
    """Minimal dialog to capture TablaFake data."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Nueva fila")
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        self.columna_input = QLineEdit()
        self.columna_input.setPlaceholderText("Texto para la columna")
        form_layout.addRow("Columna", self.columna_input)

        layout.addLayout(form_layout)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self._on_accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

    def _on_accept(self) -> None:
        if not self.columna_input.text().strip():
            QMessageBox.warning(self, "Validacion", "La columna no puede estar vacia.")
            return
        self.accept()

    def get_data(self) -> Dict[str, object]:
        """Return user input."""

        return {"columna": self.columna_input.text().strip()}


class TablaFakeDetailDialog(QDialog):
    """Displays TablaFake info."""

    def __init__(self, fila: TablaFake, parent=None) -> None:
        super().__init__(parent)
        self._fila = fila
        self.setWindowTitle("Detalle TablaFake")
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        def add_row(label: str, value: str) -> None:
            form_layout.addRow(label, QLabel(value))

        add_row("ID", str(self._fila.id or ""))
        add_row("Columna", self._fila.columna)

        layout.addLayout(form_layout)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        button_box.rejected.connect(self.reject)
        button_box.accepted.connect(self.accept)
        button_box.button(QDialogButtonBox.StandardButton.Close).clicked.connect(self.accept)
        layout.addWidget(button_box)
