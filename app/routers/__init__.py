"""
Routers module
"""
from app.routers.threats import router as threats_router
from app.routers.analysis import router as analysis_router
from app.routers.reports import router as reports_router

__all__ = ["threats_router", "analysis_router", "reports_router"]
