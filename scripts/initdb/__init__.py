from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.config import settings

from .grade import create_grades


def init_db():
    """
    Crea los registros de la base de datos de las tablas principales
    """
    engine = create_engine(settings.DATABASE_URL)
    with Session(engine) as session:
        print("Creating rows...")

        create_grades(session)

        session.commit()

        print("Rows created!")
