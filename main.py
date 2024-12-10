from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
from src.presentation.controllers import setup_controllers
from src.presentation.exeptions import setup_app_exceptions
from src.infrastructure.db.postgres.help import create_tables, delete_tables
from src.composition import Container


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield
    # await delete_tables()

def create_app():

    app = FastAPI(lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    container = Container()
    
    setup_controllers(app, container)

    setup_app_exceptions(app)

    return app


if __name__ == '__main__':
    uvicorn.run(
        app='main:create_app',
        factory=True,
        host='127.0.0.1',
        port=8000,
        reload=True,
        workers=1
    )

