import requests

endpoint = 'http://localhost:8000'

# Emulates the http GET request
response = requests.get(endpoint)

print(response.text, response.status_code)
