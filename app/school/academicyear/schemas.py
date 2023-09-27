from datetime import date

from pydantic import BaseModel, ConfigDict, FieldValidationInfo, field_validator

from app.common.schemas import TimestampsMixinSchema

from . import messages


class AcademicYearBasic(BaseModel):
    """
    Información básica de un año escolar registrado.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    year: int
    start_date: date
    end_date: date


class AcademicYearDetails(TimestampsMixinSchema, AcademicYearBasic):
    """
    Información detallada de un año escolar registrado.
    """

    pass


class AcademicYearForm(BaseModel):
    """
    Formulario para registrar/editar un registro de año escolar.
    """

    year: int
    start_date: date
    end_date: date

    @field_validator("year")
    @classmethod
    def validate_year(cls, value: int) -> int:
        current_year = date.today().year
        if not (current_year <= value <= (current_year + 1)):
            raise ValueError(messages.INVALID_YEAR)
        return value

    @field_validator("start_date")
    @classmethod
    def validate_start_date(
        cls, start_date: date, validation_info: FieldValidationInfo
    ) -> date:
        year = validation_info.data.get("year")
        if year and start_date.year != year:
            raise ValueError(messages.INVALID_START_DATE)
        return start_date

    @field_validator("end_date")
    @classmethod
    def validate_end_date(
        cls, end_date: date, validation_info: FieldValidationInfo
    ) -> date:
        year = validation_info.data.get("year")
        if year and end_date.year != year:
            raise ValueError(messages.INVALID_END_DATE)

        start_date = validation_info.data.get("start_date")
        if start_date and end_date < start_date:
            raise ValueError(messages.INVALID_END_DATE_BEFORE_START_DATE)

        return end_date
