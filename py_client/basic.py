import requests

endpoint = 'http://localhost:8000/api/'

# Emulates the http GET request
response = requests.get(endpoint, params={
                        'key-param': 'value-param'}, json={'data': 'some data in JSON format'})

print(response.json(), response.status_code)
