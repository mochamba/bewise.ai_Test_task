FROM python:latest
LABEL AUTHOR: Anton Rybakov 'ribokov@gmail.com'
WORKDIR /code 

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN mkdir /code/app
COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
