from typing import Any

import httpx
from fastapi import status
from sqlalchemy.exc import IntegrityError

from app.common.database.models import Base
from app.common.messages import RESOURCE_NOT_FOUND
from app.common.responses import CommonResponse


def check_constraint_violation(exc: IntegrityError, model: Base, constraint_name: str):
    """
    Verifica que haya un error de resctricción (check constraint) dado por PostgreSQL.

    Args:
        exc (IntegrityError): Excepción generada.
        model (Base): Modelo SqlAlchemy que genera la excepción.
        constraint_name (str): Nombre de la restricción que genera el error, consulte
        el modelo o la tabla de la base de datos para obtener su nombre.
    """
    error = str(exc)
    assert "psycopg.errors.CheckViolation" in error

    table_name = model.__tablename__

    # Revise las convenciones de nombres en Base.metadata
    db_constraint_name = f"{table_name}_{constraint_name}_check"

    assert f'"{table_name}" violates check constraint "{db_constraint_name}"' in error


def check_unique_constraint_violation(
    exc: IntegrityError, field: str, duplicated_value: Any
):
    """
    Verifica que haya un error de unicidad (unique constraint) dado por PostgreSQL.

    Args:
        exc (IntegrityError): Excepción generada
        field (str): Nombre del campo que genera el error
        duplicated_value (Any): Valor duplicado que genera el error
    """
    error = str(exc)
    assert "psycopg.errors.UniqueViolation" in error
    assert f"Key ({field})=({duplicated_value}) already exists"


def check_resource_not_found_response(response: httpx.Response):
    """
    Verifica que la respuesta dada sea un error de recurso no encontrado por defecto.
    """
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == CommonResponse(message=RESOURCE_NOT_FOUND).model_dump()
