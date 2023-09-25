from datetime import date

from pydantic import BaseModel, ConfigDict

from app.common.schemas import TimestampsMixinSchema


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
