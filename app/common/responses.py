from fastapi import status
from pydantic import BaseModel


class CommonResponseMessage(BaseModel):
    """Un esquema para cualquier mensaje de respuesta."""

    message: str


RESPONSE_404 = {
    status.HTTP_404_NOT_FOUND: {
        "description": "Recurso no encontrado.",
        "model": CommonResponseMessage,
    }
}
