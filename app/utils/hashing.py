# This library enables encryption of data
from passlib.context import CryptContext 

# Defines the hashing algorithm which is bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") 


class Hash:
    # Hash Password
    def hash_password(password: str) -> str:
        """Hash a plain user password using bcrypt"""
        return pwd_context.hash(password)
    
    # Verify user password
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a plain password and compares it to hashed password"""
        return pwd_context.verify(plain_password, hashed_password)