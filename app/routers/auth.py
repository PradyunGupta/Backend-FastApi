from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import UserLogin
from ..import models, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm #returns username and password
from .. import schemas

router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    #if all fine create a token and return it
    access_token = oauth2.create_access_token(data = {"id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}


