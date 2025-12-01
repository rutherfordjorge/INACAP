# INACAP

Proyectos del INACAP

## Panel demo

Esta rama incluye una interfaz ligera organizada por carpetas:

- `src/views/login`: pantalla de autenticación con Office 365 simulado.
- `src/views/listing`: pantalla de listado principal.
- `src/components/actions/*`: cada acción (agregar, quitar, recargar) tiene su propia carpeta.
- `src/components/feedback`: componentes reutilizables para mensajes de alerta.
- `src/services/auth`: servicio de autenticación y sesión.

### Cómo usar

1. Abre `index.html` en el navegador.
2. Ingresa el usuario de demostración `usuario@office365.com` y la contraseña `inacap123`.
3. Si las credenciales son correctas verás el listado con las acciones disponibles; si son incorrectas se mostrará un mensaje de error.
4. Usa “Cerrar sesión” para volver a la vista de login.
