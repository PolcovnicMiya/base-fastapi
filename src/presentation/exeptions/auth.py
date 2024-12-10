from typing import Dict

from fastapi import HTTPException, Request
from src.domain.auth.exception import AuthServerException, AuthClientException


class AuthExeptionHandler:
    async def auth_client_exeption_handler(
        self,rrequest: Request, exception: AuthClientException
    ) -> Dict[str,str]:
        raise HTTPException(status_code=401, detail=exception.message)

    async def auth_server_exeption_handler(
        self,request: Request, exception: AuthServerException 
    ) -> Dict[str,str]:
        raise HTTPException(status_code=500, detail=exception.message)
