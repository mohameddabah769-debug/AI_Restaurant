"""
FastAPI Application Entry Point for Eng. Mohamed Dabah Portfolio
Equipped with Enterprise-Grade Security Middleware & Headers
"""

import sys
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from .routes import router
from .qr_generator import generate_all_qrs

BASE_DIR = Path(__file__).resolve().parent

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    OWASP Standard Hardened Security Headers Middleware
    Protects against Clickjacking, MIME sniffing, XSS, and Information Leakage.
    """
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        response.headers["Server"] = "Shielded-Core"
        return response

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure QR codes exist on startup
    qr_dir = BASE_DIR / "static" / "images" / "qr"
    generate_all_qrs(qr_dir)
    print(">> Portfolio server initialized with 3D engine and secure assets.")
    yield

def create_app() -> FastAPI:
    app = FastAPI(
        title="Eng. Mohamed Dabah - 3D Portfolio API",
        description="High-performance secure 3D interactive portfolio for Computer Engineer Mohamed Dabah",
        version="1.0.0",
        docs_url="/docs",           # Interactive Swagger UI API Docs
        redoc_url="/redoc",         # ReDoc API Documentation
        openapi_url="/openapi.json",# OpenAPI Specification
        lifespan=lifespan
    )

    # 1. Security Headers Middleware
    app.add_middleware(SecurityHeadersMiddleware)

    # 2. Strict CORS Policy
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )

    # 3. Mount static assets
    static_dir = BASE_DIR / "static"
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    # 4. Include routes
    app.include_router(router)

    return app

app = create_app()
