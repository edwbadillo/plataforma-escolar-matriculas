from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from app.school.academicyear.models import AcademicYear
from tests.faker import fakeUS


async def fake_academic_year(
    db: AsyncSession, *, num_rows: int = 1, **kwargs
) -> list[AcademicYear]:
    """
    Genera registros del modelo AcademicYear con datos ficticios o especificados en
    kwargs.

    Tenga en cuenta las restricciones definidas en el modelo.

    Args:
        db (AsyncSession): Conexión con la base de datos.
        num_rows (int, opcional): Cantidad de registros a generar, por defecto 1.
        **kwargs (dict, opcional): Campos manualmente especificados para el modelo.

    Returns:
        list[AcademicYear]: Lista de registros generados
    """
    academic_years = []
    for _ in range(num_rows):
        year = kwargs.get("year", fakeUS.random_int(min=1950, max=2050))
        start_date = kwargs.get("start_date", date(year, 1, 1))
        end_date = kwargs.get("end_date", date(year, 12, 31))

        academic_years.append(
            AcademicYear(
                year=year,
                start_date=start_date,
                end_date=end_date,
            )
        )
    db.add_all(academic_years)
    await db.commit()
    for academic_year in academic_years:
        await db.refresh(academic_year)
    return academic_years
