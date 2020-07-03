FROM python:3.8

WORKDIR /home

RUN pip install -U pip aiogram && apt-get update

COPY ./

ENTRYPOINT ["python", "bot.py"]