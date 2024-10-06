from sqlalchemy.orm import Session
from app.models import Settings
from typing import Any

def get_settings(db: Session) -> Settings:
    """
    Retrieve the last (most recent) configuration from the database.

    Args:
        db (Session): The database session.

    Returns:
        models.Config: The last configuration object.
        None: If no configuration exists in the database.
    """
    return db.query(Settings).first()


def get_settings_value(db:Session, field: str) -> Any:
    """
    Retrieve a specific configuration field from the database.

    Args:
        db (Session): The database session.
        field (str): The name of the configuration field to retrieve.

    Returns:
        Any: The value of the requested configuration field.

    Raises:
        AttributeError: If the specified field does not exist in the Config model.
    """
    settings = db.query(Settings).first()
    if settings is None:
        return None
    
    if hasattr(settings, field):
        return getattr(settings, field)
    else:
        raise AttributeError(f"Settings model has no attribute '{field}'")

def create_or_update_settings(db: Session, **kwargs) -> Settings:
    """
    Create or update the single settings entry in the database.

    Args:
        db (Session): The database session.
        **kwargs: Keyword arguments representing the fields and values for the settings.

    Returns:
        models.Settings: The created or updated settings object.

    Raises:
        ValueError: If no valid fields are provided in kwargs.
    """
    settings = db.query(Settings).first()

    if settings is None:
        settings = Settings()
        db.add(settings)

    valid_fields = [column.key for column in Settings.__table__.columns if column.key != 'id']
    updated = False

    for field, value in kwargs.items():
        if field in valid_fields:
            setattr(settings, field, value)
            updated = True

    if not updated:
        raise ValueError("No valid fields provided for updating settings.")

    db.commit()
    db.refresh(settings)

    return settings
