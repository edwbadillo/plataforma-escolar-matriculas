from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.database.models import Base, IntPK


class EducationLevel(Base):
    """
    Nivel educativo definido por el sistema educativo (primaria, secundaria, etc.), cada
    nivel tiene un conjunto de grados.
    """

    __tablename__ = "education_level"

    id: Mapped[IntPK]
    """ID del nivel educativo"""
    name: Mapped[str] = mapped_column(String(50), unique=True)
    """Nombre del nivel educativo."""
    order: Mapped[int] = mapped_column(unique=True)
    """Un número que indica el orden o nivel de un nivel educativo con el fin de ordenar
    y determinar qué nivel educativo es superior o inferior a otro."""

    # Relaciones - ORM
    grades: Mapped[list["Grade"]] = relationship(back_populates="education_level")
    """Lista de grados del nivel educativo."""


class Grade(Base):
    """
    Grado escolar académico definido por el sistema educativo (prescolar, primero,
    segundo, tercero, etc.), pertenece a un nivel educativo.
    """

    __tablename__ = "grade"

    id: Mapped[IntPK]
    """ID del grado escolar"""

    name: Mapped[str] = mapped_column(String(50), unique=True)
    """Nombre del grado escolar."""

    order: Mapped[int] = mapped_column(unique=True)
    """Un número que indica el orden o nivel de un grado con el fin de ordenar y
    determinar qué grado es superior o inferior a otro. El número de orden debe
    contener al principio el número de orden del nivel educativo."""

    # Llaves foráneas
    education_level_id: Mapped[IntPK] = mapped_column(ForeignKey("education_level.id"))
    """ID del nivel educativo al que pertenece el grado escolar."""

    # Relaciones - ORM
    education_level: Mapped["EducationLevel"] = relationship(back_populates="grades")
    """Instancia del nivel educativo al que pertenece el grado escolar."""
