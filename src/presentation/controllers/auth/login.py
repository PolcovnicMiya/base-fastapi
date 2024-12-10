from typing import Dict
from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from src.application.auth.dto import (
    CreateAccessAndRefreshTokenDTO,
    RefreshAccessTokenDTO,
)
from src.application.auth.interfaces import LoginUserServiceInterface
from src.presentation.request.auth import (
    RefreshAccessTolenRequest,
    CreateAccessAndRefreshTokenRequest,
)


class LoginUserController:
    def __init__(self, service: LoginUserServiceInterface):
        self.router = APIRouter(prefix="/api/v1/auth/login", tags=["Login"])
        self._service = service
        self._routes()

    def _routes(self) -> None:
        @self.router.post(path="/swagger")
        async def create_access_and_refresh_token_from_swagger(
            request: OAuth2PasswordRequestForm = Depends(),
        ) -> Dict[str, str]:
            result = await self._service.create_access_and_refresh_token(
                CreateAccessAndRefreshTokenDTO(
                    email=request.username, password=request.password
                )
            )
            return JSONResponse(status_code=status.HTTP_200_OK, content=result)

        @self.router.post(path="/login")
        async def create_access_and_refresh_token_from_endpoint(
            request: CreateAccessAndRefreshTokenRequest,
        ) -> Dict[str, str]:
            result = await self._service.create_access_and_refresh_token(
                CreateAccessAndRefreshTokenDTO(
                    email=request.email, password=request.password
                )
            )
            return JSONResponse(status_code=status.HTTP_200_OK, content=result)

        @self.router.post(path="/refresh")
        async def refresh_access_token_endpoint(
            request: RefreshAccessTolenRequest = Query(...),
        ) -> Dict[str, str]:
            result = await self._service.refresh_access_token(
                RefreshAccessTokenDTO(refresh_token=request.refresh_token)
            )
            return JSONResponse(status_code=status.HTTP_200_OK, content=result)
