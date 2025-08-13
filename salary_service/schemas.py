# в модуль datatime мпортируем date для работы с датами
from datetime import date

# добавляем тип Optional из модуля typing, которые указывает что поле может быть None
from typing import Optional

# добавляем базовый класс для pydantic-схем, проверку для емейл и доп.ограничения для полей
from pydantic import BaseModel, Field

# сам токен
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# данные токена
class TokenData(BaseModel):
    username: Optional[str] = None

# база пользователей с параметрами логина
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: Optional[str] = None

# создание "профиля" пользователя по требованиям
class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    current_salary: float = Field(..., gt=0)
    next_raise_date: date

# занесение пользователя в базу, где хранится его номер, пароль, зарплата и дата повышения
class UserInDB(UserBase):
    id: int
    hashed_password: str
    current_salary: float
    next_raise_date: date

    class Config:
        from_attributes = True

# информация и зарплате: сколько получают и когда повысят
class SalaryInfo(BaseModel):
    current_salary: float
    next_raise_date: date

# Публикация публичного профиля - номер в базе, зарплата и дата повышения, которые видят другие пользователи
class UserPublic(UserBase):
    id: int
    current_salary: float
    next_raise_date: date

# класс который будет использоваться для валидации, сериализации и документации данных
class SalaryResponse(BaseModel):
    current_salary: float
    next_raise_date: str