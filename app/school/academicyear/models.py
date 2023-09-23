from datetime import date

from sqlalchemy import CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.common.database.models import Base, IntPK, TimestampsMixin


class AcademicYear(Base, TimestampsMixin):
    """
    Almacena los datos de un año escolar con el cual se hará referencia para las
    matrículas, periodos, cupos, etc.
    """

    __tablename__ = "academic_year"
    __table_args__ = (
        CheckConstraint("end_date > start_date", name="classes_dates"),
        CheckConstraint(
            "DATE_PART('year', start_date) = year", name="year_in_start_date"
        ),
        CheckConstraint("DATE_PART('year', end_date) = year", name="year_in_end_date"),
    )

    id: Mapped[IntPK]
    year: Mapped[int] = mapped_column(unique=True)
    start_date: Mapped[date]
    end_date: Mapped[date]
