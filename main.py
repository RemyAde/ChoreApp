from fastapi import FastAPI
import models
from database import engine
from routers import admin, auth, chores, users, address

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(chores.router)
app.include_router(users.router)
app.include_router(address.router)