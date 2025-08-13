# срок действия токена
from datetime import datetime, timedelta

# библиотека для генерации и валидации токенов
from jose import JWTError, jwt

# хэширование паролей с помощью passlib
from passlib.context import CryptContext

# обработка ошибок fastapi
from fastapi import HTTPException, status

# импорт модели пользователя
from salary_service.models import User

# импорт класса из sqlalchemy
from sqlalchemy.orm import Session

# импорт функции получения сессии
from salary_service.database import SessionLocal

# кастомные настройки
from salary_service.config import settings

# хэщирование паролей: использование алгоритма bcrypt и автопометка устаревших хэшей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# сравнение введенного пароля с хэшем из БД
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# генерация безопасного хэша
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# генерация токена: копирование данных входа, добавление времени действия токена из настроек, подпись токена секретным ключом
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# аутентификация пользователей
def authenticate_user(username: str, password: str, db: Session):
    print(f"Authenticating user: {username}")
    user = db.query(User).filter(User.username == username).first()

    if not user:
        print("User not found")
        return None

    print(f"User found: {user.username}")
    if not verify_password(password, user.hashed_password):
        print("Password verification failed")
        return None

    print("Authentication successful")
    return user

# декорирование токена с использованием секретного ключа
def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

