import requests

endpoint = 'http://localhost:8000/api/'

# Emulates the http GET request
response = requests.get(endpoint, params={
                        'key-param': 'value-param'}, json={'data': 'some data in JSON format'})

print(response.json(), response.status_code)


class Point:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y


p = Point(2, 6)

print(p.x)

p._x = 4

print(p.x)
