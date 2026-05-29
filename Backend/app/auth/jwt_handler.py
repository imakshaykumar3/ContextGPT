#app/auth/jwt_handler.py
from datetime import (
    datetime,
    timedelta,
    timezone
)

from jose import jwt

from app.config.settings import (

    JWT_SECRET_KEY,

    JWT_ALGORITHM,

    ACCESS_TOKEN_EXPIRE_MINUTES
)


def create_access_token(
    user_id: int
) -> str:

    expire = (

        datetime.now(
            timezone.utc
        )

        + timedelta(
            minutes=(
                ACCESS_TOKEN_EXPIRE_MINUTES
            )
        )
    )

    payload = {

        "sub": str(user_id),

        "exp": expire
    }

    return jwt.encode(

        payload,

        JWT_SECRET_KEY,

        algorithm=JWT_ALGORITHM
    )


def decode_token(
    token: str
):

    return jwt.decode(

        token,

        JWT_SECRET_KEY,

        algorithms=[
            JWT_ALGORITHM
        ]
    )