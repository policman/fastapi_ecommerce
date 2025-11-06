from sqlalchemy.orm import Session

from app.database import SessionLocal


def get_db():
    """
    Зависимость для получения сессии бд
    Создает новую сессию и закрывает для каждого запроса
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------- async -------------
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session_maker


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """Предоставляет асинхронную сессию SQLAlchemy для работы с бд PostgreSQL"""
    async with async_session_maker() as session:
        yield session
