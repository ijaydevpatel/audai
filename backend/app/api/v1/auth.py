from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from ...core.security import create_access_token, get_password_hash, verify_password
from ...models.user import User
from ...schemas.auth import Token, UserCreate, UserRead
from ..deps import get_current_user, get_session

router = APIRouter()


@router.post("/signup", response_model=Token)
def signup(user_in: UserCreate, session: Session = Depends(get_session)) -> Token:
    if session.exec(select(User).where(User.email == user_in.email)).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(email=user_in.email, hashed_password=get_password_hash(user_in.password))
    session.add(user)
    session.commit()
    session.refresh(user)

    access_token = create_access_token(str(user.id))
    refresh_token = create_access_token(str(user.id), expires_delta=timedelta(days=30))
    return Token(access_token=access_token, refresh_token=refresh_token)


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)) -> Token:
    user = session.exec(select(User).where(User.email == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(str(user.id))
    refresh_token = create_access_token(str(user.id), expires_delta=timedelta(days=30))
    return Token(access_token=access_token, refresh_token=refresh_token)


@router.get("/me", response_model=UserRead)
def read_me(current_user: User = Depends(get_current_user)) -> User:
    return current_user
