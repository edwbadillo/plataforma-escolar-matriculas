from enum import Enum
from typing import Sequence

from sqlalchemy import select

from app.common.database import funcs
from app.common.database.repository import DBRepository

from .models import EducationLevel, Grade


class Sort(Enum):
    """
    Enumerado para ordenar los niveles educativos o grados escolares, los literales
    se hacen referencia al nombre del método de ordenación de SQLAlchemy asc() o desc().
    """

    ASC = "asc"
    DESC = "desc"


class EducationalLevelRepository(DBRepository):
    """Repositorio de niveles educativos"""

    async def get_all(self, sort: Sort = Sort.ASC) -> Sequence[EducationLevel]:
        """
        Devuelve todos los niveles educativos.

        Args:
            order (Order, opcional): Especifica el modo de ordenamiento basado en el
            número de orden de un nivel educativo, por defecto, se ordena del más bajo
            nivel educativo al más alto.

        Returns:
            Sequence[EducationLevel]: Lista de niveles educativos.
        """
        column_order = getattr(EducationLevel.order, sort.value)
        stmt = select(EducationLevel).order_by(column_order())
        return await funcs.get_all(self._db, EducationLevel, stmt)

    async def exists_by_id(self, id: int) -> bool:
        """
        Devuelve True si el nivel educativo con el ID dado existe en la base de datos.

        Args:
            id (int): ID del nivel educativo a verificar.

        Returns:
            bool: Devuelve True si el nivel educativo existe, de lo contrario False.
        """
        return await funcs.exists_by_id(self._db, EducationLevel, id)


class GradeRepository(DBRepository):
    """Repositorio de grados o niveles escolares"""

    async def get_all(
        self, order: Sort = Sort.ASC, *, by_education_level: EducationLevel | int = None
    ) -> Sequence[Grade]:
        """
        Devuelve todos los grados escolares registrados.

        Args:
            order (Order, opcional): Especifica el modo de ordenamiento basado en el
            número de orden de un grado escolar, por defecto, se ordena del más bajo
            grado escolar al más alto.
            by_education_level_id (EducationLevel | int, opcional): Nivel educativo por
            el cual listar los grados escolares.

        Returns:
            Sequence[Grade]: Lista de grados escolares.
        """
        column_order = getattr(Grade.order, order.value)
        stmt = select(Grade).order_by(column_order())

        if by_education_level:
            educational_level_id = None
            if isinstance(by_education_level, EducationLevel):
                educational_level_id = by_education_level.id
            else:
                educational_level_id = by_education_level

            stmt = stmt.where(Grade.education_level_id == educational_level_id)

        return await funcs.get_all(self._db, Grade, stmt)

    async def exists_by_id(self, id: int) -> bool:
        """
        Devuelve True si el grado escolar con el ID dado existe en la base de datos.

        Args:
            id (int): ID del grado escolar a verificar.

        Returns:
            bool: Devuelve True si el grado escolar existe, de lo contrario False.
        """
        return await funcs.exists_by_id(self._db, Grade, id)
