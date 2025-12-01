"""Ejemplo de uso del inicio de sesión sin interfaz."""
from __future__ import annotations

import os

from office365_login.login_service import Office365Login, print_token_summary


if __name__ == "__main__":
    client_id = os.environ.get("MSAL_CLIENT_ID", "<CLIENT_ID_DE_TU_APP>")
    tenant_id = os.environ.get("MSAL_TENANT_ID", "inacapmail.cl")

    login = Office365Login(
        client_id=client_id,
        tenant_id=tenant_id,
        scopes=["User.Read"],
        cache_path=".msal_token_cache.json",
    )

    token_result = login.acquire_token(login_hint="usuario@inacapmail.cl")
    print_token_summary(token_result)
