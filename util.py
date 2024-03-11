
class Cache:

    def __init__(self):
        self.dict = {}

    def set(self, key, value):
        self.dict[key] = value

    def get(self, key):
        return self.dict.get(key)
