"""Oracle Autonomous Database connection helper."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional

import oracledb


class OracleConnection:
    """Encapsulates connection management to Oracle Autonomous Database."""

    def __init__(self, user: str, password: str, dsn: str) -> None:
        self._user = user
        self._password = password
        self._dsn = dsn

    def get_connection(self) -> oracledb.Connection:
        """Return a new Oracle connection instance.

        Raises:
            oracledb.Error: If the connection cannot be established.
        """

        try:
            return oracledb.connect(user=self._user, password=self._password, dsn=self._dsn)
        except oracledb.Error as exc:  # pragma: no cover - requires DB
            raise ConnectionError("No se pudo conectar a Oracle Autonomous Database") from exc

    @classmethod
    def from_settings(cls, settings_path: Path) -> "OracleConnection":
        """Create an instance from a JSON settings file."""

        with settings_path.open("r", encoding="utf-8") as file:
            data: Dict[str, Any] = json.load(file)

        db_conf: Dict[str, Optional[str]] = data.get("database", {})
        user = db_conf.get("user") or ""
        password = db_conf.get("password") or ""
        dsn = db_conf.get("dsn") or ""
        return cls(user=user, password=password, dsn=dsn)

