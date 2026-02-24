# import sqlite3
# import time

# # Connect to SQLITE3 DATABASE
# def connect_to_db(db_path="fastapi.db", retry_delay=3):
#     while True:
#         try:
#             conn = sqlite3.connect(db_path, timeout=5)
#             conn.row_factory = sqlite3.Row
#             print("Database connection was successful")
#             return conn
#         except Exception as error:
#             print("Connection failed:", error)
#             time.sleep(retry_delay)


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.config.settings import settings

# To avoid declarative_base Warnings
class Base(DeclarativeBase): 
    pass


if settings.DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False},
        future=True
    )
else:
    engine = create_engine(
        settings.DATABASE_URL, 
        future=True
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

Base = declarative_base()

# Dependency (Creates a Session for the Database)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

