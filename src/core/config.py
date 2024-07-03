import os
from dotenv import load_dotenv


load_dotenv()

# DB
DB_HOST_PET = os.getenv("DB_HOST_PET")
DB_USER_PET = os.getenv("DB_USER_PET")
DB_PASS_PET = os.getenv("DB_PASS_PET")
DB_NAME_PET = os.getenv("DB_NAME_PET")
DB_PORT_PET = os.getenv("DB_PORT_PET")

# TEST
DB_HOST_TEST = os.getenv("DB_HOST_TEST")
DB_USER_TEST = os.getenv("DB_USER_TEST")
DB_PASS_TEST = os.getenv("DB_PASS_TEST")
DB_NAME_TEST = os.getenv("DB_NAME_TEST")
DB_PORT_TEST = os.getenv("DB_PORT_TEST")

# REDIS
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")


# EMAIL
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

# JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
