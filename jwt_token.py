from jose import jwt, JWTError
from typing import Union
from datetime import timedelta, datetime
from schemas import TokenData
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from db_connections import get_db
from db_models import Users

SECRET_KEY="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUES = 30


def create_access_token(data: dict, expires_delta: Union[timedelta, None]=None):
    to_encode=data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        userId: int = payload.get("userId")
        userName: str = payload.get("userName")
        if userId is None and userName is None:
            raise credentials_exception
        token_data = TokenData(userId=userId,userName=userName)
    except JWTError:
        raise credentials_exception
    return token_data


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session= Depends(get_db)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials",
                                        headers={"WWW-Authenticate":"Bearer"},)
    jtoken=verify_token(token, credentials_exception=credentials_exception)
    user=db.query(Users).filter(Users.userId==jtoken.userId).first()
    return user
