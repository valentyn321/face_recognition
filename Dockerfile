FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
#Adding scipts to the path, because entrypoint will be there
ENV PATH="/scripts:${PATH}"

WORKDIR /app

ADD . /app

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install --upgrade pip
RUN pip install -U pip wheel cmake
RUN pip install pipenv \
    && pipenv install --system --deploy --ignore-pipfile

RUN chmod +x scripts/*

RUN mkdir -p /vol/web/static

CMD [ "entrypoint.sh" ]
