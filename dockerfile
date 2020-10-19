FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN pip install uwsgi

RUN apt-get update
RUN apt-get install sqlite3

ENV DEBUG=True

COPY . .

EXPOSE 5000

CMD ["uwsgi", "--ini", "app.ini"]
