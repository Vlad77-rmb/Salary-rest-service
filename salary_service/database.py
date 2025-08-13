# создание подключения к базе данных
from sqlalchemy import create_engine

# создание базового класса для декларативного определения модулей
from sqlalchemy.ext.declarative import declarative_base

# создание сессий работы с базами данных
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

from jose import JWTError, jwt
from salary_service.schemas import TokenData
from fastapi import HTTPException, status
from salary_service.config import settings

# использование БД - SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./salary.db"

# создание основного движка
engine = create_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False}
)

# настройка сессий с отключением синхронизации с БД и отключением автоматических изменений
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
 # базовый класс, от которого наследуются все модели БД
Base = declarative_base()

# генератор, создающий новую сессию БД, с параметрами возврата ее через yield и принудительного закрытия сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# получение данных пользователя из токена
def get_user_data(token: str):
    from .models import User
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    with SessionLocal() as db:
        user = db.query(User).filter(User.username == token_data.username).first()
        if user is None:
            raise credentials_exception

    return {
        "current_salary": user.current_salary,
        "next_raise_date": user.next_raise_date.strftime("%Y-%m-%d")  # Преобразуем дату в строку
    }