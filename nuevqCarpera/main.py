"""CLI entry point for Oracle stored procedure operations."""
from __future__ import annotations

import argparse
from datetime import datetime, date
from pathlib import Path
from typing import Callable, Iterable, Optional

from app.domain.models.cliente import Cliente
from app.infrastructure.database.oracle_connection import OracleConnection
from app.infrastructure.repositories.cliente_repository import ClienteRepository


def _parse_date(date_str: Optional[str]) -> Optional[date]:
    """Convert a YYYY-MM-DD string into a ``date`` object."""

    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValueError("Las fechas deben tener el formato YYYY-MM-DD") from exc


def _build_repository(settings_path: Path) -> ClienteRepository:
    """Instantiate a repository using the given settings path."""

    connection_factory = OracleConnection.from_settings(settings_path)
    return ClienteRepository(connection_factory)


def _print_cliente(cliente: Cliente) -> None:
    """Print a single cliente row in a friendly format."""

    print(
        f"ID={cliente.id} | RUT={cliente.rut}-{cliente.dv} | "
        f"Nombre={cliente.nombre} {cliente.apellido} | "
        f"Email={cliente.email} | Teléfono={cliente.telefono} | "
        f"Estado={cliente.estado_cliente} | Límite={cliente.limite_credito}"
    )


def _handle_list(repo: ClienteRepository) -> None:
    """List all clientes using ``SP_GET_CLIENTES``."""

    clientes = repo.get_all()
    if not clientes:
        print("No se encontraron clientes.")
        return

    for cliente in clientes:
        _print_cliente(cliente)


def _handle_get(repo: ClienteRepository, cliente_id: int) -> None:
    """Get a single cliente by id using ``SP_GET_CLIENTE_BY_ID``."""

    cliente = repo.get_by_id(cliente_id)
    if not cliente:
        print(f"Cliente con ID {cliente_id} no encontrado.")
        return

    _print_cliente(cliente)


def _handle_add(repo: ClienteRepository, args: argparse.Namespace) -> None:
    """Insert a new cliente using ``SP_INSERT_CLIENTE``."""

    cliente = Cliente(
        id=None,
        rut=args.rut,
        dv=args.dv,
        nombre=args.nombre,
        apellido=args.apellido,
        fecha_nac=_parse_date(args.fecha_nac),
        email=args.email,
        telefono=args.telefono,
        direccion=args.direccion,
        estado_cliente=args.estado,
        limite_credito=args.limite_credito,
    )
    new_id = repo.add(cliente)
    print(f"Cliente creado con ID {new_id}.")


def _handle_update(repo: ClienteRepository, args: argparse.Namespace) -> None:
    """Update an existing cliente using ``SP_UPDATE_CLIENTE``."""

    cliente = Cliente(
        id=args.id,
        rut=args.rut,
        dv=args.dv,
        nombre=args.nombre,
        apellido=args.apellido,
        fecha_nac=_parse_date(args.fecha_nac),
        email=args.email,
        telefono=args.telefono,
        direccion=args.direccion,
        estado_cliente=args.estado,
        limite_credito=args.limite_credito,
    )
    repo.update(cliente)
    print(f"Cliente con ID {args.id} actualizado correctamente.")


def _handle_delete(repo: ClienteRepository, cliente_ids: Iterable[int]) -> None:
    """Delete one or more clientes using ``SP_DELETE_CLIENTE``."""

    repo.delete_many(cliente_ids)
    print(f"Clientes eliminados: {', '.join(map(str, cliente_ids))}")


def main() -> int:
    """Run the CLI to consume stored procedures without a UI."""

    parser = argparse.ArgumentParser(
        description=(
            "Ejecuta operaciones CRUD contra Oracle utilizando stored procedures."
        )
    )
    parser.add_argument(
        "--settings",
        type=Path,
        default=Path(__file__).parent / "config" / "settings.json",
        help="Ruta al archivo JSON con la configuración de la BD",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="Listar todos los clientes")

    get_parser = subparsers.add_parser("get", help="Obtener un cliente por ID")
    get_parser.add_argument("id", type=int, help="Identificador del cliente")

    add_parser = subparsers.add_parser("add", help="Crear un nuevo cliente")
    add_parser.add_argument("--rut", required=True)
    add_parser.add_argument("--dv", required=True)
    add_parser.add_argument("--nombre", required=True)
    add_parser.add_argument("--apellido", required=True)
    add_parser.add_argument("--fecha-nac", dest="fecha_nac")
    add_parser.add_argument("--email", required=True)
    add_parser.add_argument("--telefono", required=True)
    add_parser.add_argument("--direccion", required=True)
    add_parser.add_argument(
        "--estado",
        required=True,
        help="Estado del cliente (por ejemplo, ACTIVO/INACTIVO)",
    )
    add_parser.add_argument(
        "--limite-credito",
        dest="limite_credito",
        type=float,
        help="Límite de crédito opcional",
    )

    update_parser = subparsers.add_parser(
        "update", help="Actualizar un cliente existente"
    )
    update_parser.add_argument("--id", type=int, required=True)
    update_parser.add_argument("--rut", required=True)
    update_parser.add_argument("--dv", required=True)
    update_parser.add_argument("--nombre", required=True)
    update_parser.add_argument("--apellido", required=True)
    update_parser.add_argument("--fecha-nac", dest="fecha_nac")
    update_parser.add_argument("--email", required=True)
    update_parser.add_argument("--telefono", required=True)
    update_parser.add_argument("--direccion", required=True)
    update_parser.add_argument("--estado", required=True)
    update_parser.add_argument(
        "--limite-credito",
        dest="limite_credito",
        type=float,
        help="Límite de crédito opcional",
    )

    delete_parser = subparsers.add_parser(
        "delete", help="Eliminar uno o más clientes"
    )
    delete_parser.add_argument(
        "ids", nargs="+", type=int, help="Identificadores de clientes a eliminar"
    )

    args = parser.parse_args()
    repo = _build_repository(args.settings)

    handlers: dict[str, Callable[[ClienteRepository, argparse.Namespace], None]] = {
        "list": lambda r, _: _handle_list(r),
        "get": lambda r, parsed: _handle_get(r, parsed.id),
        "add": _handle_add,
        "update": _handle_update,
        "delete": lambda r, parsed: _handle_delete(r, parsed.ids),
    }

    try:
        handler = handlers[args.command]
        handler(repo, args)
        return 0
    except Exception as exc:  # pragma: no cover - runtime safety for CLI usage
        print(f"Error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
