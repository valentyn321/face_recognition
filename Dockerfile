FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
RUN mkdir /app/static

ADD . /app

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install --upgrade pip
RUN pip install -U pip wheel cmake
RUN pip install pipenv \
    && pipenv install --system --deploy --ignore-pipfile

RUN python manage.py migrate
RUN python manage.py collectstatic

EXPOSE 8000
