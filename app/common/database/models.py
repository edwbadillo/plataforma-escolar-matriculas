from datetime import datetime
from typing import Annotated

from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# Tipo definido para un campo fecha que se especifica automáticamente por el motor
AutoTimestamp = Annotated[
    datetime, mapped_column(nullable=False, server_default=func.now())
]
IntPK = Annotated[int, mapped_column(primary_key=True)]


class Base(DeclarativeBase):
    """Todo modelo ORM de SQLAlchemy debe extender esta clase."""

    pass


class TimestampsMixin:
    """
    Mixin para agregar los campos created_at y updated_at que son establecidos
    automáticamente por el motor de base de datos directamente.

    Al usar PostgreSQL, es necesario ejecutar un script SQL para que el campo updated_at
    se actualice correctamente al editar un registro.
    """

    created_at: Mapped[AutoTimestamp]
    updated_at: Mapped[AutoTimestamp]
