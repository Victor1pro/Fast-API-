#This file creates the SQLALCHEMY ORM Models - This mapps out the Database Tables
from app.database import Base
from sqlalchemy import Column, String, Integer, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Post(Base):

    # Table Name
    __tablename__ = "posts"

    # Column Fields
    id = Column(Integer, primary_key=True, index=True, nullable=False) # No need for unique and nullable if primary key is set.
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String, nullable=False, index=True)
    content = Column(String, nullable=False, index=True)
    published = Column(Boolean, server_default="True", index=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.current_timestamp(), index=True)

    owner = relationship("User")


class User(Base):
    # Table name
    __tablename__ = "users"

    # Column Fields
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    email = Column(String, nullable=False, index=True, unique=True)
    hashed_password = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.current_timestamp(), index=True)


class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)


