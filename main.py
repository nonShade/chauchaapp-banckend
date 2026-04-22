"""
ChauchaApp Backend API.

FastAPI application with authentication endpoints,
CORS middleware, and global exception handlers.
"""

import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

load_dotenv()

from app.modules.auth.controller import router as auth_router
from app.shared.exceptions import AppException

app = FastAPI(
    title="ChauchaApp API",
    description="API Backend for ChauchaApp — financial literacy platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------
cors_origins = os.getenv(
    "CORS_ORIGINS", "http://localhost:3000,http://localhost:8000"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in cors_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(auth_router)


# ---------------------------------------------------------------------------
# Global Exception Handlers
# ---------------------------------------------------------------------------
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    """Map AppException subclasses to appropriate HTTP status codes."""
    status_map = {
        "VALIDATION_ERROR": 400,
        "NOT_FOUND": 404,
        "CONFLICT": 409,
        "UNAUTHORIZED": 401,
        "INTERNAL_ERROR": 500,
    }
    status_code = status_map.get(exc.code, 500)
    return JSONResponse(
        status_code=status_code,
        content={"error": exc.message},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Catch-all handler for unhandled exceptions."""
    return JSONResponse(
        status_code=500,
        content={"error": "Ocurrió un error interno. Intente más tarde."},
    )


# ---------------------------------------------------------------------------
# Health Check
# ---------------------------------------------------------------------------
@app.get("/health", tags=["System"])
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
