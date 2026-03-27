#config.py
import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY","devsecret")
    ADMIN_CODE = os.getenv("ADMIN_CODE", "12345678")  # store as STRING
    PRODUCER_CODE = os.getenv("ADMIN_CODE", "87654321")  # store as STRING
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL",
    f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"   # "Strict" if you don’t embed
    SESSION_COOKIE_SECURE = False     # True in HTTPS/prod
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 60*60*24*30  # 30 days (or timedelta)
    