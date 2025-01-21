import uvicorn

from fastapi import FastAPI, APIRouter


from src.settings.config import get_settings


router = APIRouter()


@router.get("/")
def index():
	return {"message": "Hello World!"}


def create_app() -> FastAPI:
	config = get_settings()

	app = FastAPI(
		title="Communet API",
		description="Communet API it's a application for communication between users",
		version="0.1.0",
		docs_url="/api/docs",
		debug=config.DEBUG,
		port=config.API_PORT,
	)

	app.include_router(router)

	return app
