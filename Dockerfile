FROM python:3.6-slim-buster

MAINTAINER giobart

ADD . /code
WORKDIR /code

RUN pip install -r requirements.txt

EXPOSE 5007

CMD ["python", "entry.py"]

