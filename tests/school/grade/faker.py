from sqlalchemy.ext.asyncio import AsyncSession

from app.school.grade.models import Grade
from tests.faker import fakeUS


async def fake_grade(db: AsyncSession, **kwargs) -> Grade:
    """
    Genera una instancia Grade con datos ficticios o especificados en kwargs.

    Args:
        db (AsyncSession): Conexión con la base de datos, útil en caso de interactuar
        con registros existentes.
        num_rows (int, opcional): Cantidad de registros a generar, por defecto 1.
        **kwargs (dict, opcional): Campos manualmente especificados para el modelo.

    Returns:
        Grade: Instancia del registro generado
    """
    return Grade(
        id=kwargs.get("id", fakeUS.random_int()),
        name=kwargs.get("name", " ".join(fakeUS.words(nb=2))),
        level=kwargs.get("level", fakeUS.word()),
    )
