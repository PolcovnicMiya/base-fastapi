from pydantic import BaseModel, EmailStr, StrictStr

class SendRegisterCodeRequest(BaseModel):
    email:EmailStr


class AcceptRegisterCodeRequest(BaseModel):
    code: StrictStr
    email: EmailStr
    password: StrictStr
    