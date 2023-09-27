from fastapi import APIRouter, FastAPI

from .common.errors import set_exceptions_handler
from .school.academicyear.router import router as academic_year_router

app = FastAPI()

main_router = APIRouter(prefix="/api")
main_router.include_router(academic_year_router)

app.include_router(main_router)


set_exceptions_handler(app)


@app.get("/")
def index():
    return {"message": "Hello World!"}
