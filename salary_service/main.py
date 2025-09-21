from salary_service.database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
from datetime import datetime
from salary_service.database import get_db
from fastapi.security import OAuth2PasswordRequestForm  
from fastapi.middleware.cors import CORSMiddleware
# импорт основных компонентов приложения
from fastapi import FastAPI, Depends, HTTPException, status

# аутентификация
from fastapi.security import OAuth2PasswordBearer

#  функции для генерации токенов и проверки учетных записей
from salary_service.auth import authenticate_user, create_access_token

# получение данных пользователя из БД
from salary_service.database import get_user_data

# создание модели пользователя
from salary_service.models import User

# типизация ответов с помощью pydantic-моделей
from salary_service.schemas import Token, SalaryResponse

# функция для работы с временными интервалами
from datetime import timedelta

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешает все домены
    allow_credentials=True,
    allow_methods=["*"],  # Разрешает все методы (GET, POST и т.д.)
    allow_headers=["*"],  # Разрешает все заголовки
)

@app.get("/")
async def root():
    return {
        "message": "Welcome to Salary Service",
        "docs": "http://127.0.0.1:8000/docs",
        "endpoints": {
            "login": "POST /token",
            "get_salary": "GET /salary"
        }
    }


def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Проверяем существование пользователя admin
        admin_exists = db.query(User).filter(User.username == "admin").first()
        print(f"Admin exists: {admin_exists is not None}")

        if not admin_exists:
            print("Creating admin user...")
            raise_date = datetime.strptime("2023-12-01", "%Y-%m-%d").date()
            hashed_pwd = get_password_hash("secret")
            admin_user = User(
                username="admin",
                hashed_password=hashed_pwd,
                current_salary=50000.0,
                next_raise_date=raise_date
            )
            db.add(admin_user)
            db.commit()
            print("Admin user created successfully")
        else:
            print("Admin user already exists")
    except Exception as e:
        print(f"Error creating admin user: {e}")
        db.rollback()
    finally:
        db.close()

@app.on_event("startup")
def on_startup():
    init_db()

# создание QAuth2 с указанием url для получения токена
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# регистрирует отправку данных на сервер по пути /token
@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    # проверка аутентификации пользователя
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # генерация jwt-токена с именем пользователя и сроком действия 15 минут
    access_token_expires = timedelta(minutes=15)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# запрос к сервису для получения данных о зарплате
@app.get("/salary", response_model=SalaryResponse)

# автоматическая проверка и извлечение токена из заголовка
async def read_salary(token: str = Depends(oauth2_scheme)):

    # получение данных пользователя
    user_data = get_user_data(token)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "current_salary": user_data["current_salary"],
        "next_raise_date": user_data["next_raise_date"]
    }
