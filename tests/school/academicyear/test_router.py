from datetime import date

from fastapi import status
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.responses import CommonResponse, ResourceCreatedResponse
from app.school.academicyear import messages
from app.school.academicyear.models import AcademicYear
from app.school.academicyear.router import BASE_URL
from tests.utils import check_resource_not_found_response


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
