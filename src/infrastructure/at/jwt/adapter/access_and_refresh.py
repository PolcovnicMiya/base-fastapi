from datetime import datetime, timedelta, timezone
from typing import Any, Dict
from src.configuration import Environments
from src.infrastructure.at.jwt.ports import AccessAndRefreshJWTRepositoryPort
import jwt
import bcrypt


class AccessAndRefreshJWTRepositoryAdapter(AccessAndRefreshJWTRepositoryPort):

    async def encode_token(
        self, token_type: str, data: Dict[str, Any]
    ) -> str:
        to_encode = data.copy()
        now = datetime.now(timezone.utc)
        if token_type == "access":
            expire = now + timedelta(
                minutes=int(Environments().jwt_config.ACCESS_TOKEN_EXPIRE_IN_SECOND)
            )
        elif token_type == 'refresh':
            expire = now + timedelta(
                days=int(Environments().jwt_config.REFRESH_TOKEN_EXPIRE_IN_SECOND)
            )
        to_encode.update(
            {
                "exp": expire,
                "type": token_type,
            }
        )
        encode_jwt = jwt.encode(
            to_encode,
            Environments().jwt_config.PRIVATE_KEY_PATH.read_text(),
            algorithm=Environments().jwt_config.ALGORITHM,
        )
        return encode_jwt

    async def decode_token(self, token: str | bytes) -> Dict[str, Any]:
        decode = jwt.decode(
            token,
            Environments().jwt_config.PUBLIC_KEY_PATH.read_text(),
            algorithms=[Environments().jwt_config.ALGORITHM],
        )
        return decode
