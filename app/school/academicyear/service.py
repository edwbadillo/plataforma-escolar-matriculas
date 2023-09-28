from app.common.errors import ExistsValueError

from .messages import YEAR_EXISTS
from .models import AcademicYear
from .repository import AcademicYearRepository
from .schemas import AcademicYearForm


class AcademicYearService:
    """
    Define funciones para la gestión de los años escolares
    """

    def __init__(self, repository: AcademicYearRepository) -> None:
        """
        Constructor del servicio de años escolares.

        Args:
            repository (AcademicYearRepository): Repositorio de años escolares.
        """
        self._repository = repository

    async def get_all(self) -> list[AcademicYear]:
        """
        Devuelve todos los años escolares registrados.

        Returns:
            list[AcademicYear]: Lista de años escolares
        """
        return await self._repository.get_all()

    async def get_by_id(self, id: int) -> AcademicYear:
        """
        Devuelve los datos de un año escolar.

        Args:
            id (int): ID del año escolar, debe existir en la base de datos.

        Returns:
            AcademicYear: Registro de año escolar
        """
        return await self._repository.get_by_id(id)

    async def create(self, form: AcademicYearForm) -> int:
        """
        Crea un nuevo año escolar con los datos especificados.

        Args:
            form (AcademicYearForm): Datos del nuevo registro a crear.

        Returns:
            int: ID del nuevo registro

        Raises:
            ExistsValueError: Si el año escolar existe en la base de datos
        """
        if await self._repository.exists_by_year(form.year):
            raise ExistsValueError("year", YEAR_EXISTS)

        academic_year = AcademicYear(**form.model_dump())
        await self._repository.save(academic_year)
        return academic_year.id

    async def update(self, id: int, form: AcademicYearForm) -> None:
        """
        Actualiza los datos de un año escolar con los datos especificados.

        Args:
            id (int): ID del año escolar, debe existir en la base de datos.
            form (AcademicYearForm): Datos del nuevo registro a crear.

        Raises:
            ExistsValueError: Si el año escolar existe en la base de datos
        """
        academic_year = await self._repository.get_by_id(id)

        # No tiene sentido cambiar el año, solo actualiza las fechas.
        academic_year.start_date = form.start_date
        academic_year.end_date = form.end_date

        await self._repository.save(academic_year)
