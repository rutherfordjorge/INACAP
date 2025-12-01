"""Servicio de inicio de sesión con Office 365 usando MSAL.

El módulo expone la clase :class:`Office365Login` que implementa
el flujo de dispositivo (device code) para obtener tokens de
Microsoft Entra ID (Azure AD) sin necesidad de interfaz gráfica.
"""
from __future__ import annotations

from pathlib import Path
from typing import Iterable, Optional

import msal


class Office365Login:
    """Administra un inicio de sesión sin interfaz para Office 365.

    Se basa en el flujo de dispositivo de MSAL (apto para scripts o
    apps sin navegador embebido). Los tokens se cachean en disco para
    evitar pedir autorización en cada ejecución.

    Parameters
    ----------
    client_id:
        Identificador de la aplicación pública registrada en Azure AD.
    tenant_id:
        ID o dominio del tenant (por ejemplo, ``"inacapmail.cl"``).
    scopes:
        Permisos solicitados (p. ej. ``["User.Read"]`` para Graph).
    cache_path:
        Ruta del archivo donde se persistirá la caché de tokens.
    allowed_domain:
        Dominio permitido para el usuario (``"inacapmail.cl"`` por defecto).
    """

    def __init__(
        self,
        client_id: str,
        tenant_id: str,
        scopes: Iterable[str],
        cache_path: str | Path = "office365_token_cache.json",
        allowed_domain: str = "inacapmail.cl",
    ) -> None:
        self.client_id = client_id
        self.tenant_id = tenant_id
        self.scopes = list(scopes)
        self.cache_path = Path(cache_path)
        self.allowed_domain = allowed_domain
        self.cache = msal.SerializableTokenCache()
        self._load_cache()
        authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        self.app = msal.PublicClientApplication(
            client_id=self.client_id,
            authority=authority,
            token_cache=self.cache,
        )

    def _load_cache(self) -> None:
        if self.cache_path.exists():
            self.cache.deserialize(self.cache_path.read_text())

    def _persist_cache(self) -> None:
        if self.cache.has_state_changed:
            self.cache_path.write_text(self.cache.serialize())

    def acquire_token(self, login_hint: Optional[str] = None) -> dict:
        """Obtiene un token de acceso válido para las ``scopes``.

        Primero intenta una adquisición silenciosa usando la caché. Si no
        hay sesión previa, inicia el flujo de dispositivo e imprime en
        consola las instrucciones para autorizar el inicio de sesión en el
        navegador del usuario.
        """

        login_hint = login_hint or f"usuario@{self.allowed_domain}"
        accounts = self.app.get_accounts(username=login_hint)
        result = None

        if accounts:
            result = self.app.acquire_token_silent(self.scopes, account=accounts[0])

        if not result:
            flow = self.app.initiate_device_flow(scopes=self.scopes, login_hint=login_hint)
            if "message" not in flow:
                raise RuntimeError("No se pudo iniciar el flujo de dispositivo de MSAL.")

            print(flow["message"])  # Mensaje con URL y código a ingresar.
            result = self.app.acquire_token_by_device_flow(flow)

        self._persist_cache()
        self._validate_result(result)
        return result

    def _validate_result(self, result: dict) -> None:
        if not result:
            raise RuntimeError("No se recibió respuesta de Microsoft al solicitar el token.")

        if "error" in result:
            description = result.get("error_description") or result["error"]
            raise RuntimeError(f"Error al autenticar en Office 365: {description}")

        username = self._extract_username(result)
        if self.allowed_domain and username and not username.lower().endswith(f"@{self.allowed_domain}"):
            raise PermissionError(
                f"El usuario {username} no pertenece al dominio permitido @{self.allowed_domain}."
            )

    def _extract_username(self, result: dict) -> Optional[str]:
        claims = result.get("id_token_claims", {})
        preferred = claims.get("preferred_username") or claims.get("email")
        if preferred:
            return preferred

        account = result.get("account") or {}
        return account.get("username")


def print_token_summary(result: dict) -> None:
    """Imprime un resumen seguro del token devuelto por MSAL."""

    username = (
        result.get("id_token_claims", {}).get("preferred_username")
        or result.get("account", {}).get("username")
        or "<desconocido>"
    )
    scopes = result.get("scope", "")
    print("Autenticado como:", username)
    print("Scopes concedidos:", scopes)
    if "access_token" in result:
        print("Token (primeros 50 caracteres):", result["access_token"][:50], "...")
