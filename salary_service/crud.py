# класс сессии для взаимодействия с базой данных
from sqlalchemy.orm import Session

# модули с моделями SQLAlchemy и pydantic-схемами
from . import models, schemas

# хэширование паролей
from .auth import get_password_hash

# запрос на получение пользователя по условию
def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

# создание нового пользователя
def create_user(db: Session, user: schemas.UserCreate):

    # хэширование пароля
    hashed_password = get_password_hash(user.password)

    # создание модели пользователя с данными из таблицы с последующим добавлением к БД
    db_user = models.User(
        username=user.username,
        hashed_password=hashed_password,
        current_salary=user.current_salary,
        next_raise_date=user.next_raise_date
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user