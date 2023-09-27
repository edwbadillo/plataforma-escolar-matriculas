from fastapi import status
from pydantic import BaseModel

from .errors import FormErrorDetail


class CommonResponse(BaseModel):
    """Un esquema para cualquier mensaje de respuesta."""

    message: str
    """Un mensaje descriptivo para cualquier respuesta"""


class FormErrorResponse(CommonResponse):
    """Un esquema para errores de formulario."""

    errors: list[FormErrorDetail]
    """Lista de errores de formulario."""


class ResourceCreatedResponse(CommonResponse):
    """Un esquema para recursos creados."""

    resource_id: int
    """ID del recurso creado"""


RESPONSE_404 = {
    status.HTTP_404_NOT_FOUND: {
        "description": "Recurso no encontrado.",
        "model": CommonResponse,
    }
}
