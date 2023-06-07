from os import getenv, path
from dotenv import load_dotenv


load_dotenv()

# Database
DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT")
DB_NAME = getenv("DB_NAME")
DB_USER = getenv("DB_USER")
DB_PASSWORD = getenv("DB_PASSWORD")

# Authentication
SECRET_KEY = "You********secret******string****e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60000

HOST = "localhost"
PORT = "8000"

CURRENT_PATH = path.curdir

URL_GET_QUIZ_QUESTIONS = "https://jservice.io/api/random?count="


