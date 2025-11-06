from decimal import Decimal

from sqlalchemy import Boolean, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped as M, mapped_column as mc, relationship

from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id: M[int] = mc(primary_key=True)
    name: M[str] = mc(String(100), nullable=False)
    description: M[str | None] = mc(String(500), nullable=True)
    price: M[Decimal] = mc(Numeric(10, 2), nullable=False)
    image_url: M[str | None] = mc(String(200), nullable=True)
    stock: M[int] = mc(Integer, nullable=False)
    is_active: M[bool] = mc(Boolean, default=True)
    category_id: M[int] = mc(
        ForeignKey("categories.id"), nullable=False, index=True
    )
    seller_id: M[int] = mc(
        ForeignKey("users.id"), nullable=False, index=True
    )
    rating: M[Decimal | None] = mc(Numeric(2, 1),
                                   nullable=True,
                                   index=True)  # не по тз

    count_review: M[int] = mc(Integer, default=0, nullable=False)  # не по тз

    seller: M["User"] = relationship(back_populates="products")
    category: M["Category"] = relationship(back_populates="products")
    reviews: M[list["Review"]] = relationship(back_populates="product")
