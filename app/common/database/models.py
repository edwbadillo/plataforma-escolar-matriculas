from datetime import datetime
from typing import Annotated

from sqlalchemy import MetaData, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# Tipo definido para un campo fecha que se especifica automáticamente por el motor
AutoTimestamp = Annotated[
    datetime, mapped_column(nullable=False, server_default=func.now())
]
IntPK = Annotated[int, mapped_column(primary_key=True)]


class Base(DeclarativeBase):
    """Todo modelo ORM de SQLAlchemy debe extender esta clase."""

    metadata = MetaData(
        # Se establece un estandar de nombres para el caso de PostgreSQL
        naming_convention={
            "ix": "%(column_0_label)s_idx",
            "uq": "%(table_name)s_%(column_0_name)s_key",
            "ck": "%(table_name)s_%(constraint_name)s_check",
            "fk": "%(table_name)s_%(column_0_name)s_fkey",
            "pk": "%(table_name)s_pkey",
        }
    )


class TimestampsMixin:
    """
    Mixin para agregar los campos created_at y updated_at que son establecidos
    automáticamente por el motor de base de datos directamente.

    Al usar PostgreSQL, es necesario ejecutar un script SQL para que el campo updated_at
    se actualice correctamente al editar un registro.
    """

    created_at: Mapped[AutoTimestamp]
    updated_at: Mapped[AutoTimestamp]
