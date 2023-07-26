# syntax=docker/dockerfile:1

FROM python:3.10.0

WORKDIR /my-expenses

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

ENV FLASK_APP=web_server.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=0

COPY . .

CMD ["python3", "web_server.py"]