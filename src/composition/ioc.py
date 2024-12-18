from dependency_injector import containers, providers


from src.application.auth.service.login import LoginUserService
from src.application.auth.service.register import RegisterUserService
from src.infrastructure.db.redis.adapter import (
    EmailCodeRedisRepositoryAdapter,
    EmailAttemptRedisRepositoryAdapter,
    JWTRedisRepositoryAdapter
)
from src.infrastructure.smtp.adapter import VerifyEmailSMTPRepositoryAdapter
from src.infrastructure.at.jwt.adapter import (
    AccessAndRefreshJWTRepositoryAdapter,
    HashingPasswordRepositoryAdapter,
)
from src.infrastructure.db.postgres.adapter import (
    RolePostgresRepositoryAdapter,
    UserRolePostgresRepositoryAdapter,
    UserPostgresRepositoryAdapter,
)


class Container(containers.DeclarativeContainer):
    # AT
    # ----------
    # JWT
    _access_and_refresh_jwt_repo = providers.Singleton(
        AccessAndRefreshJWTRepositoryAdapter
    )

    _hashing_password_repo = providers.Singleton(HashingPasswordRepositoryAdapter)

    # BD
    # ---------
    # Postgres

    _role_postgres_repo = providers.Singleton(RolePostgresRepositoryAdapter)

    _user_postgres_repo = providers.Singleton(UserPostgresRepositoryAdapter)

    _user_role_postgres_repo = providers.Singleton(UserRolePostgresRepositoryAdapter)

    # REDIS

    _email_code_redis_repo = providers.Singleton(EmailCodeRedisRepositoryAdapter)

    _email_attempt_redis_repo = providers.Singleton(EmailAttemptRedisRepositoryAdapter)

    _jwt_redis_repo = providers.Singleton(JWTRedisRepositoryAdapter)
    
    # SMTP

    _verify_email_smtp_repo = providers.Singleton(VerifyEmailSMTPRepositoryAdapter)

    #Service
    # ------
    # Auth
    
    register_user_service = providers.Factory(
        RegisterUserService, 
        _user_postgres_repo = _user_postgres_repo,
        _email_code_redis_repo = _email_code_redis_repo,
        _verify_email_smtp_repo = _verify_email_smtp_repo,
        _role_postgres_repo = _role_postgres_repo,
        _user_role_postgres_repo = _user_role_postgres_repo,
        _hashing_password_repo = _hashing_password_repo
    )

    login_user_service = providers.Factory(
        LoginUserService,
            _access_and_refresh_jwt_repo = _access_and_refresh_jwt_repo,
            _user_postgres_repo = _user_postgres_repo,
            _user_role_postgres_repo = _user_role_postgres_repo,
            _jwt_redis_repo = _jwt_redis_repo,
            _hashing_password_repo = _hashing_password_repo
        
    )