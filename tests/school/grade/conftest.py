import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.school.grade.models import Grade


@pytest.fixture
async def grades(db: AsyncSession) -> list[Grade]:
    grades = [
        Grade(id=0, name="Prescolar", level="Prescolar"),
        Grade(id=1, name="Primero", level="Primero"),
        Grade(id=2, name="Segundo", level="Segundo"),
        Grade(id=3, name="Tercero", level="Tercero"),
    ]
    db.add_all(grades)
    await db.commit()
    for grade in grades:
        await db.refresh(grade)
    return grades
