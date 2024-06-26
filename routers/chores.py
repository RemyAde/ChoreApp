from fastapi import APIRouter, Depends, status, HTTPException, Path
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from models import Chores
from pydantic import BaseModel, Field
from .auth import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class ChoresRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int =Field(gt=0, le=5)
    complete: bool = Field(default=False)


@router.get("/chores", status_code=status.HTTP_200_OK)
async def read_chores(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed.')
    chore_model = db.query(Chores).filter(Chores.owner_id == user.get('id')).all()
    return chore_model

@router.get("/chores/{chore_id}", status_code=status.HTTP_200_OK)
async def read_chore(user: user_dependency, db: db_dependency, chore_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed.')
    
    chore_model = db.query(Chores).filter(Chores.id == chore_id).filter(Chores.owner_id == user.get('id')).first()
    if chore_model is None:
        raise HTTPException(status_code=404, detail="Chore not found")
    
    return chore_model

@router.post("/chores/create", status_code=status.HTTP_201_CREATED)
async def create_chore(user: user_dependency, db: db_dependency, chores_request: ChoresRequest):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed.')
    
    chore_model = Chores(**chores_request.model_dump(), owner_id=user.get('id'))

    db.add(chore_model)
    db.commit()

@router.put("/chores/update/{chore_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_chore(user: user_dependency, db: db_dependency, chore_request: ChoresRequest, chore_id: int = Path(gt=0)):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed.')
    
    chore_model = db.query(Chores).filter(Chores.id == chore_id).filter(Chores.owner_id == user.get('id')).first()
    if chore_model is None:
        raise HTTPException(status_code=404, detail="Chore not found")
    
    chore_model.title = chore_request.title # type: ignore
    chore_model.description = chore_request.description # type: ignore
    chore_model.priority = chore_request.priority # type: ignore
    chore_model.complete = chore_request.complete # type: ignore

    db.add(chore_model)
    db.commit()

@router.delete("/chores/delete/{chore_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chore(user: user_dependency, db: db_dependency, chore_id: int = Path(gt=0)):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed.')
    
    chore_model = db.query(Chores).filter(Chores.id == chore_id).filter(Chores.owner_id == user.get('id')).first()

    if chore_model is None:
        raise HTTPException(status_code=404, detail="Chore not found")

    db.delete(chore_model)
    db.commit()
    