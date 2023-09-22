from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Grade


async def get_grades(db: AsyncSession) -> list[Grade]:
    """
    Lista todos los grados registrados definidos por el sistema educativo y del colegio.

    Args:
        db (AsyncSession): Sesión de base de datos
    """
    return list(await db.scalars(select(Grade)))


async def exists_by_id(db: AsyncSession, id: int) -> bool:
    """
    Devuelve True si el grado con el id dado existe en la base de datos.

    Args:
        db (AsyncSession): Sesión de base de datos
        id (int): ID del registro a verificar
    """
    stmt = select(Grade.id).where(Grade.id == id)
    return (await db.scalar(stmt)) is not None
