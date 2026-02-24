from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.database import get_db
from sqlalchemy.orm import Session
from app.schemas.user import Token
from app.models.user import User
from app.utils.hashing import Hash
from app.utils.oauth2 import create_access_token

router = APIRouter(
    tags=['Authentication']
)

@router.post("/login", status_code=status.HTTP_202_ACCEPTED, response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == user_credentials.username).first()

    # For login failures (wrong email or wrong password), 401 Unauthorized is the standard status code.
    # Using 404 is optional only if you want to hide whether the user exists, but 401 is still the correct semantic choice.
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not Hash.verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    # Creates a JWT Token
    access_token = create_access_token(data= {"user_id": user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}

