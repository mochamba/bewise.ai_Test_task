# Импортируем библиотеку request для отправки запросов
import requests
from sqlalchemy import create_engine
# Импорт библиотеки для работы с датой и временем под псевдонимом "dt"
from datetime import datetime as dt
from app import models
from os import getenv


def requestor(questions_num: int):
    """Получает ответ от стороннего API"""
    responce_message = f"{getenv('SIDE_URL')}?count={questions_num}"
    side_response = requests.get(responce_message)
    return side_response


def json_reader(response: requests.models.Response):
    """Парсит полученный от стороннего API json ответ и сохраняет его в бд"""
    engine = create_engine(models.url_string)
    models.metadata.create_all(engine)
    with engine.connect() as connection:
        # перевод полученного ответа в список словарей
        list_of_questions = response.json()
        true_list_of_questions = []
        for question in list_of_questions:
            # Проверка полученного вопроса на наличие в таблице
            check_response = models.questions.select().where(
                models.questions.c.question_id == question['id']
                )
            checker = connection.execute(check_response).fetchall()
            if checker == []:
                last_commit = {
                    'question_id': question['id'],
                    'question_text': question['question'],
                    'answer_text': question['answer'],
                    'created_at': dt.strptime(
                        question['created_at'], getenv('FORM')).date()
                    }
                # Добавление проверенного вопроса в список для записи
                true_list_of_questions.append(last_commit)
            else:
                another_question = requestor(1)
                list_of_questions.append(another_question.json()[0])
                continue
        questions_data = models.questions.insert()
        connection.execute(questions_data, true_list_of_questions)
        connection.commit()
        connection.close()
    return last_commit
