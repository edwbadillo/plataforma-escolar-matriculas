import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.school.grade.models import Grade
from app.school.grade.repository import GradeRepository

from .faker import fake_grade


@pytest.fixture
def repository(db: AsyncSession):
    return GradeRepository(db, Grade)


async def test_list_grades(db: AsyncSession, repository: GradeRepository):
    """Lista todos los grados del colegio"""

    grades_in_db = await fake_grade(db, num_rows=5)

    grades_list = await repository.get_all()
    assert len(grades_list) == len(grades_in_db)

    first_grade = grades_list[0]
    assert first_grade.id == grades_in_db[0].id
    assert first_grade.name == grades_in_db[0].name
    assert first_grade.level == grades_in_db[0].level


@pytest.mark.parametrize(
    "id, exists",
    [
        (2, True),
        (345, False),
    ],
)
async def test_exists_by_id(
    db: AsyncSession, repository: GradeRepository, id: int, exists: bool
):
    """Verifica que existe el grado con el id dado"""
    await fake_grade(db, id=2)
    assert await repository.exists_by_id(id) == exists


async def test_count(db: AsyncSession, repository: GradeRepository):
    """Verifica que la cantidad de registros"""
    await fake_grade(db, num_rows=5)
    assert await repository.count() == 5
