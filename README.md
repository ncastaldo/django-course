# Django Course

Notes from the Django course available at [https://www.youtube.com/watch?v=c708Nf0cHrs](https://www.youtube.com/watch?v=c708Nf0cHrs)

## Set up

- `.gitignore` taken from [https://github.com/jpadilla/django-project-template](https://github.com/jpadilla/django-project-template)

## The backend

Inside the `backend` folder, execute `django-admin startproject cfehome .`

Use `python3 manage.py runserver 8000` to run Django

Use `python3 manage.py startapp api` that will create the `api` folder and then add the `api` string in the `INSTALLED_APPS` array of the `settings.py` file of the `cfehome`.

It is a good idea to create a `urls.py` in the `api` folder just like it exists in the `cfehome` folder, in order to distinguish API urls from the others.

## The frontend

Inside the `py_client` folder we are going to create the client consuming the API.

`https://www.httpbin.org/` as a test example for an API

JSON format is slightly different from Python3 dict object
- `response.text` to have the JSON as is
- `response.json()` to transform it into a dictionary

`response = requests.get(endpoint, ...)` 
- `data = {'key': 'value'}` -> application/x-www-form-urlencoded
- `json = {'key': 'value'}` -> application/json
- `params = {'key': 'value'}` -> parameters are placed in urlencoded

## Common

### *args and **kwargs

```python
def myFun(*args,**kwargs):
    print("args: ", args)
    print("kwargs: ", kwargs)  
  
# Now we can use both *args ,**kwargs
# to pass arguments to this function :
myFun("geeks", "for", "geeks", first="Nicola", second="here")

"""
Output:
args: ('geeks', 'for', 'geeks')
kwargs {'first': 'Nicola', 'second': 'here'}
"""
```