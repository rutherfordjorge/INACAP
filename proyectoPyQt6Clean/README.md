# TablaFake en PyQt6 (esqueleto para alumnos)

Proyecto de escritorio en PyQt6 con estructura MVVM listo para que los alumnos completen su propio CRUD. La entidad principal es `TablaFake`, con dos campos:

- `id: int | None`
- `columna: str`

El repositorio y el ViewModel ya exponen los metodos necesarios, pero sus cuerpos solo contienen `pass` para que los estudiantes implementen la logica de base de datos que prefieran.

## Requisitos rapidos

- Python 3.11+
- Dependencias: `pip install -r requirements.txt`
- Archivo `config/settings.json` con la configuracion de conexion (puedes apuntar a Oracle u otra base y adaptar el repositorio).

## Archivos clave

- `main.py`: punto de entrada; crea `QApplication`, carga la configuracion y abre `MainWindow`.
- `app/domain/models/modeloFake.py`: dataclass `TablaFake` (id, columna).
- `app/infrastructure/database/oracle_connection.py`: factoria de conexiones (util si usas Oracle; puedes reemplazarla).
- `app/infrastructure/repositories/tabla_fake_repository.py`: CRUD stub con solo `pass` para que los alumnos escriban sus consultas.
- `app/viewmodels/tabla_fake_viewmodel.py`: capa de presentacion; metodos vacios para orquestar el flujo entre UI y repositorio.
- `app/ui/tabla_fake_table_model.py`: `QAbstractTableModel` que muestra `id` y `columna`, con columna de seleccion por checkbox.
- `app/ui/dialogs.py`: dialogos simples para crear y ver detalles de una fila.
- `app/ui/main_window.py`: ventana principal con acciones **Recargar**, **Nuevo**, **Eliminar** y tabla central.

## Usar el esqueleto

1. Completa los metodos del repositorio (`get_all`, `add`, `update`, etc.) con la logica de tu base de datos.
2. Haz que el ViewModel invoque esos metodos y emita las senales correspondientes (`items_changed`, `error_occurred`).
3. Ajusta la UI si tu tabla real tiene mas columnas (extiende `TablaFake` y el `TablaFakeTableModel`).
4. Ejecuta con:

   ```bash
   python main.py
   ```

La aplicacion arranca pero no realiza operaciones reales hasta que completes el CRUD. Es intencionalmente minimalista para fines didacticos.
