from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.common.database.models import Base


class Grade(Base):
    """
    Grado escolar académico definido por el sistema educativo (prescolar, primero,
    segundo, tercero, etc.)
    """

    __tablename__ = "grade"

    # Grado escolar (0-11)
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)

    # Nombre del grado, legible para el usuario, usado para reportes o interfaz
    name: Mapped[str] = mapped_column(String(30), unique=True)

    # Nivel educativo (primaria, secundaria, etc.)
    level: Mapped[str] = mapped_column(String(30))
