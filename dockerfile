FROM python3.9-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN apt-get install sqlite3

ENV DEBUG=False

EXPOSE 5000

COPY . .

CMD ['uwsgi', 'app.ini']
