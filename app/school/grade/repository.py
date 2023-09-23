from sqlalchemy.ext.asyncio import AsyncSession

from app.common.database.repository import BaseRepository

from .models import Grade


class GradeRepository(BaseRepository[Grade]):
    """
    Repositorio de los grados escolares.
    """

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)
        self._model = Grade
