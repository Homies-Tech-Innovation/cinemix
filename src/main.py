from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import settings

# Router imports
from src.routes import search

# logger imports
from src.utils.logger import setup_logging
from src.utils import logger

# Redis client
from src.services.redis_service import redis_client


# Initialize logger
setup_logging()

# App initialization
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or use settings.origins if you want strict CORS
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup routers
app.include_router(search.router, prefix="/api/v1")


# Run Redis health check on startup
@app.on_event("startup")
async def startup_event():
    await redis_client.check_connection()


# Optional: startup log
logger.info("FastAPI app initialized and routers configured ✅")
