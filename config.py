import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cambia-esta-clave-por-una-segura'
    SQLALCHEMY_DATABASE_URI = (
        os.getenv('DATABASE_URL') or
        'postgresql+psycopg2://postgres:1234@localhost/ecommerse'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    
