import uuid

def gen_uuid():
    return str(uuid.uuid4()).replace('-', '')

def gen_pretty_id(id: int):
    return str(hex(id))[2:].upper().rjust(4, '0')