FROM python:3.12.3-slim-bullseye as python

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV PORT 8080

WORKDIR /app

COPY . /app/

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD gunicorn workdiary.wsgi:application --bind 0.0.0.0:$PORT

EXPOSE $PORT
