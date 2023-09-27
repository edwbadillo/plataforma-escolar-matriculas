from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from ..responses import FormErrorResponse
from .exceptions import ExistsValueError
from .forms import FormErrorDetail


async def set_exception_handler(app: FastAPI):
    """
    Establece el manejador general de excepciones que pueden ocurrir en la aplicación
    """

    @app.exception_handler(ExistsValueError)
    async def exists_value_error_handler(request: Request, exc: ExistsValueError):
        """
        Normalmente este error es generado desde un servicio que realiza un registro
        desde un formulario.
        """
        form_error_response = FormErrorResponse(
            message="Error de formulario",
            errors=[
                FormErrorDetail(field=exc.field, message=exc.message),
            ],
        )
        return JSONResponse(status_code=422, content=form_error_response.model_dump())
