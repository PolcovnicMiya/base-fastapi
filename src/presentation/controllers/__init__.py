from fastapi import FastAPI

from src.presentation.controllers.auth import LoginUserController, RegisterUserController
from src.composition import Container


def setup_controllers(app:FastAPI, container: Container):
    app.include_router(RegisterUserController(container.register_user_service()).router)
    app.include_router(LoginUserController(container.login_user_service()).router)