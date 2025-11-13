
from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped as M, mapped_column as mc, relationship

from app.database import Base

class Category(Base):
    __tablename__ = "categories"

    id: M[int] = mc(primary_key=True)
    name: M[str] = mc(String(50), nullable=False)
    parent_id: M[int | None] = mc(ForeignKey("categories.id"), nullable=True)
    is_active: M[bool] = mc(Boolean, default=True)

    products: M[list["Product"]] = relationship(back_populates="category")

    parent: M["Category | None"] = relationship(back_populates="children",
                                                remote_side="Category.id")

    children: M[list["Category"]] = relationship(back_populates="parent")
