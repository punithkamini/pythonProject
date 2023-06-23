from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session

import hashing
import jwt_token
from db_connections import get_db
from db_models import Users
from schemas import User
from hashing import Hash
from schemas import Token
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

router=APIRouter(tags=['Authentication'])


@router.post("/token", response_model=Token)
def login(users: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user=db.query(Users).filter(Users.userName==users.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid credentials")
    if not Hash.verify_password(user.userPwd, users.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid password")
    access_token = jwt_token.create_access_token(data={"userId":user.userId,"userName":user.userName},
                                                 expires_delta=timedelta(jwt_token.ACCESS_TOKEN_EXPIRE_MINUES))
    return {"access_token": access_token, "token_type": "bearer"}
