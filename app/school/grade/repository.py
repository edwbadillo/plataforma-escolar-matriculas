from app.common.database.repository import BaseRepository

from .models import Grade


class GradeRepository(BaseRepository[Grade]):
    """
    Repositorio de los grados escolares.
    """
