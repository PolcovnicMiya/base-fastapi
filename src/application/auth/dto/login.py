from dataclasses import dataclass


@dataclass(frozen=1, slots=1)
class CreateAccessAndRefreshTokenDTO:
    email: str
    password: str


@dataclass(frozen=1, slots=1)
class RefreshAccessTokenDTO:
    refresh_token: str
