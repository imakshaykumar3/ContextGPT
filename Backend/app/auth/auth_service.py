#app/auth/auth_service.py
import logging

from sqlalchemy import select

from app.db.database import (
    AsyncSessionLocal
)

from app.db.models import (
    User
)

from app.auth.password import (

    hash_password,

    verify_password
)

logger = logging.getLogger(__name__)


async def register_user(

    name: str,

    email: str,

    password: str
):

    async with AsyncSessionLocal() as db:

        existing = await db.execute(

            select(User).where(
                User.email == email
            )
        )

        user = (
            existing.scalar_one_or_none()
        )

        if user:

            raise Exception(
                "Email already registered"
            )

        new_user = User(

            name=name,

            email=email,

            hashed_password=(
                hash_password(
                    password
                )
            )
        )

        db.add(new_user)

        await db.commit()

        await db.refresh(
            new_user
        )

        return new_user


async def authenticate_user(

    email: str,

    password: str
):

    async with AsyncSessionLocal() as db:

        result = await db.execute(

            select(User).where(
                User.email == email
            )
        )

        user = (
            result.scalar_one_or_none()
        )

        if not user:

            return None

        if not verify_password(

            password,

            user.hashed_password
        ):

            return None

        return user