import uuid
from random import randint

__author__ = 'exor'


class UUID:

    def __init__(self):
        pass
    
    @staticmethod
    def uuid_generator():
        return str(uuid.uuid4())


class RandomPassword:

    def __init__(self):
        pass

    @staticmethod
    def random_password_generator(n):
        range_start = 10 ** (n - 1)
        range_end = (10 ** n) - 1
        return str(randint(range_start, range_end))

