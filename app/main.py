from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
# from app.database import engine
# from app.models import user
from app.Routers import post, users, vote
from app.auth import auth

# Creates the Table from ORM models from the models folder (if using alembic no need)
# user.Base.metadata.create_all(bind=engine)

# Creates an FastAPI Instance
app = FastAPI()

origins = []

# Creates a Middleware
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"]
)

# Define Routes
app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=5000, reload=True)
