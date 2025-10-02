from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import settings

# Router imports
from src.routes import search

# logger imports
from src.utils.logger import setup_logging
from src.utils import logger

# Redis client
from src.redis import redis_client


# Initialize logger
setup_logging()


# Run Redis health check on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_client.check_connection()
    yield
    await redis_client.client.close()


# App initialization
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or use settings.origins if you want strict CORS
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup routers
app.include_router(search.router, prefix="/api/v1")

# Optional: startup log
logger.info("FastAPI app initialized and routers configured ✅")
