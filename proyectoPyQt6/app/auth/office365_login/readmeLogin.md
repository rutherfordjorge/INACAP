# Inicio de sesión con Office 365 (Azure AD)

Este módulo implementa un flujo de autenticación **device code** con la biblioteca [`msal`](https://github.com/AzureAD/microsoft-authentication-library-for-python). Está pensado para validar usuarios del dominio `@inacapmail.cl` antes de mostrar la interfaz principal.

## Archivos

- `authenticator.py`: encapsula toda la lógica de autenticación.
- `__init__.py`: exporta los símbolos públicos.
- `readmeLogin.md`: este documento.
- `config/office365.json`: configuración utilizada por el autenticador (ver más abajo).

## Configuración requerida

1. Registra una aplicación pública en Azure AD y habilita el flujo **Device Code**.
2. Copia `config/office365.example.json` como `config/office365.json` y rellena los valores:
   ```json
   {
     "tenant_id": "<ID_DEL_TENANT>",
     "client_id": "<ID_DE_LA_APLICACION_PUBLICA>",
     "username_hint": "usuario@inacapmail.cl",
     "scopes": ["User.Read"]
   }
   ```

   - `tenant_id`: el GUID del directorio (Tenant ID).
   - `client_id`: el Application (client) ID.
   - `username_hint`: opcional; se muestra en mensajes y ayuda a identificar al usuario esperado.
   - `scopes`: permisos solicitados (por defecto `User.Read`).

## Cómo funciona el código

1. `Office365Authenticator.from_file` lee el JSON de configuración y prepara el cliente de MSAL (`PublicClientApplication`).
2. `login()` inicia el flujo de *device code* (`initiate_device_flow`), que devuelve la URL y el código que el usuario debe ingresar. Estos datos se imprimen en consola para evitar dependencias de una interfaz adicional.
3. `acquire_token_by_device_flow` espera a que el usuario valide el código en el navegador. Si la autenticación es correcta devuelve el `access_token` y la información del usuario (`preferred_username`).
4. Se retorna un `LoginResult` indicando éxito o error. El mensaje se consume en `main.py` para avisar al usuario y decidir si se muestra la ventana principal.

## Uso en la aplicación

`main.py` llama al autenticador **antes** de crear la ventana principal:

```python
settings_path = Path(__file__).parent / "config" / "settings.json"
office365_settings = Path(__file__).parent / "config" / "office365.json"
authenticator = Office365Authenticator.from_file(office365_settings)
result = authenticator.login()

if not result.success:
    QMessageBox.critical(None, "Login", result.message)
    return 1

QMessageBox.information(None, "Login", result.message)
window = MainWindow(settings_path)
```

- Si el login falla se muestra un mensaje de error y la app termina.
- Si el login es correcto se continúa al listado de clientes.

## Dependencias

- `msal`: biblioteca oficial de Microsoft para autenticarse contra Azure AD.

Instálala junto con el resto de dependencias del proyecto:

```bash
pip install -r requirements.txt
```
