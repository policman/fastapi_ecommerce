from sqlalchemy.orm import Session
from fastapi import Depends
from collections.abc import Generator

from app.database import SessionLocal

def get_db() -> Generator[Session, None, None]:
    """
    Зависимость для получения сессии бд
    Создает новую сессию и закрывает для каждого запроса
    """

    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()