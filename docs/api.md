# API
API pozwala na wygodne tworzenie aplikacji klienciej i zapewnia możliwość całkowitego odseparowania jej od warstwy logicznej.  

## Endpointy
### /user
###### GET
Pozwala na pobranie danych użytkownika  
- id - id użytkownika którego dane chcemy pobrać

###### PUT
Rejestruje użytkownika
- nick - nick użytkownika
- email - email
- password - hasło

###### PATCH
Aktualizuje dane użytkownika
- id - id użytkownika którego dane chcemy zaktualizować
- field - pole w bazie które będzie zaktualizowane
- value - wartość

###### DELETE
Usuwa użytkownika
- id - id użytkownika którego chcemy usunąć


### /user/data
###### GET
Pobiera dane JSON użytkownika
- id - id użytkownika którego JSON chcemy pobrać

###### PUT
Nadpisuje dane JSON użytkownika
- id - id użytkownika
- json - string z danymi JSON do nadpisania