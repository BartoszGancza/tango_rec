from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette import status

from app.schemas.entities import UserSchema
from app.services.auth import AuthService
from config.database import get_db

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def decode_token(token):
    db = next(get_db())
    return await AuthService(db=db).get_user_by_token(username=token)


async def get_user(token: oauth2_scheme = Depends()):
    user = await decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: get_db = Depends()
):
    user = await AuthService(db=db).get_user(form_data)

    return {"access_token": user.username, "token_type": "bearer"}


@router.get("/me", response_model=UserSchema)
async def read_me(user: get_user = Depends()):
    return user
