from fastapi import FastAPI

from src.domain.auth.exception import AuthClientException, AuthServerException
from .auth import AuthExeptionHandler


def setup_app_exceptions(app: FastAPI) -> None:
    app.add_exception_handler(
        AuthClientException, 
        AuthExeptionHandler().auth_client_exeption_handler
    )
    app.add_exception_handler(
        AuthServerException, 
        AuthExeptionHandler().auth_server_exeption_handler
    )