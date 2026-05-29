from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    status
)

from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    UserResponse
)

from app.auth.auth_service import (
    register_user,
    authenticate_user
)

from app.auth.jwt_handler import (
    create_access_token
)

from app.auth.dependencies import (
    get_current_user
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
async def register(
    request: RegisterRequest
):
    try:

        user = await register_user(
            request.name,
            request.email.lower().strip(),
            request.password
        )

        return user

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post(
    "/login",
    response_model=TokenResponse
)
async def login(
    request: LoginRequest
):

    user = await authenticate_user(
        request.email.lower().strip(),
        request.password
    )

    if not user:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    access_token = create_access_token(
        user.id
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer"
    )


@router.get(
    "/me",
    response_model=UserResponse
)
async def me(
    current_user=Depends(
        get_current_user
    )
):
    return current_user