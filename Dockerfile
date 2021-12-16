FROM python:3.8-slim

WORKDIR /app

COPY . /app/

RUN pip3 install pipenv

RUN pipenv install --system --deploy

CMD [ "python", "app.py" ]
