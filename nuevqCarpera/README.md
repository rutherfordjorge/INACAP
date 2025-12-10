# nuevqCarpera

Proyecto basado en `proyectoPyQt6` pero sin la UI. Expone un CLI para probar la
conexión a Oracle Autonomous Database y consumir los stored procedures que ya
existían en el repositorio original.

## Requisitos

- Python 3.10+
- Dependencias del archivo `requirements.txt`
- Un wallet de Oracle Autonomous Database (no se incluye en el repositorio).

Instala las dependencias con:

```bash
pip install -r requirements.txt
```

## Configuración

1. Descarga el wallet desde tu instancia de Autonomous Database y descomprímelo
en una carpeta local fuera del repositorio (o dentro, pero siempre ignorada por
git).
2. Edita `config/settings.json` y completa:
   - `user`: usuario de la base de datos.
   - `password`: contraseña del usuario.
   - `dsn`: nombre del servicio (por ejemplo `mydb_tp` o `mydb_medium`).
   - `wallet_dir`: ruta absoluta a la carpeta donde descomprimiste el wallet.
   - `wallet_password`: si el wallet tiene contraseña, inclúyela; de lo
     contrario, deja `null`.
3. Verifica que `.gitignore` esté excluyendo los archivos del wallet.

## Uso del CLI

Ejecuta el comando desde la raíz del proyecto. Ejemplos:

Listar todos los clientes:

```bash
python main.py list
```

Obtener un cliente específico:

```bash
python main.py get 10
```

Agregar un cliente nuevo:

```bash
python main.py add \
  --rut 12345678 \
  --dv 9 \
  --nombre Juan \
  --apellido Pérez \
  --fecha-nac 1990-01-01 \
  --email juan.perez@example.com \
  --telefono "+56 9 1234 5678" \
  --direccion "Av. Siempre Viva 123" \
  --estado ACTIVO \
  --limite-credito 500000
```

Actualizar un cliente:

```bash
python main.py update \
  --id 10 \
  --rut 12345678 \
  --dv 9 \
  --nombre Juan \
  --apellido Pérez \
  --fecha-nac 1990-01-01 \
  --email juan.perez@example.com \
  --telefono "+56 9 1234 5678" \
  --direccion "Av. Siempre Viva 123" \
  --estado ACTIVO \
  --limite-credito 750000
```

Eliminar uno o más clientes:

```bash
python main.py delete 10 11 12
```

Se puede personalizar la ruta al archivo de configuración pasando `--settings`:

```bash
python main.py list --settings /ruta/a/otro/settings.json
```
