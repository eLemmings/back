# Funkcje pomocnicze
import uuid

# Generator UUID
def gen_uuid():
    return str(uuid.uuid4()).replace('-', '')

# Zamienia id na krótszą forme
def gen_pretty_id(id: int):
    return str(hex(id))[2:].upper().rjust(4, '0')