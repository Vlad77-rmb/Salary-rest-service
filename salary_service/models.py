# Column - определение столбцов таблицы, Integer, String и Date - sql, которые будут преобразованы в типы данных
from sqlalchemy import Column, Integer, String, Date, Float

# базовый класс для моделей SQLAlchemy
from .database import Base

# модель соответствует таблице в базе данных
class User(Base):
    __tablename__ = "users"

# описание каждого столбца таблицы
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, nullable=True)
    hashed_password = Column(String)
    current_salary = Column(Float)
    next_raise_date = Column(Date)