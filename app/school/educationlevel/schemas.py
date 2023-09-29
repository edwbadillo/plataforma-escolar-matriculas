from pydantic import BaseModel, ConfigDict


class EducationLevelSchema(BaseModel):
    """
    Representación de los datos de un nivel educativo.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class GradeSchema(BaseModel):
    """
    Representación de los datos de un grado escolar.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
