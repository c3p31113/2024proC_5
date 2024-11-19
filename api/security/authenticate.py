from datetime import datetime, timedelta, timezone


from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jwt import decode, encode
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel

import databases.literals as databaseliterals
from databases.accessor import connect, selectFrom
from logging import getLogger

logger = getLogger("uvicorn.app")
pwd_context = CryptContext(scheme=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/authenticate/token")


def loadSecretKey(filepath: str) -> str:
    try:
        with open(filepath, mode="r", encoding="utf-8") as file:
            text = file.read()
            if text == "":
                raise Exception("SECRET KEY IS EMPTY.")
            return text
    except FileNotFoundError:
        logger.critical("SECRET KEY FILE IS GONE.")
        exit(1)


SECRETKEY = loadSecretKey("config/secretKey.text")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1  # TODO デバッグ用数値

HTTPERROR_INCORRECT_USER_OR_PASS = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)
HTTPERROR_INACTIVE_USER = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Inactive user",
)


class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class Admin(BaseModel):
    ID: int
    username: str
    last_login_date: datetime


class AdminInDB(Admin):
    hashed_password: str


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_admin(username: str) -> AdminInDB | None:
    db_connection = connect()
    admin = selectFrom(
        connection=db_connection,
        table=databaseliterals.DATABASE_TABLE_ADMINS,
        columns="*",
        where=f"USERNAME = {username}",
        oneOnly=True,
    )
    db_connection.close()
    if admin is None:
        return None
    else:
        id = admin["ID"]
        username = admin["name"]
        password = admin["password"]
        lastlogin = admin["lastlogin"]
        return AdminInDB(
            ID=id,
            username=username,
            last_login_date=lastlogin,
            hashed_password=password,
        )


def authenticate_admin(username: str, password: str) -> AdminInDB | None:
    admin = get_admin(username)
    if not admin:
        return None
    if not verify_password(password, admin.hashed_password):
        return None
    return admin
