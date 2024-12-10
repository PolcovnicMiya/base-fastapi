from typing import Dict
from fastapi.responses import JSONResponse
from fastapi import APIRouter, status
from src.application.auth.dto import SendRegisterCodeDTO, AcceptRegisterCodeDTO
from src.application.auth.interfaces import RegisterUserServiceInterface
from src.presentation.request.auth import (
    SendRegisterCodeRequest,
    AcceptRegisterCodeRequest,
)


class RegisterUserController:
    def __init__(self, service: RegisterUserServiceInterface):
        self.router = APIRouter(prefix="/api/v1/auth/register", tags=["Register"])
        self._service = service

        self._routes()

    def _routes(self) -> None:
        @self.router.post(path="/send-code")
        async def send_register_code_endpoint(
            request: SendRegisterCodeRequest,
        ) -> Dict[str, str]:
            await self._service.send_register_code(
                SendRegisterCodeDTO(email=request.email)
            )
            return JSONResponse(status_code=status.HTTP_200_OK,
                                content={
                                    "msg": "Code sent."
                                })

        @self.router.post(path="/accept-code")
        async def refresh_access_token_code_endpoint(
            request: AcceptRegisterCodeRequest,
        ) -> Dict[str, str]:
            await self._service.accept_register_code(
                AcceptRegisterCodeDTO(email=request.email,
                                      code=request.code,
                                      password=request.password)
            )
            return JSONResponse(status_code=status.HTTP_200_OK,
                                content={
                                    "msg": "User is verified."
                                })
        
