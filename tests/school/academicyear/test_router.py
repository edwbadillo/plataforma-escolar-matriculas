from datetime import date

from fastapi import status
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.messages import FORM_ERROR
from app.common.responses import (
    CommonResponse,
    FormErrorResponse,
    ResourceCreatedResponse,
)
from app.school.academicyear import messages
from app.school.academicyear.models import AcademicYear
from app.school.academicyear.router import BASE_URL
from tests.faker import faker_db_func
from tests.utils import check_resource_not_found_response

from .faker import fake_academic_year


async def test_get_all(client: AsyncClient, academic_year):
    response = await client.get(f"{BASE_URL}")
    assert response.status_code == status.HTTP_200_OK

    assert response.json() == [
        {
            "id": academic_year.id,
            "year": academic_year.year,
            "start_date": str(academic_year.start_date),
            "end_date": str(academic_year.end_date),
        }
    ]


async def test_get_by_id(client: AsyncClient, academic_year: AcademicYear):
    response = await client.get(f"{BASE_URL}/{academic_year.id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": academic_year.id,
        "year": academic_year.year,
        "start_date": str(academic_year.start_date),
        "end_date": str(academic_year.end_date),
        "created_at": str(academic_year.created_at.isoformat()),
        "updated_at": None,
    }


async def test_get_by_id_not_found(client: AsyncClient):
    response = await client.get(f"{BASE_URL}/1")
    check_resource_not_found_response(response)


async def test_create(client: AsyncClient, db: AsyncSession):
    current_year = date.today().year
    form = {
        "year": 2023,
        "start_date": f"{current_year}-01-01",
        "end_date": f"{current_year}-12-31",
    }

    response = await client.post(f"{BASE_URL}", json=form)
    assert response.status_code == status.HTTP_201_CREATED

    academic_year_registered = (await db.scalars(select(AcademicYear))).first()

    expected_response = ResourceCreatedResponse(
        message=messages.CREATED, resource_id=academic_year_registered.id
    ).model_dump()

    assert response.json() == expected_response


async def test_create_with_year_already_exists(db: AsyncSession, client: AsyncClient):
    current_year = date.today().year
    await faker_db_func(
        db,
        fake_academic_year,
        year=current_year,
        start_date=date(current_year, 1, 1),
        end_date=date(current_year, 12, 31),
    )

    form = {
        "year": current_year,
        "start_date": f"{current_year}-01-01",
        "end_date": f"{current_year}-12-31",
    }

    response = await client.post(f"{BASE_URL}", json=form)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert (
        response.json()
        == FormErrorResponse(
            message=FORM_ERROR,
            errors=[
                {"field": "year", "message": messages.YEAR_EXISTS},
            ],
        ).model_dump()
    )


async def test_update(client: AsyncClient, academic_year: AcademicYear):
    next_year = date.today().year + 1
    form = {
        "year": next_year,
        "start_date": f"{next_year}-01-01",
        "end_date": f"{next_year}-12-31",
    }

    response = await client.put(f"{BASE_URL}/{academic_year.id}", json=form)
    assert response.status_code == status.HTTP_200_OK

    expected_response = CommonResponse(message=messages.UPDATED).model_dump()

    assert response.json() == expected_response
