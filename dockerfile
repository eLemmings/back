FROM python:3.9

WORKDIR /app

# Instalacja zależności
COPY requirements.txt .

RUN pip install -r requirements.txt
RUN pip install uwsgi

RUN apt-get update
RUN apt-get install sqlite3

# Zmienne środowiskowe
ENV DEBUG=True

# Kopoiowanie kodu źródłowego
COPY . .

EXPOSE 5000

# Entry point
CMD ["uwsgi", "--ini", "app.ini"]
