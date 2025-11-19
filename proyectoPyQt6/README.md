# INACAP
Proyectos del INACAP

## Configurar Oracle Autonomous Database

1. Descarga tu wallet de Oracle Autonomous Database y descomprimela en `config/wallet` (debe contener archivos como `tnsnames.ora`, `cwallet.sso`, etc.).  
2. Actualiza `config/settings.json` con tus credenciales y, si tu wallet tiene contrasena, rellena `wallet_password`.  
3. Asegurate de que el valor `dsn` coincida con el alias definido en el `tnsnames.ora` (por ejemplo `jrk202502_medium`).  

El helper `OracleConnection` usa automaticamente los archivos de la wallet para resolver el alias y establecer una conexion TLS segura. Si la ruta configurada no existe la aplicacion mostrara un error explicando que falta.
