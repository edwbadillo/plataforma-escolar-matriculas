from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.database.session import get_db

from .repository import AcademicYearRepository
from .service import AcademicYearService


def get_repository(db: AsyncSession = Depends(get_db)):
    return AcademicYearRepository(db)


def get_service(repository: AcademicYearRepository = Depends(get_repository)):
    return AcademicYearService(repository)
