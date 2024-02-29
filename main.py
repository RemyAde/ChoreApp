from fastapi import FastAPI, Depends
import models
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from models import Chores
from pydantic import BaseModel, Field

app = FastAPI()


class ChoresRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int =Field(gt=0, le=5)
    complete: bool = Field(default=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/chores")
async def read_chores(db: db_dependency):
    chores_model = db.query(Chores).all()
    return chores_model

@app.get("/chores/{chore_id}")
async def read_chore(db: db_dependency, chore_id: int):
    chore_model = db.query(Chores).filter(Chores.id == chore_id).first()
    return chore_model

@app.post("/chores/create")
async def create_chore(db: db_dependency, chores_request: ChoresRequest):
    chores_model = Chores(**chores_request.model_dump())

    db.add(chores_model)
    db.commit()

@app.put("/chores/update/{chore_id}")
async def update_chore(db: db_dependency, chore_request: ChoresRequest, chore_id: int):
    chore_model = db.query(Chores).filter(Chores.id == chore_id).first()

    chore_model.title = chore_request.title
    chore_model.description = chore_request.description
    chore_model.priority = chore_request.priority
    chore_model.complete = chore_request.complete

    db.add(chore_model)
    db.commit()

@app.delete("/chores/delete/{chore_id}")
async def delete_chore(db: db_dependency, chore_id: int):
    chores_model = db.query(Chores).filter(Chores.id == chore_id).first()

    db.delete(chores_model)
    db.commit()


models.Base.metadata.create_all(bind=engine)