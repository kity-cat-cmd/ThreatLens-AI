"""
ThreatLens AI - Main Application Entry Point
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database.init_db import init_database
from app.routers import threats_router, analysis_router, reports_router
from app.services.threat_service import ThreatService

settings = get_settings()

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting ThreatLens AI...")
    init_database()
    logger.info("ThreatLens AI started successfully!")
    yield
    # Shutdown
    logger.info("Shutting down ThreatLens AI...")


# Create FastAPI application
app = FastAPI(
    title="ThreatLens AI",
    description="AI-Powered Security Threat Analysis Platform",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(threats_router)
app.include_router(analysis_router)
app.include_router(reports_router)


@app.get("/api/v1/health")
def health_check():
    """Health check endpoint"""
    return {"status": "ok", "service": "ThreatLens AI", "version": "1.0.0"}


@app.get("/api/v1/stats")
def get_statistics():
    """Get threat statistics"""
    from app.database import SessionLocal

    db = SessionLocal()
    try:
        service = ThreatService(db)
        return service.get_statistics()
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the dashboard"""
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()


# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
    )
