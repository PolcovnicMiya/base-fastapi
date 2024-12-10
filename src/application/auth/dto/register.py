from dataclasses import dataclass


@dataclass(frozen=1, slots=1)
class SendRegisterCodeDTO:
    email: str


@dataclass(frozen=1, slots=1)
class AcceptRegisterCodeDTO:
    email: str
    code: str
    password: str
