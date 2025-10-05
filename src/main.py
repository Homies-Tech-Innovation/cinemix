# FastAPI imports
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from src.config import settings

# Router imports
from src.routes import search

# logger imports
from src.utils import logger

# Redis client
from src.redis import redis_client

# Middleware imports
from src.middlewares import rate_limiter_middleware


# Run Redis health check on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_client.check_connection()
    yield


# App initialization
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or use settings.origins if you want strict CORS
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Setup rate limiter middleware
@app.middleware("http")
async def rate_limiter_middleware_wrapper(request: Request, call_next):
    return await rate_limiter_middleware(request, call_next)


# Setup routers
app.include_router(search.router, prefix="/api/v1")

# Optional: startup log
logger.info("FastAPI app initialized and routers configured ✅")
