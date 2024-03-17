import sys 
sys.path.append('..')

from typing import Optional
from fastapi import Depends, APIRouter
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .auth import get_current_user, get_user_exception

router = APIRouter(
    prefix="/address",
    tags=["address"],
    responses={404: {'description': 'Not Found'}}
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Address(BaseModel):
    address1: str
    address2: Optional[str]
    city: str
    state: str
    country: str
    postalcode: str
    apt_num: Optional[int]


@router.post("/")
async def create_address(address: Address, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    
    if user is None:
        raise get_user_exception()
    address_model = models.Address(**address.model_dump())

    db.add(address_model)
    db.flush()
    
    user_model = db.query(models.Users).filter(models.Users.id == user.get('id')).first()
    user_model.address_id = address_model.id

    db.add(user_model)

    db.commit()
