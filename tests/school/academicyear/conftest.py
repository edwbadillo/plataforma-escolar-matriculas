import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.school.academicyear.models import AcademicYear
from app.school.academicyear.repository import AcademicYearRepository


@pytest.fixture
def repository(db: AsyncSession):
    return AcademicYearRepository(db, AcademicYear)
