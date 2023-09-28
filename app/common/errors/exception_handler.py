from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from .. import messages as common_messages
from ..responses import CommonResponse, FormErrorResponse
from .exceptions import ExistsValueError, ResourceNotFound
from .forms import FormErrorDetail


def set_exception_handler(app: FastAPI):
    """
    Establece el manejador general de excepciones que pueden ocurrir en la aplicación
    """

    @app.exception_handler(ExistsValueError)
    def exists_value_error_handler(request: Request, exc: ExistsValueError):
        """
        Normalmente este error es generado desde un servicio que realiza un registro
        desde un formulario.
        """
        form_error_response = FormErrorResponse(
            message=common_messages.FORM_ERROR,
            errors=[
                FormErrorDetail(field=exc.field, message=exc.message),
            ],
        )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=form_error_response.model_dump(),
        )

    @app.exception_handler(ResourceNotFound)
    def resource_not_found_handler(request: Request, exc):
        """
        Este error generalmente ocurre cuando un registro no existe en la base de
        datos, normalmente los repositorios generan este error.
        """
        content_response = CommonResponse(message=common_messages.RESOURCE_NOT_FOUND)

        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=content_response.model_dump(),
        )
