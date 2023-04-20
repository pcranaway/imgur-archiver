import random
import string

def gen_id() -> str:
    id = ''

    for _ in range(5):
        id = id + random.choice(string.ascii_letters + string.digits)

    return id
