from fastapi import status, HTTPException, Depends, APIRouter
from app.schemas.user import UserCreate, UserResponse
from app.utils.hashing import Hash
from app.database import get_db
from app.models.user import User
from sqlalchemy.orm import Session

# creates A Route
router = APIRouter(
    prefix="/users",
    tags=['Users']
)


# Create Users
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    # Check if the email already exists
    existing_user = db.query(User).filter(User.email == user.email).first() 
    if existing_user:
        raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="Email already registered" )

    # Hash the password - User password
    hashed_pw = Hash.hash_password(user.password)
    new_user = User(email = user.email, hashed_password = hashed_pw)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Get User by Id
@router.get("/{id}", response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.id == id).first()

    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with Id: {id} was not found")
    
    return existing_user