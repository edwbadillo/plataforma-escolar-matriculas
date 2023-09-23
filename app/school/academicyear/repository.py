from sqlalchemy import select

from app.common.database.repository import BaseRepository, SaveMixin
from app.school.academicyear.models import AcademicYear


class AcademicYearRepository(BaseRepository[AcademicYear], SaveMixin[AcademicYear]):
    """
    Repositorio de los años escolares registrados por la institución.
    """

    async def get_all(self) -> list[AcademicYear]:
        """
        Devuelve todos los años escolares registrados ordenados por el mas reciente al
        mas antiguo.
        """
        stmt = select(AcademicYear).order_by(AcademicYear.year.desc())
        scalar_result = await self._db.scalars(stmt)
        return scalar_result.all()

    async def exists_by_year(self, year: int) -> bool:
        """
        Verifica si existe un registro con el año dado.

        Args:
            year (int): Año escolar a verificar

        Returns:
            bool: Devuelve True si el registro existe, False si no
        """
        stmt = select(AcademicYear.year).where(AcademicYear.year == year)
        result = await self._db.scalar(stmt)
        return result is not None
