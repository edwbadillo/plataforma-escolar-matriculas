from typing import Annotated

from fastapi import APIRouter, Depends

from app.common.responses import RESPONSE_404

from .depends import get_service
from .schemas import AcademicYearBasic, AcademicYearDetails
from .service import AcademicYearService

BASE_URL = "/años-escolares"

router = APIRouter(prefix=BASE_URL, tags=["Años escolares"])

Service = Annotated[AcademicYearService, Depends(get_service)]


@router.get("")
async def get_all(service: Service) -> list[AcademicYearBasic]:
    """
    Trae todos los años escolares registrados ordenados por el mas reciente al mas
    antiguo.
    """
    return await service.get_all()


@router.get("/{id}", responses=RESPONSE_404)
async def get_by_id(id: int, service: Service) -> AcademicYearDetails:
    """
    Trae los datos de un año escolar por su ID.
    """
    return await service.get_by_id(id)
