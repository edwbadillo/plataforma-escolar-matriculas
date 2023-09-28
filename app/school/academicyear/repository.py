from typing import Sequence

from sqlalchemy import select

from app.common.database import funcs
from app.common.database.repository import DBRepository
from app.school.academicyear.models import AcademicYear

from .exceptions import AcademicYearNotFound


class AcademicYearRepository(DBRepository):
    """
    Implementación del repositorio de años escolares.
    """

    async def get_all(self) -> Sequence[AcademicYear]:
        """
        Lista todos los años escolares registrados.

        Returns:
            list[AcademicYear]: Lista de años escolares
        """
        stmt = select(AcademicYear).order_by(AcademicYear.year.desc())
        return await funcs.get_all(self._db, AcademicYear, stmt)

    async def get_by_id(self, id: int) -> AcademicYear:
        """
        Devuelve los datos de un año escolar.

        Args:
            id (int): ID del año escolar, debe existir en la base de datos.

        Raises:
            AcademicYearNotFound: El año escolar no existe en la base de datos.

        Returns:
            AcademicYear: Registro de año escolar.
        """
        academic_year = await funcs.get_by_id(self._db, AcademicYear, id)
        if not academic_year:
            raise AcademicYearNotFound
        return academic_year

    async def exists_by_id(self, id: int) -> bool:
        """
        Verifica si existe un registro con el ID dado.

        Args:
            id (int): ID del registro a verificar

        Returns:
            bool: Devuelve True si el registro existe, de lo contrario False.
        """
        return await funcs.exists_by_id(self._db, AcademicYear, id)

    async def exists_by_year(self, year: int, exclude_id: int = None) -> bool:
        """
        Verifica si existe un registro con el año dado.

        Args:
            year (int): Año escolar a verificar
            exclude_id (int, opcional): ID del registro a excluir.

        Returns:
            bool: Devuelve True si el registro existe, de lo contrario False.
        """
        stmt = select(AcademicYear.year).where(AcademicYear.year == year)
        if exclude_id:
            stmt = stmt.where(AcademicYear.id != exclude_id)
        result = await self._db.scalar(stmt)
        return result is not None

    async def save(self, academic_year: AcademicYear) -> AcademicYear:
        """
        Guarda el registro en la base de datos.

        Args:
            academic_year (AcademicYear): Registro a guardar.

        Returns:
            int: ID del registro guardado
        """
        return await funcs.save(self._db, academic_year)
