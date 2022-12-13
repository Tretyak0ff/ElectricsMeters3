import os
from loguru import logger
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


load_dotenv(find_dotenv())

DATABASES_NAME = os.environ.get('DATABASES_NAME')
DATABASES_USER = os.environ.get('DATABASES_USER')
DATABASES_PASSWORD = os.environ.get('DATABASES_PASSWORD')
DATABASES_HOST = os.environ.get('DATABASES_HOST')
DATABASES_PORT = os.environ.get('DATABASES_PORT')


def get_engine(db_user, db_password, db_host, db_port, db_name):
    url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    connection = create_engine(url, pool_size=10, max_overflow=20)
    return connection


engine = get_engine(db_user=DATABASES_USER,
                    db_password=DATABASES_PASSWORD,
                    db_host=DATABASES_HOST,
                    db_port=DATABASES_PORT,
                    db_name=DATABASES_NAME)
try:
    Session = sessionmaker(bind=engine)
    logger.info(f'\n *** Connect DB...')
finally:
    sessionmaker.close_all()
