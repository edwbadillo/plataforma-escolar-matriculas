from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Grade


async def get_grades(db: AsyncSession) -> list[Grade]:
    """
    Lista todos los grados registrados definidos por el sistema educativo y del colegio.
    """
    return await db.scalars(select(Grade))
