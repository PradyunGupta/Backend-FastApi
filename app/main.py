from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post , user , auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware



#models.Base.metadata.create_all(bind=engine)
# this is not needed anymore because we have alembic
app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# CRUD operations in fastapi
@app.get("/")
def root():
    return {"message": "hello World"}







