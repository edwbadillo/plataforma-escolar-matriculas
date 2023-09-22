from sqlalchemy.ext.asyncio import AsyncSession

from app.school.grade.models import Grade
from tests.faker import fakeUS


async def fake_grade(db: AsyncSession, *, num_rows: int = 1, **kwargs) -> list[Grade]:
    """
    Genera registros del modelo Grade con datos ficticios o especificados en kwargs.

    Args:
        db (AsyncSession): Conexión con la base de datos.
        num_rows (int, opcional): Cantidad de registros a generar, por defecto 1.
        **kwargs (dict, opcional): Campos manualmente especificados para el modelo.

    Returns:
        list[Grade]: Lista de registros generados
    """
    grades = []
    for _ in range(num_rows):
        grades.append(
            Grade(
                id=kwargs.get("id", fakeUS.random_int()),
                name=kwargs.get("name", fakeUS.words(nb=1)),
                level=kwargs.get("level", fakeUS.word()),
            )
        )
    db.add_all(grades)
    await db.commit()
    for grade in grades:
        await db.refresh(grade)
    return grades
