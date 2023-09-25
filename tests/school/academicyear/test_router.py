from fastapi import status
from httpx import AsyncClient

from app.school.academicyear.models import AcademicYear
from app.school.academicyear.router import BASE_URL


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


# TODO: Test not found
