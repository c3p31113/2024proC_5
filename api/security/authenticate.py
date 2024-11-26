from datetime import datetime, timedelta, timezone


from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jwt import decode, encode
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel

import databases.literals as databaseliterals
from databases.accessor import connect, selectFrom
from logging import getLogger

logger = getLogger("uvicorn.app")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/token")


def loadSecretKey(filepath: str = "config/secretKey.txt") -> str:
    try:
        with open(filepath, mode="r", encoding="utf-8") as file:
            text = file.read().rstrip("\n")
            if text == "":
                raise Exception("SECRET KEY IS EMPTY.")
            return text
    except FileNotFoundError:
        logger.critical("SECRET KEY FILE IS GONE.")
        exit(1)


SECRETKEY = loadSecretKey()
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120  # TODO デバッグ用数値

EXCEPTION_INCORRECT_USER_OR_PASS = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)
EXCEPTION_INACTIVE_USER = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Inactive user",
)


class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class TokenData(BaseModel):
    username: str | None = None


class Admin(BaseModel):
    ID: int
    username: str
    last_login_date: datetime
    disabled: bool = False


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
        columns=["ID", "name", "password", "last_login_date"],
        where=f"name = '{username}'",
        oneOnly=True,
    )
    logger.debug(f"get admin result : {admin}")
    db_connection.close()
    if admin is None:
        return None
    else:
        id = admin["ID"]
        username = admin["name"]
        password = admin["password"]
        lastlogin: datetime = admin["last_login_date"]
        return AdminInDB(
            ID=id,
            username=username,
            last_login_date=lastlogin,
            hashed_password=password,
        )


def authenticate_admin(
    username: str, password: str, log_password=False
) -> AdminInDB | None:
    admin = get_admin(username)
    if not admin:
        return None
    if log_password:
        logger.debug(password)
        logger.debug(admin.hashed_password)
    if not verify_password(password, admin.hashed_password):
        return None
    return admin


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
):
    forencode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    forencode.update({"exp": expire})
    encoded_jwt = encode(forencode, SECRETKEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    CREDENTIALS_EXCEPTION = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode(token, SECRETKEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise CREDENTIALS_EXCEPTION
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise CREDENTIALS_EXCEPTION
    if token_data.username is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="token was empty"
        )
    admin = get_admin(username=token_data.username)
    if admin is None:
        raise CREDENTIALS_EXCEPTION
    return admin


async def get_current_active_user(current_user: Admin = Depends(get_current_user)):
    if current_user.disabled:
        raise EXCEPTION_INACTIVE_USER
    return current_user
