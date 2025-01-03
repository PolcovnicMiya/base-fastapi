import bcrypt

from src.infrastructure.at.jwt.ports import HashingPasswordRepositoryPort


class HashingPasswordRepositoryAdapter(HashingPasswordRepositoryPort):
    async def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        pwd_bytes: bytes = password.encode()
        password = bcrypt.hashpw(pwd_bytes, salt)
        return password.decode("utf-8")
    
    async def validate_password(self, password: str, hashed_password: bytes) -> bool:
        return bcrypt.checkpw(
            password=password.encode(),
            hashed_password=hashed_password,
        )
