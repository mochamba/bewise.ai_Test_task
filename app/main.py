
from fastapi import FastAPI
from app import models
from app.methods import requestor, json_reader


app = FastAPI(title='questions_miner')


@app.post('/')
def main(question_req: models.Questions_req):
    """Получает запрос количества вопросов и переадресовывает его на url"""
    side_response = requestor(question_req.questions_num)
    if side_response.status_code == 200:
        last_commit = json_reader(side_response)
        return last_commit
    else:
        return last_commit

