# API
API pozwala na wygodne tworzenie aplikacji klienciej i zapewnia możliwość całkowitego odseparowania jej od warstwy logicznej.  

## Uwierzytelnianie
1. Pobieramy token korzystając z endpointu logowania `/user/login`
1. Umieszczamy token w nagłowkau zapytania które chcemy uwierzytelnić `Authorization: Bearer <token>`

## Endpointy
### /register
###### POST
Rejestruje użytkownika
```js
"nick": "<nazwa użytkownika>",
"email": "<email>",
"password": "<hasło>",
```


### /login
###### POST
Zwraca token niezbędny do uwierzytelnienia
```js
"email": "<email>",
"password": "<hasło>",
```


### /user
###### GET - (Wymaga uwierzytelnienia)
Pozwala na pobranie danych użytkownika  

###### PATCH - (Wymaga uwierzytelnienia)
Aktualizuje dane użytkownika
```js
"field": "<np. email albo nick>",
"value": "<wartość>",
```
###### DELETE - (Wymaga uwierzytelnienia)
Usuwa użytkownika


### /user/data
###### GET - (Wymaga uwierzytelnienia)
Pobiera dane JSON użytkownika

###### PUT - (Wymaga uwierzytelnienia)
Nadpisuje dane JSON użytkownika
```js
"diaries": [{
    "name": "Mój dziennik",
    "type": "int",
    "min": 1,
    "max": 5,
    "date": 0,
    "colors": ["#ff0000", "#00ff00", "#098ab3", "#ae4582", "#975bca"],
    "entries": [[]]
}]
```

### /share
###### GET - (Wymaga uwierzytelnienia)
Pobiera wszystkie udostępnienia użytkownika

###### PUT - (Wymaga uwierzytelnienia)
Dodaje udostępnienie
```js
"index": "<indeks dziennika w pliku json>"
```


### /share/<uuid>
###### GET
Zwraca jeden dziennik i usuwa udostępnienie z bazy danych. Z linku można skorzystać tylko raz