from fastapi import FastAPI

from src.application.api.auth.handlers import router as auth_router
from src.application.api.channels.handlers import router as channel_router
from src.settings.config import settings


def create_app() -> FastAPI:
	app = FastAPI(
		title="Communet API",
		description="Communet API it's a application for communication between users",
		version="0.1.0",
		docs_url="/api/docs",
		debug=settings().DEBUG,
		port=settings().API_PORT,
	)

	app.include_router(router=auth_router, prefix="/api/v1")
	app.include_router(router=channel_router, prefix="/api/v1")

	return app
