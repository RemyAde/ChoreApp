from fastapi import APIRouter, Depends, status, HTTPException, Path
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from models import Chores, Users
from pydantic import BaseModel, Field
from .auth import get_current_user
from .auth import bcrypt_context

router = APIRouter(
    prefix='/user',
    tags=['user']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class UserRequest(BaseModel):
    new_password: str = Field(min_length=4)
    confirm_password: str = Field(min_length=4)

@router.get("/", status_code=status.HTTP_200_OK)
async def get_user_data(user: user_dependency, db:db_dependency):

    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail='User not Found')
    
    return user_model

@router.put("/change_password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, user_request: UserRequest):

    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if user_model is None:
        raise HTTPException(status_code=404, detail="User not Found")
    
    if user_request.new_password != user_request.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords don't match")
    
    user_model.hashed_password = bcrypt_context.hash(user_request.new_password)

    db.add(user_model)
    db.commit()