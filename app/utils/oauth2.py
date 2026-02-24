from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.config.settings import settings
from app.schemas.user import TokenData
from app.models.user import User
from app.database import get_db
from jose import jwt, JWTError
from datetime import datetime, timezone, timedelta


oauth2scheme = OAuth2PasswordBearer(tokenUrl="login")

# Create Access Token
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.APP_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.APP_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


# Verify Access Token
def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, settings.APP_SECRET_KEY, algorithms=settings.ALGORITHM)
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        
        token_data = TokenData(id = id)
    except JWTError:
        raise credentials_exception
    
    return token_data


# Get Current User
def get_current_user(token: str = Depends(oauth2scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate Credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.id == token.id).first()
    
    return user