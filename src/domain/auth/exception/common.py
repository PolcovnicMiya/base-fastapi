from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AuthClientException(Exception):
    message: str


@dataclass(frozen=True, slots=True)
class AuthServerException(Exception):
    message: str
