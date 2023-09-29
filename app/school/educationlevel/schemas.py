from pydantic import BaseModel, ConfigDict


class GradeSchema(BaseModel):
    """
    Representación de los datos de un grado escolar.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class EducationLevelSchema(BaseModel):
    """
    Representación de los datos de un nivel educativo.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    grades: list[GradeSchema]


class EducationLevelsInformation(BaseModel):
    """
    Muestra toda la información de los niveles educativos con sus respectivos grados.
    """

    education_levels: list[EducationLevelSchema]
