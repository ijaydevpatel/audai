from collections.abc import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlmodel import Session, SQLModel, create_engine

from ..core.config import settings
from ..models.user import User

engine = create_engine(settings.database_url, echo=False, pool_pre_ping=True)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.api_v1_prefix}/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        subject: str | None = payload.get("sub")
        if subject is None:
            raise credentials_exception
    except JWTError as exc:  # pragma: no cover
        raise credentials_exception from exc

    user = session.get(User, int(subject))
    if user is None:
        raise credentials_exception
    return user


def init_db() -> None:
    SQLModel.metadata.create_all(engine)
