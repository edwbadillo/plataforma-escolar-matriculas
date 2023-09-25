from .models import AcademicYear
from .repository import AcademicYearRepository


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
