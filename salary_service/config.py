# импорт класса BaseSettings для работы с настройками приложения
from pydantic_settings import BaseSettings

# создаем класс settings, который является хранилищем всех настроек приложения
class Settings(BaseSettings):

    # задача параметров настройкам
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    DATABASE_URL: str = "sqlite:///./salary.db"

# настройки конфигурации класса, в них указываем что настройки берем из файла ".env" и файл будет читаться в кодировке utf-8
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# создание объекта settings
settings = Settings()