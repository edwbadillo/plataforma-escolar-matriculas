from pydantic import BaseModel, ConfigDict


class GradeSchema(BaseModel):
    """
    Representación de los datos de un grado escolar.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    level: str
