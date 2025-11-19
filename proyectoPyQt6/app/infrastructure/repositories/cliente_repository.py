"""Repository layer for Cliente entity."""
from __future__ import annotations

from typing import List, Optional, Sequence

from app.domain.models.cliente import Cliente
from app.infrastructure.database.oracle_connection import OracleConnection


class ClienteRepository:
    """Handles CRUD operations over CLIENTE table."""

    def __init__(self, connection_factory: OracleConnection) -> None:
        self._connection_factory = connection_factory

    def get_all(self) -> List[Cliente]:
        """Retrieve every client from the database."""

        query = (
            "SELECT ID, RUT, DV, NOMBRE, APELLIDO, FECHA_NAC, EMAIL, TELEFONO, DIRECCION, "
            "ESTADO_CLIENTE, LIMITE_CREDITO FROM CLIENTE"
        )
        with self._connection_factory.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

        return [self._map_row(row) for row in rows]

    def get_by_id(self, cliente_id: int) -> Optional[Cliente]:
        """Return a client by its identifier."""

        query = (
            "SELECT ID, RUT, DV, NOMBRE, APELLIDO, FECHA_NAC, EMAIL, TELEFONO, DIRECCION, "
            "ESTADO_CLIENTE, LIMITE_CREDITO FROM CLIENTE WHERE ID = :id"
        )
        with self._connection_factory.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, id=cliente_id)
                row = cursor.fetchone()

        return self._map_row(row) if row else None

    def add(self, cliente: Cliente) -> int:
        """Insert a new client and return its generated ID."""

        query = (
            "INSERT INTO CLIENTE (RUT, DV, NOMBRE, APELLIDO, FECHA_NAC, EMAIL, TELEFONO, DIRECCION, ESTADO_CLIENTE, LIMITE_CREDITO) "
            "VALUES (:rut, :dv, :nombre, :apellido, :fecha_nac, :email, :telefono, :direccion, :estado_cliente, :limite_credito) "
            "RETURNING ID INTO :id"
        )
        with self._connection_factory.get_connection() as conn:
            with conn.cursor() as cursor:
                id_var = cursor.var(int)
                cursor.execute(
                    query,
                    rut=cliente.rut,
                    dv=cliente.dv,
                    nombre=cliente.nombre,
                    apellido=cliente.apellido,
                    fecha_nac=cliente.fecha_nac,
                    email=cliente.email,
                    telefono=cliente.telefono,
                    direccion=cliente.direccion,
                    estado_cliente=cliente.estado_cliente,
                    limite_credito=cliente.limite_credito,
                    id=id_var,
                )
                conn.commit()
                return int(id_var.getvalue())

    def update(self, cliente: Cliente) -> None:
        """Update an existing client."""

        if cliente.id is None:
            raise ValueError("El cliente debe tener ID para ser actualizado")

        query = (
            "UPDATE CLIENTE SET RUT=:rut, DV=:dv, NOMBRE=:nombre, APELLIDO=:apellido, FECHA_NAC=:fecha_nac, "
            "EMAIL=:email, TELEFONO=:telefono, DIRECCION=:direccion, ESTADO_CLIENTE=:estado_cliente, LIMITE_CREDITO=:limite_credito "
            "WHERE ID=:id"
        )
        with self._connection_factory.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    query,
                    id=cliente.id,
                    rut=cliente.rut,
                    dv=cliente.dv,
                    nombre=cliente.nombre,
                    apellido=cliente.apellido,
                    fecha_nac=cliente.fecha_nac,
                    email=cliente.email,
                    telefono=cliente.telefono,
                    direccion=cliente.direccion,
                    estado_cliente=cliente.estado_cliente,
                    limite_credito=cliente.limite_credito,
                )
                conn.commit()

    def delete(self, cliente_id: int) -> None:
        """Delete a client by ID."""

        with self._connection_factory.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM CLIENTE WHERE ID = :id", id=cliente_id)
                conn.commit()

    @staticmethod
    def _map_row(row: Sequence) -> Cliente:
        """Map a DB row to the domain model."""

        return Cliente(
            id=row[0],
            rut=row[1],
            dv=row[2],
            nombre=row[3],
            apellido=row[4],
            fecha_nac=row[5],
            email=row[6],
            telefono=row[7],
            direccion=row[8],
            estado_cliente=row[9],
            limite_credito=row[10],
        )

