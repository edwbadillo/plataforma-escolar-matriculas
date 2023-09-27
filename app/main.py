from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import JSONResponse

from .common.errors import ExistsValueError, FormErrorDetail
from .common.responses import FormErrorResponse
from .school.academicyear.router import router as academic_year_router

app = FastAPI()

main_router = APIRouter(prefix="/api")
main_router.include_router(academic_year_router)

app.include_router(main_router)


@app.get("/")
def index():
    return {"message": "Hello World!"}


@app.exception_handler(ExistsValueError)
async def exists_value_error_handler(request: Request, exc: ExistsValueError):
    # error = FormErrorDetail(field=exc.field, message=exc.message)
    form_error_response = FormErrorResponse(
        message="Error de formulario",
        errors=[FormErrorDetail(field=exc.field, message=exc.message)],
    )
    return JSONResponse(status_code=422, content=form_error_response.model_dump())
