from pydantic import BaseModel


class GradeSchema(BaseModel):
    id: int
    name: str
    level: str

    class Config:
        orm_mode = True
