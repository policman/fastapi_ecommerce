from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import get_current_buyer, get_current_user
from app.db_depends import get_async_db
from app.models import Product as ProductModel
from app.models import Review as ReviewModel
from app.models import User as UserModel
from app.schemas import ReviewCreate, Review as ReviewSchema

router = APIRouter(tags=["reviews"])


async def recalc_product_grade(product_id: int, db: AsyncSession):
    # пересчёт нового рейтинга
    avg_stmt = select(func.avg(ReviewModel.grade)).where(
        ReviewModel.product_id == product_id, ReviewModel.is_active.is_(True)
    )
    avg_grade = float((await db.scalar(avg_stmt)) or 0.0)

    # пересчет нового количества отзывов
    count_stmt = select(func.count(ReviewModel.id)).where(
        ReviewModel.product_id == product_id, ReviewModel.is_active.is_(True)
    )
    count_grade = int((await db.scalar(count_stmt)) or 0)

    await db.execute(
        update(ProductModel)
        .where(ProductModel.id == product_id)
        .values(rating=avg_grade, count_review=count_grade)
    )



@router.get("/reviews", response_model=list[ReviewSchema])
async def get_reviews(db: AsyncSession = Depends(get_async_db)):
    reviews = (
        await db.scalars(select(ReviewModel).where(ReviewModel.is_active.is_(True)))
    ).all()

    return reviews


@router.get("/products/{product_id}/reviews", response_model=list[ReviewSchema])
async def get_review(product_id: int, db: AsyncSession = Depends(get_async_db)):
    product_reviews = (
        await db.scalars(
            select(ReviewModel).where(
                ReviewModel.product_id == product_id, ReviewModel.is_active.is_(True)
            )
        )
    ).all()

    if product_reviews is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reviews for {product_id} not found or inactive",
        )
    return product_reviews


# не по тз, решил получать product_id из параметра пути, вместо тела
@router.post("/products/{product_id}/reviews",
             response_model=ReviewSchema,
             status_code=status.HTTP_201_CREATED,
)
async def create_review(review: ReviewCreate,
                        product_id: int,
                        db: AsyncSession = Depends(get_async_db),
                        current_user: UserModel = Depends(get_current_buyer),
):

    # проверка есть ли уже у пользователя отзыв на данный товар --Не по тз
    is_user_already_review = await db.scalar(
        select(ReviewModel).where(
            ReviewModel.user_id == current_user.id,
            ReviewModel.product_id == product_id,
            ReviewModel.is_active.is_(True)
        )
    )
    if is_user_already_review is not None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Review already exists",
        )

    # проверка существования и активности товара
    is_product = await db.scalar(
        select(ProductModel).where(
            ProductModel.id == product_id, ProductModel.is_active.is_(True)
        )
    )
    if is_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found or inactive",
        )

    db_review = ReviewModel(
        **review.model_dump(), user_id=current_user.id, product_id=product_id
    )
    db.add(db_review)
    await recalc_product_grade(product_id, db)
    await db.commit()
    await db.refresh(db_review)

    return db_review


@router.delete("/reviews/{review_id}")
async def delete_review(
    review_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: UserModel = Depends(get_current_user),
):
    review = await db.scalar(
        select(ReviewModel).where(
            ReviewModel.id == review_id, ReviewModel.is_active.is_(True)
        )
    )
    if review is None:
        raise HTTPException(
            status_code=404, detail="Review not found or already deleted"
        )

    if review.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only author can delete review")



    await db.execute(
        update(ReviewModel).where(ReviewModel.id == review_id).values(is_active=False)
    )

    await recalc_product_grade(review.product_id, db)
    await db.commit()

    return {"message": "Review deleted"}
