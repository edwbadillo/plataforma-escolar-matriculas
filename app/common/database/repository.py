from typing import Generic, TypeVar

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Base

Model = TypeVar("Model", bound=Base)


class BaseRepository(Generic[Model]):
    """
    Clase base para cualquier repositorio que se conecta a la base de datos.

    Define los métodos comunes para cualquier repositorio y ofrece un acceso a la sesión
    de la base de datos.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Constructor del repositorio.

        Args:
            db (AsyncSession): Sesión de base de datos
        """
        self._db = db
        self._model: type[Model] = Model

    async def get_all(self) -> list[Model]:
        """
        Devuelve todos los registros de la base de datos.

        Returns:
            Lista de modelos sqlalchemy
        """
        stmt = select(self._model)
        result = await self._db.scalars(stmt)
        return result.all()

    async def exists_by_id(self, id: int) -> bool:
        """
        Devuelve True si el registro con el ID dado existe en la base de datos.

        Args:
            id (int): ID del registro a verificar

        Returns:
            bool: Devuelve True si el registro existe, False si no.
        """
        stmt = select(self._model.id).where(self._model.id == id)
        result = await self._db.scalar(stmt)
        return result is not None

    async def count(self) -> int:
        """
        Devuelve la cantidad de registros en la base de datos.
        """
        return await self._db.scalar(select(func.count(self._model.id)))
