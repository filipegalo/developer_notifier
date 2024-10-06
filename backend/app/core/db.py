from sqlmodel import Session, create_engine
from typing import Generator, Annotated
from fastapi import Depends
from app.core.config import settings

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))

def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_db)]