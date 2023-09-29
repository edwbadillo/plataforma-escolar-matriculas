from sqlalchemy.ext.asyncio import AsyncSession

from app.school.educationlevel.models import EducationLevel, Grade
from tests.faker import fakeUS


async def fake_education_level(db: AsyncSession, **kwargs) -> EducationLevel:
    """
    Genera una instancia EducationLevel con datos ficticios o especificados en kwargs.

    Args:
        db (AsyncSession): Conexión con la base de datos, útil en caso de interactuar
        con registros existentes.
        **kwargs (dict, opcional): Campos manualmente especificados para el modelo.

    Returns:
        EducationLevel: Instancia del registro generado
    """
    return EducationLevel(
        id=kwargs.get("id", fakeUS.random_int()),
        name=kwargs.get("name", " ".join(fakeUS.words(nb=2))),
        order=kwargs.get("order", fakeUS.random_int()),
    )


async def fake_grade(db: AsyncSession, **kwargs) -> Grade:
    """
    Genera una instancia Grade con datos ficticios o especificados en kwargs.

    Args:
        db (AsyncSession): Conexión con la base de datos, útil en caso de interactuar
        con registros existentes.
        **kwargs (dict, opcional): Campos manualmente especificados para el modelo.

    Returns:
        Grade: Instancia del registro generado
    """

    return Grade(
        id=kwargs.pop("id", fakeUS.random_int()),
        name=kwargs.pop("name", " ".join(fakeUS.words(nb=2))),
        order=kwargs.pop("order", fakeUS.random_int()),
        **kwargs,
    )
