

class Adealsweden():

    def __init__(self, name, price, url):
        self.name = name
        self.price = price
        self.url = url

    def __repr__(self):
        return f'{self.name=} {self.price=} {self.url=}'

class Swedroid():

    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return f'{self.url=}'
    
class Amazon():

    def __init__(self, name, price, url):
        self.name = name
        self.price = price
        self.url = url

    def __repr__(self):
        return f'{self.name=} {self.price=} {self.url=}'
    