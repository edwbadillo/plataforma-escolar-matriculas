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

    def __init__(self, db: AsyncSession, model: type[Model]) -> None:
        """
        Constructor del repositorio.

        Args:
            db (AsyncSession): Sesión de base de datos
            model (type[Model]): Modelo de la base de datos usado para las consultas
            base.
        """
        self._db = db
        self._model = model

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

    async def get_by_id(self, id: int, optional: bool = False) -> Model:
        """
        Devuelve el registro con el ID dado.

        Args:
            id (int): ID del registro a buscar
            optional (bool, optional): Por defecto es False indicando que si no existe
            un registro por el ID dado lanzará una excepción. Si se indica True es
            posible devolver None si no existe el registro.

        Returns:
            Devuelve el registro con el ID dado o None si no existe (si optional=True).
        """
        stmt = select(self._model).where(self._model.id == id)
        result = await self._db.scalars(stmt)

        if optional:
            return result.one_or_none()
        return result.one()


class SaveMixin(Generic[Model]):
    async def save(self, model: Model) -> Model:
        """
        Guarda el modelo en la base de datos.
        """
        self._db.add(model)
        await self._db.commit()
        return model
