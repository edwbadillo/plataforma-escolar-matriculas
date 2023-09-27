from datetime import date

from pydantic import ValidationError

from app.common.errors import FormErrors
from app.school.academicyear import messages
from app.school.academicyear.models import AcademicYear
from app.school.academicyear.schemas import (
    AcademicYearBasic,
    AcademicYearDetails,
    AcademicYearForm,
)


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


def test_form_schema_is_valid():
    year = date.today().year
    schema = AcademicYearForm.model_validate(
        {
            "year": year,
            "start_date": f"{year}-01-01",
            "end_date": f"{year}-12-31",
        }
    )
    assert schema.year == year
    assert schema.start_date == date(year, 1, 1)
    assert schema.end_date == date(year, 12, 31)


def test_form_schema_invalid_year():
    year = date.today().year
    try:
        AcademicYearForm.model_validate(
            {
                "year": year - 1,
                "start_date": f"{year - 1}-01-01",
                "end_date": f"{year - 1}-12-31",
            }
        )
        assert False, "Should have raised an error"
    except ValidationError as e:
        errors = FormErrors(e)
        assert errors.total_errors == 1
        errors.check("year", message=messages.INVALID_YEAR, type_error="value_error")


def test_form_schema_validate_year_dates_not_in_year():
    year = date.today().year
    try:
        AcademicYearForm.model_validate(
            {
                "year": year,
                "start_date": f"{year - 1}-01-01",
                "end_date": f"{year - 1}-12-31",
            }
        )
        assert False, "Should have raised an error"
    except ValidationError as e:
        errors = FormErrors(e)
        assert errors.total_errors == 2
        errors.check(
            "start_date", message=messages.INVALID_START_DATE, type_error="value_error"
        )
        errors.check(
            "end_date", message=messages.INVALID_END_DATE, type_error="value_error"
        )


def test_form_schema_validate_end_date_after_start_date():
    year = date.today().year
    try:
        AcademicYearForm.model_validate(
            {
                "year": year,
                "start_date": f"{year}-06-01",
                "end_date": f"{year}-01-01",
            }
        )
        assert False, "Should have raised an error"
    except ValidationError as e:
        errors = FormErrors(e)
        assert errors.total_errors == 1
        errors.check(
            "end_date",
            message=messages.INVALID_END_DATE_BEFORE_START_DATE,
            type_error="value_error",
        )
