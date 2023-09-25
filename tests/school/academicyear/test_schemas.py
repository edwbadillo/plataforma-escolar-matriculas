from app.school.academicyear.models import AcademicYear
from app.school.academicyear.schemas import AcademicYearBasic, AcademicYearDetails


def test_basic_schema(academic_year: AcademicYear):
    schema = AcademicYearBasic.model_validate(academic_year)
    assert schema.id == academic_year.id
    assert schema.year == academic_year.year
    assert schema.start_date == academic_year.start_date
    assert schema.end_date == academic_year.end_date


def test_details_schema(academic_year: AcademicYear):
    schema = AcademicYearDetails.model_validate(academic_year)
    assert schema.id == academic_year.id
    assert schema.created_at == academic_year.created_at
    assert schema.updated_at == academic_year.updated_at
