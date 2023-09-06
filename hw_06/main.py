# Необходимо создать базу данных для интернет-магазина. База данных должна
# состоять из трех таблиц: товары, заказы и пользователи. Таблица товары должна
# содержать информацию о доступных товарах, их описаниях и ценах. Таблица
# пользователи должна содержать информацию о зарегистрированных
# пользователях магазина. Таблица заказы должна содержать информацию о
# заказах, сделанных пользователями.
# ○ Таблица пользователей должна содержать следующие поля: id (PRIMARY KEY),
# имя, фамилия, адрес электронной почты и пароль.
# ○ Таблица товаров должна содержать следующие поля: id (PRIMARY KEY),
# название, описание и цена.
# ○ Таблица заказов должна содержать следующие поля: id (PRIMARY KEY), id
# пользователя (FOREIGN KEY), id товара (FOREIGN KEY), дата заказа и статус
# заказа.
#
#
# Создайте модели pydantic для получения новых данных и
# возврата существующих в БД для каждой из трёх таблиц
# (итого шесть моделей).
# Реализуйте CRUD операции для каждой из таблиц через
# создание маршрутов, REST API (итого 15 маршрутов).
# ○ Чтение всех
# ○ Чтение одного
# ○ Запись
# ○ Изменение
# ○ Удаление
from datetime import date
from typing import List
from http.client import HTTPException
import databases
import sqlalchemy
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field
from sqlalchemy import create_engine

app = FastAPI()

DATABASE_URL = "sqlite:///db_hw_6.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(25)),
    sqlalchemy.Column("surname", sqlalchemy.String(25)),
    sqlalchemy.Column("email", sqlalchemy.String(50)),
    sqlalchemy.Column("password", sqlalchemy.String(50)),

)

products = sqlalchemy.Table(
    "products",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(25)),
    sqlalchemy.Column("description", sqlalchemy.String(25)),
    sqlalchemy.Column("price", sqlalchemy.Float()),
)

orders = sqlalchemy.Table(
    "orders",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id")),
    sqlalchemy.Column("product_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("products.id")),
    sqlalchemy.Column("date", sqlalchemy.Date),
    sqlalchemy.Column("status", sqlalchemy.String(25)),
)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)
class User(BaseModel):
    id: int = Field(...)
    name: str = Field(..., max_length=25)
    surname: str = Field(..., max_length=25)
    email: str = Field(..., min_length=6, max_length=50)
    password: str = Field(..., min_length=6, max_length=50)


class UserIn(BaseModel):
    name: str = Field(..., max_length=25)
    surname: str = Field(..., max_length=25)
    email: str = Field(..., min_length=6, max_length=50)
    password: str = Field(..., min_length=6, max_length=50)


@app.post("/users/", response_model=User)
async def create_user(user: UserIn):
    query = users.insert().values(name=user.name, surname=user.surname, email=user.email, password=user.password)
    last_record_id = await database.execute(query)
    return {**user.dict(), "id": last_record_id}

@app.get("/users/", response_model=List[User])
async def read_users(skip: int = 0, take: int = 100):
    query = users.select().offset(skip).limit(take)
    return await database.fetch_all(query)

@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    result = await database.fetch_one(query)
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    return result

@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserIn):
    query = users.update().where(users.c.id == user_id).values(name=user.name, surname=user.surname, email=user.email, password=user.password)
    await database.execute(query)
    return {**user.dict(), "id": user_id}

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {"message": "User deleted successfully"}

class Product(BaseModel):
    id: int = Field(...)
    name: str = Field(..., max_length=25)
    description: str = Field(..., max_length=25)
    price: float = Field(...)

class ProductIn(BaseModel):
    name: str = Field(..., max_length=25)
    description: str = Field(..., max_length=25)
    price: float = Field(...)

@app.post("/products/", response_model=Product)
async def create_product(product: ProductIn):
    query = products.insert().values(name=product.name, description=product.description, price=product.price)
    last_record_id = await database.execute(query)
    return {**product.dict(), "id": last_record_id}

@app.get("/products/", response_model=List[Product])
async def read_products(skip: int = 0, take: int = 100):
    query = products.select().offset(skip).limit(take)
    return await database.fetch_all(query)

@app.get("/products/{product_id}", response_model=Product)
async def read_product(product_id: int):
    query = products.select().where(products.c.id == product_id)
    result = await database.fetch_one(query)
    if result is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return result

@app.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: int, product: ProductIn):
    query = products.update().where(products.c.id == product_id).values(name=product.name, description=product.description, price=product.price)
    await database.execute(query)
    return {**product.dict(), "id": product_id}

@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    query = products.delete().where(products.c.id == product_id)
    await database.execute(query)
    return {"message": "Product deleted successfully"}

class Order(BaseModel):
    id: int = Field(...)
    user_id: int = Field(...)
    product_id: int = Field(...)
    date: date
    status: str

class OrderIn(BaseModel):
    user_id: int
    product_id: int
    date: date
    status: str

@app.post("/orders/", response_model=Order)
async def create_order(order: OrderIn):
    query = orders.insert().values(user_id=order.user_id, product_id=order.product_id, date=order.date, status=order.status)
    last_record_id = await database.execute(query)
    return {**order.dict(), "id": last_record_id}

@app.get("/orders/", response_model=List[Order])
async def read_orders(skip: int = 0, take: int = 100):
    query = orders.select().offset(skip).limit(take)
    return await database.fetch_all(query)

@app.get("/orders/{order_id}", response_model=Order)
async def read_order(order_id: int):
    query = orders.select().where(orders.c.id == order_id)
    result = await database.fetch_one(query)
    if result is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return result

@app.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: int, order: OrderIn):
    query = orders.update().where(orders.c.id == order_id).values(user_id=order.user_id, product_id=order.product_id, date=order.date, status=order.status)
    await database.execute(query)
    return {**order.dict(), "id": order_id}

@app.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    query = orders.delete().where(orders.c.id == order_id)
    await database.execute(query)


if __name__ == "__main__":

    uvicorn.run(f'{__file__}:app', port=8000)
