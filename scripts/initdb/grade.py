from sqlalchemy.ext.asyncio import AsyncSession

from app.school.educationlevel.models import Grade


def create_grades(session: AsyncSession):
    print("Creating grades...")
    session.add_all(
        [
            Grade(id=0, name="PRESCOLAR", level="PREESCOLAR"),
            Grade(id=1, name="PRIMERO", level="PRIMARIA"),
            Grade(id=2, name="SEGUNDO", level="PRIMARIA"),
            Grade(id=3, name="TERCERO", level="PRIMARIA"),
            Grade(id=4, name="CUARTO", level="PRIMARIA"),
            Grade(id=5, name="QUINTO", level="PRIMARIA"),
            Grade(id=6, name="SEXTO", level="BASICA SECUNDARIA"),
            Grade(id=7, name="SEPTIMO", level="BASICA SECUNDARIA"),
            Grade(id=8, name="OCTAVO", level="BASICA SECUNDARIA"),
            Grade(id=9, name="NOVENO", level="BASICA SECUNDARIA"),
            Grade(id=10, name="DECIMO", level="SECUNDARIA MEDIA"),
            Grade(id=11, name="UNDECIMO", level="SECUNDARIA MEDIA"),
        ]
    )
