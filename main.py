import uvicorn

from fastapi import FastAPI, APIRouter


from src.settings.config import get_settings

from fastapi import Depends, FastAPI, APIRouter
from src.settings.config import settings

router = APIRouter()


@router.get("/")
def index():
	return {"message": "Hello World!"}


def create_app() -> FastAPI:
	app = FastAPI(
		title="Communet API",
		description="Communet API it's a application for communication between users",
		version="0.1.0",
		docs_url="/api/docs",
		debug=settings().DEBUG,
		port=settings().API_PORT,
	)

	app.include_router(router)

	return app
