from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from db_connections import get_db
from db_models import Users
from schemas import User
from hashing import Hash

router=APIRouter(tags=['Users'])


@router.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    return db.query(Users).all()


@router.post("/users", status_code=status.HTTP_201_CREATED)
def create_new_user(user: User, db: Session = Depends(get_db)):
    new_user=Users(userId=user.userId,userName=user.userName, userPwd=Hash.bcrypt(user.userPwd))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/users/{userId}")
def get_single_task(userId:int, db: Session = Depends(get_db)):
    user= db.query(Users).filter(Users.userId==userId)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {userId} not found")
    return user.first()
