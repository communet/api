import uvicorn

from fastapi import FastAPI, APIRouter


router = APIRouter()


@router.get("/")
def index():
	return {"message": "Hello World!"}


def create_app() -> FastAPI:
	app = FastAPI()

	app.include_router(router)

	return app
