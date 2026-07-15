"""Liveness and readiness endpoints for orchestrators and Docker healthchecks"""

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import text
from containers import Container
from db.database import Database
from core.logger import get_logger

health_router = APIRouter(tags=['health'])


@health_router.get('/health/live')
def liveness():
    """Process is running and able to handle requests."""
    return {"status": "ok"}


@health_router.get('/health/ready')
@inject
def readiness(db: Database = Depends(Provide(Container.db))):
    """Downstream dependencies (database) are reachable."""
    try:
        with db.session() as session:
            session.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception:
        get_logger().err_response(content="readiness check: database unreachable")
        return JSONResponse(status_code=503, content={"status": "unavailable"})
