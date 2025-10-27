import os
from dotenv import load_dotenv

# Cargar las variables del .env
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "clave-por-defecto")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("❌ La variable DATABASE_URL no está definida en el archivo .env")









# import os
# basedir = os.path.abspath(os.path.dirname(__file__))

# class Config:
#     SECRET_KEY = os.environ.get('SECRET_KEY') or 'cambia-esta-clave-por-una-segura'
#     SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1234@localhost:5432/ecommerse'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False



# import os
# basedir = os.path.abspath(os.path.dirname(__file__))

# class Config:
#     SECRET_KEY = os.environ.get('SECRET_KEY') or 'cambia-esta-clave-por-una-segura'
#     SQLALCHEMY_DATABASE_URI = (
#         os.getenv('DATABASE_URL') or
#         'postgresql+psycopg2://postgres:1234@localhost/'
#     )
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

# import os

# class Config:
#     SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-segura'
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
