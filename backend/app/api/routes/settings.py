from fastapi import APIRouter, HTTPException
from app.core.db import SessionDep
from app.crud.settings import get_settings, create_or_update_settings
from app.models import Settings, SettingsResponse
import logging

router = APIRouter()

@router.get("/settings", 
    summary="Get current settings",
    responses={
        200: {"description": "Successful response with settings data"},
        404: {"description": "Settings not found"},
        500: {"description": "Internal server error"},
        503: {"description": "Service unavailable"}
    },
    response_model=SettingsResponse
)
def get(db: SessionDep):
    try:
        settings = get_settings(db)
        if settings is None:
            raise HTTPException(status_code=404, detail="Settings not found")
        return settings
    except RuntimeError as e:
        logging.error(f"An error occurred: {e}")
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        if isinstance(e, HTTPException) and e.status_code == 404:
            raise e
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/settings",
    summary="Create new settings",
    responses={
        200: {"description": "Successfully created new settings"},
        400: {"description": "Bad request"},
        500: {"description": "Internal server error"}
    },
    response_model=SettingsResponse
)
def create(db: SessionDep, settings: Settings):
    try:
        new_settings = create_or_update_settings(db, **settings.model_dump())
        return new_settings
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

