
from pydantic import BaseModel, EmailStr, StrictStr


class CreateAccessAndRefreshTokenRequest(BaseModel):
    email: EmailStr
    password: StrictStr

class RefreshAccessTolenRequest(BaseModel):
    refresh_token:str 