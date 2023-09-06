# Объедините студентов в команды по 2-5 человек в сессионных залах.
# Разработать API для управления списком пользователей с использованием базы данных SQLite. Для этого создайте модель User со следующими полями:
# - id: int (идентификатор пользователя, генерируется автоматически)
# - username: str (имя пользователя)
# - email: str (электронная почта пользователя)
# - password: str (пароль пользователя)
#
# API должно поддерживать следующие операции:
# - Получение списка всех пользователей: GET /users/
# - Получение информации о конкретном пользователе: GET /users/{user_id}/
# - Создание нового пользователя: POST /users/
# - Обновление информации о пользователе: PUT /users/{user_id}/
# - Удаление пользователя: DELETE /users/{user_id}/
#
# Для валидации данных используйте параметры Field модели User. Для работы с базой данных используйте SQLAlchemy и модуль databases.
# from pathlib import Path
# import databases
# import sqlalchemy
# import uvicorn
# from fastapi import FastAPI
# from pydantic import BaseModel, Field
# from sqlalchemy import create_engine
#
# app = FastAPI()
#
# DATABASE_URL = "sqlite:///databases.db"
# database = databases.Database(DATABASE_URL)
# metadata = sqlalchemy.MetaData()
#
# users = sqlalchemy.Table(
#     "users",
#     metadata,
#     sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
#     sqlalchemy.Column("username", sqlalchemy.String(25)),
#     sqlalchemy.Column("email", sqlalchemy.String(50)),
#     sqlalchemy.Column("password", sqlalchemy.String(50)),
# )
#
# engine = create_engine(DATABASE_URL)
# metadata.create_all(engine)
#
#
# class User(BaseModel):
#     id: int = Field(...)
#     username: str = Field(..., max_length=25)
#     email: str = Field(..., min_length=6, max_length=50)
#     password: str = Field(..., min_length=6, max_length=50)
#
#
# class UserIn(BaseModel):
#     username: str = Field(..., max_length=25)
#     email: str = Field(..., min_length=6, max_length=50)
#     password: str = Field(..., min_length=6, max_length=50)
#
#
# @app.on_event("startup")
# async def startup():
#     await database.connect()
#
#
# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()
#
#
# @app.get("/")
# async def get_all_users():
#     query = users.select()
#     return await database.fetch_all(query)
from typing import List

import databases
import sqlalchemy
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field
from sqlalchemy import create_engine

app = FastAPI()

DATABASE_URL = "sqlite:///datab.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String(25)),
    sqlalchemy.Column("email", sqlalchemy.String(50)),
    sqlalchemy.Column("password", sqlalchemy.String(50)),
)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)


class User(BaseModel):
    id: int = Field(...)
    username: str = Field(..., max_length=25)
    email: str = Field(..., min_length=6, max_length=50)
    password: str = Field(..., min_length=6, max_length=50)


class UserIn(BaseModel):
    username: str = Field(..., max_length=25)
    email: str = Field(..., min_length=6, max_length=50)
    password: str = Field(..., min_length=6, max_length=50)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def get_all_users():
    return await database.fetch_all(users)


@app.get("/users/")
async def get_all_users():
    query = users.select()
    return await database.fetch_all(query)


@app.get("/fake_users/{count}")
async def create_note(count: int):
    for i in range(count):
        query = users.insert().values(username=f'user{i}', email=f'mail{i}@mail.ru', password='123456')
        await database.execute(query)
    return {'message': f'{count} fake users created'}


@app.get('/users/', response_model=List[User])
async def read_users():
    query = users.select()
    return await database.fetch_all(query)

@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)

@app.post("/users/",  response_model=User)
async def create_user(user: UserIn):
    query = users.insert().values(username=user.username,email=user.email, password=user.password)
    query = users.insert().values(**user.dict())
    last_record_id = await database.execute(query)
    return {**user.dict(), "id": last_record_id}

@app.put('/users/{user_id}', response_model=User)
async def update_user(user_id: int, new_user: UserIn):
    query = users.update().where(users.c.id == user_id).values(**new_user.dict())
    await database.execute(query)
    return {**new_user.dict(), "id":user_id}


@app.delete("/users/{user_id}")
async def delete_user(user_id:int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {'message': f'User {user_id} deleted'}


if __name__ == "__main__":

    uvicorn.run(f'{__file__}:app', port=8001)
