from fastapi import FastAPI

from app.log import log_middleware
from app.routers import categories, products, reviews, users

app = FastAPI(title="FastAPI Интернет-магазин", version="0.1.0")

app.middleware("http")(log_middleware)

app.include_router(categories.router)
app.include_router(products.router)
app.include_router(users.router)
app.include_router(reviews.router)


@app.get("/")
async def root():
    """
    Корневой маршрут, подтверждающий, что API работает
    """
    return {"message": "Добро пожаловать в API интернет-магазина"}
