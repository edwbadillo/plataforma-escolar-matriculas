from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from app.school.academicyear.models import AcademicYear
from tests.faker import fakeUS


async def fake_academic_year(db: AsyncSession, **kwargs) -> AcademicYear:
    """
    Genera registros del modelo AcademicYear con datos ficticios o especificados en
    kwargs.

    Tenga en cuenta las restricciones definidas en el modelo.

    Args:
        db (AsyncSession): Conexión con la base de datos, util para interactuar con
        registros existentes.

    Returns:
        AcademicYear
    """
    year = kwargs.get("year", fakeUS.random_int(min=1950, max=2050))
    start_date = kwargs.get("start_date", date(year, 1, 1))
    end_date = kwargs.get("end_date", date(year, 12, 31))

    return AcademicYear(
        year=year,
        start_date=start_date,
        end_date=end_date,
    )
