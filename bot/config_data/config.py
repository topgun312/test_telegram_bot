import os

from dotenv import find_dotenv, load_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены так как отсутствует файл .env")
else:
    load_dotenv()


BOT_TOKEN = os.getenv("BOT_TOKEN")


DATABASE_DATA = {
    "drivername": "postgresql",
    "host": os.getenv("POSTGRES_HOST"),
    "database": os.getenv("POSTGRES_DB"),
    "username": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "port": os.getenv("POSTGRES_PORT"),
    "query": {},
}


DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("clubs", "Все клубы знакомств по интересам"),
    ("myclubs", "Мои избранные клубы знакомств"),
    ("proposals", "Предложения на знакомство"),
    ("myproposals", "Мои предложения на знакомство"),
    ("myfriends", "Мои друзья"),
    ("settings", "Настройки бота"),
)

