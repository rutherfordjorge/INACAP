"""Office 365 authentication helper using MSAL."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import msal


@dataclass
class LoginResult:
    """Outcome of an authentication attempt."""

    success: bool
    message: str
    account: Optional[str] = None


class Office365Authenticator:
    """Encapsulates the device-code login against Azure AD/Office 365."""

    def __init__(
        self,
        tenant_id: str,
        client_id: str,
        scopes: List[str],
        username_hint: Optional[str] = None,
    ) -> None:
        self._tenant_id = tenant_id
        self._client_id = client_id
        self._scopes = scopes
        self._username_hint = username_hint

    @classmethod
    def from_file(cls, settings_path: Path) -> "Office365Authenticator":
        """Instantiate the authenticator from a JSON settings file."""

        if not settings_path.exists():
            raise FileNotFoundError(f"No se encontró la configuración en {settings_path}.")

        with settings_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        return cls(
            tenant_id=data.get("tenant_id", ""),
            client_id=data.get("client_id", ""),
            scopes=data.get("scopes", ["User.Read"]),
            username_hint=data.get("username_hint"),
        )

    def login(self) -> LoginResult:
        """Perform device code login and return the outcome."""

        authority = f"https://login.microsoftonline.com/{self._tenant_id}"
        app = msal.PublicClientApplication(self._client_id, authority=authority)

        flow = app.initiate_device_flow(scopes=self._scopes)
        if "user_code" not in flow:
            message = flow.get("error_description", "No se pudo iniciar el flujo de login.")
            return LoginResult(False, message)

        # Mostrar instrucciones en consola para no depender de una interfaz adicional
        print("Visita", flow["verification_uri"], "e ingresa el código", flow["user_code"])

        result = app.acquire_token_by_device_flow(flow)
        if "access_token" in result:
            account = (
                result.get("id_token_claims", {}).get("preferred_username")
                or self._username_hint
                or ""
            )
            message = f"Inicio de sesión correcto para {account or 'usuario'}."
            return LoginResult(True, message, account or None)

        error_message = result.get("error_description", "No se pudo autenticar con Office 365.")
        return LoginResult(False, error_message)
