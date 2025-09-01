from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import settings

# Router imports
from src.routes import search

# App intialization
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup routers
app.include_router(search.router, prefix="/api/v1")
