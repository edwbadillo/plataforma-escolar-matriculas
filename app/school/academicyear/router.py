from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.common.responses import RESPONSE_404, CommonResponse, ResourceCreatedResponse

from .depends import get_service
from .messages import CREATED, UPDATED
from .schemas import AcademicYearBasic, AcademicYearDetails, AcademicYearForm
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


@router.post("", status_code=status.HTTP_201_CREATED)
async def create(form: AcademicYearForm, service: Service) -> ResourceCreatedResponse:
    """
    Crea un nuevo año escolar.
    """
    id = await service.create(form)
    return ResourceCreatedResponse(message=CREATED, resource_id=id)


@router.put("/{id}", responses=RESPONSE_404)
async def update(id: int, form: AcademicYearForm, service: Service) -> CommonResponse:
    """
    Actualiza los datos de un año escolar con los datos especificados.
    """
    await service.update(id, form)
    return CommonResponse(message=UPDATED)
