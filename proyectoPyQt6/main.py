"""Entry point for the PyQt6 MVVM application."""
from __future__ import annotations

import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication, QMessageBox

from app.auth.office365_login import Office365Authenticator
from app.ui.main_window import MainWindow


def main() -> int:
    """Run the desktop application."""

    app = QApplication(sys.argv)
    base_path = Path(__file__).parent
    settings_path = base_path / "config" / "settings.json"
    login_settings_path = base_path / "config" / "office365.json"

    try:
        authenticator = Office365Authenticator.from_file(login_settings_path)
    except FileNotFoundError as exc:
        QMessageBox.critical(None, "Login", str(exc))
        return 1

    login_result = authenticator.login()
    if not login_result.success:
        QMessageBox.critical(None, "Login", login_result.message)
        return 1

    QMessageBox.information(None, "Login", login_result.message)

    window = MainWindow(settings_path)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
