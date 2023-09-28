"""
Define funciones de utilidad para realizar consultas comunes y sencillas en la base de
datos.
"""

from typing import Sequence, TypeVar

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.database.models import Base

M = TypeVar("M", bound=Base)


async def get_all(
    db: AsyncSession, model: type[M], stmt: Select | None = None
) -> Sequence[M]:
    """
    Devuelve todos los registros de un modelo de la base de datos, esta función de
    utilidad es usada para consultas sencillas.

    Args:
        db (AsyncSession): Sesión de base de datos
        model (type[M]): Modelo a consultar
        stmt (Select, opcional): Consulta específica a realiazar.
    """
    if stmt is None:
        stmt = select(model)

    return (await db.scalars(stmt)).all()


async def get_by_id(db: AsyncSession, model: type[M], id: int) -> M | None:
    """
    Devuelve el registro con el ID dado.

    Args:
        db (AsyncSession): Sesión de base de datos
        model (type[M]): Modelo a consultar
        id (int): ID del registro a buscar

    Returns:
        Devuelve el registro con el ID dado o None si no existe.
    """
    stmt = select(model).where(model.id == id)
    return (await db.scalars(stmt)).first()


async def count_all(db: AsyncSession, model: type[M]) -> int:
    """
    Devuelve la cantidad total de registros de un modelo de la base de datos.

    Args:
        db (AsyncSession): Sesión de base de datos
        model (type[M]): Modelo a consultar

    Returns:
        int: Cantidad de registros en la base de datos.
    """
    return await db.scalar(select(func.count(model.id)))


async def exists_by_id(db: AsyncSession, model: type[M], id: int) -> bool:
    """
    Devuelve True si el registro con el ID dado existe en la base de datos.

    Args:
        db (AsyncSession): Sesión de base de datos
        model (type[M]): Modelo a consultar
        id (int): ID del registro a verificar

    Returns:
        bool: Devuelve True si el registro existe, False si no.
    """
    stmt = select(model).where(model.id == id)
    return await db.scalar(stmt) is not None


async def save(db: AsyncSession, model: type[M], refresh: bool = False) -> M:
    """
    Guarda la información del modelo en la base de datos.

    Args:
        db (AsyncSession): Sesión de base de datos
        model (type[M]): Modelo a guardar
        refresh (bool, opcional): Si se le debe indicar a SQLAlchemy que actulice la
        información del modelo con el de la base de datos, esto es útil cuando la base
        de datos realiza procesos adicionales como la ejecución de triggers para la
        asignación de valores a otros campos. Por defecto es False.
    """
    db.add(model)
    await db.commit()

    if refresh:
        await db.refresh(model)

    return model
