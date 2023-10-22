from pydantic import BaseModel
from sqlalchemy import MetaData, Table, String, Integer, DateTime, Column, URL
from os import getenv


# Класс для принятия POST запросов
class Questions_req(BaseModel):
    questions_num: int = 1


# объект представляющий собой таблицу базы данных
metadata = MetaData()
questions = Table(
    'questions',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('question_id', Integer),
    Column('question_text', String(200)),
    Column('answer_text', String(150)),
    Column('created_at', DateTime),
)

# Собирает строку для подключения к бд
url_string = URL.create(
        'postgresql+pg8000',
        username=getenv('POSTGRES_USER'),
        password=getenv('POSTGRES_PASSWORD'),
        host='postgres',
        database=getenv('DATABASE')
            )
