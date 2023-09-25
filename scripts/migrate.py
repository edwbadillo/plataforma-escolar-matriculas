import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection, create_async_engine

from app.common.database.models import Base
from app.config import settings

# Importar todos los modelos SQLAlchemy
from app.school.academicyear.models import AcademicYear  # noqa
from app.school.grade.models import Grade  # noqa


async def __create_auto_updated_at_function(conn: AsyncConnection) -> None:
    """
    Crea una función que actualiza el campo updated_at de la tabla.
    """
    sql = """
        CREATE OR REPLACE FUNCTION update_updated_at()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = NOW();
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """
    await conn.execute(text(sql))


async def __create_base_functions(conn: AsyncConnection):
    """
    Crea funciones base de PostgreSQL requeridos para posteriores triggers
    """
    print("Creating database functions...")
    await __create_auto_updated_at_function(conn)
    print("Database functions created!")


async def __set_updated_at_trigger(conn: AsyncConnection, model: type[Base]) -> None:
    """
    Crea un trigger que actualiza el campo updated_at de la tabla al editar un registro.
    """
    sql = f"""
        CREATE OR REPLACE TRIGGER update_updated_at
        BEFORE UPDATE ON {model.__tablename__}
        FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at();
    """
    await conn.execute(text(sql))


async def __create_triggers(conn: AsyncConnection):
    """
    Crea los triggers a diferentes tablas creadas en la base de datos
    """
    print("Creating triggers...")
    await __set_updated_at_trigger(conn, AcademicYear)
    print("Triggers created!")


async def __create_tables(conn):
    """Crea las tablas de la base de datos"""
    print("Creating tables...")
    await conn.run_sync(Base.metadata.create_all)
    print("Tables created!")


async def __reset_db(conn: AsyncConnection):
    """
    Borra todas las tablas de la base de datos, funciones, triggers, etc.
    """
    print("Deleting tables...")
    await conn.run_sync(Base.metadata.drop_all)
    print("Tables deleted!")


async def migrate(reset_db: bool = False):
    """
    Crea la estructura de tablas de la base de datos, funciones y triggers necesarios
    en la base de datos.

    NOTA IMPORTANTE: Esto puede ser remplazado por el sistema de migraciones de alembic
    """
    engine = create_async_engine(settings.DATABASE_URL)
    async with engine.begin() as conn:
        if reset_db:
            await __reset_db(conn)

        await __create_base_functions(conn)
        await __create_tables(conn)
        await __create_triggers(conn)


if __name__ == "__main__":
    import sys

    reset_db = sys.argv[1] == "--reset"
    asyncio.run(migrate(reset_db))
