from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import settings

# Router imports
from src.routes import search

# logger imports
from src.utils.logger import setup_logging


# Initialize logger
from src.utils import logger

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

# Optional: startup log
logger.info("FastAPI app initialized and routers configured ✅")
