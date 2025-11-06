from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped as M
from sqlalchemy.orm import mapped_column as mc
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: M[int] = mc(Integer, primary_key=True)
    email: M[str] = mc(String, unique=True, index=True, nullable=False)
    hashed_password: M[str] = mc(String, nullable=False)
    is_active: M[bool] = mc(Boolean, default=True)
    role: M[str] = mc(String, default="buyer")
    is_admin: M[bool] = mc(Boolean, default=False)

    products: M[list["Product"]] = relationship(back_populates="seller")
    reviews: M[list["Review"]] = relationship(back_populates="user")
