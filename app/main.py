from fastapi import FastAPI

from .school.academicyear.router import router as academic_year_router

app = FastAPI()

app.include_router(academic_year_router)


@app.get("/")
def index():
    return {"message": "Hello World!"}
