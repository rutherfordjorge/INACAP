# Login con Office 365 sin interfaz

Este módulo permite autenticar cuentas del dominio `@inacapmail.cl` contra Microsoft Office 365 (Microsoft Entra ID/Azure AD) sin abrir una ventana de navegador embebido. Usa el flujo de **código de dispositivo** de la librería [MSAL](https://pypi.org/project/msal/) para mostrar en consola las instrucciones de autorización.

## Archivos incluidos

- `login_service.py`: clase `Office365Login` que gestiona el flujo de inicio de sesión, la caché de tokens y valida que el usuario pertenezca al dominio permitido.
- `example_usage.py`: script mínimo que ejecuta el flujo y muestra un resumen del token obtenido.
- `__init__.py`: permite importar el módulo como paquete.

## Requisitos previos

1. Instala las dependencias del proyecto (agregamos `msal` al `requirements.txt`):

   ```bash
   pip install -r requirements.txt
   ```

2. Registra una **Aplicación (cliente) pública** en Azure AD (Entra ID):
   - Tipo: *Public client/native (mobile & desktop)*.
   - Permisos delegados (por ejemplo `User.Read` de Microsoft Graph).
   - Copia el **Client ID** y el **Tenant ID** (o dominio).

3. Ten a mano una cuenta `usuario@inacapmail.cl` con permisos para el recurso que vayas a consumir.

## Cómo funciona el código

1. `Office365Login` crea una `PublicClientApplication` de MSAL usando el `tenant_id` para apuntar al directorio correcto (`https://login.microsoftonline.com/<tenant_id>`).
2. Los tokens se cachean en disco (`office365_token_cache.json` por defecto) mediante `msal.SerializableTokenCache` para permitir inicios silenciosos posteriores.
3. `acquire_token()` intenta primero `acquire_token_silent`; si no hay token válido, inicia el **device flow** con `initiate_device_flow`, que devuelve una URL y un código de verificación.
4. El usuario abre la URL en cualquier navegador, ingresa el código y completa el login; MSAL bloquea hasta recibir la confirmación y devuelve el token.
5. `_validate_result` revisa errores y comprueba que `preferred_username` termine en `@inacapmail.cl`, evitando sesiones de otros dominios.
6. `print_token_summary` imprime un resumen seguro (no expone el token completo).

## Uso rápido

Puedes definir tus credenciales como variables de entorno y ejecutar el ejemplo:

```bash
export MSAL_CLIENT_ID="<CLIENT_ID_DE_TU_APP>"
export MSAL_TENANT_ID="inacapmail.cl"  # o el GUID del tenant
python office365_login/example_usage.py
```

El script mostrará algo como:

```
Para iniciar sesión, visita https://microsoft.com/devicelogin e ingresa el código XXXX-YYYY.
Autenticado como: usuario@inacapmail.cl
Scopes concedidos: User.Read
Token (primeros 50 caracteres): eyJ0eXAiOiJKV1QiLCJh... 
```

Para integrarlo en otro módulo, importa y reutiliza el servicio:

```python
from office365_login.login_service import Office365Login

login = Office365Login(
    client_id="<CLIENT_ID_DE_TU_APP>",
    tenant_id="inacapmail.cl",  # o el GUID del tenant
    scopes=["User.Read"],
)

result = login.acquire_token(login_hint="usuario@inacapmail.cl")
access_token = result["access_token"]
```

El método `acquire_token` lanzará un `PermissionError` si el usuario autenticado no pertenece al dominio `@inacapmail.cl`.
