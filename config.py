import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "mesa-ayuda-ti-dev-key")
    SQLALCHEMY_DATABASE_URI = "sqlite:///mesa_ayuda.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
