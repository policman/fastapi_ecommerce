from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Text, func
from sqlalchemy.orm import Mapped as M
from sqlalchemy.orm import mapped_column as mc
from sqlalchemy.orm import relationship

from app.database import Base


class Review(Base):
    __tablename__ = "reviews"

    id: M[int] = mc(primary_key=True)
    user_id: M[int] = mc(ForeignKey("users.id"), index=True, nullable=False)
    product_id: M[int] = mc(ForeignKey("products.id"), index=True, nullable=False)
    comment: M[str | None] = mc(Text, nullable=True)
    comment_date: M[datetime] = mc(DateTime(timezone=True), server_default=func.now())
    grade: M[int] = mc(Integer, nullable=False)
    is_active: M[bool] = mc(Boolean, default=True)

    user: M["User"] = relationship(back_populates="reviews")
    product: M["Product"] = relationship(back_populates="reviews")
