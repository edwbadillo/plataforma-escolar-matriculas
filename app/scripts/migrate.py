from sqlalchemy import create_engine

from app.common.database.models import Base
from app.config import settings


def migrate():
    from app.schoolconfig.grade.models import Grade  # noqa

    print("Creating tables...")

    engine = create_engine(settings.DATABASE_URL)
    Base.metadata.create_all(engine)

    print("Tables created!")
