# Django Course

Notes from the Django course available at [https://www.youtube.com/watch?v=c708Nf0cHrs](https://www.youtube.com/watch?v=c708Nf0cHrs)

## Set up

- `.gitignore` taken from [https://github.com/jpadilla/django-project-template](https://github.com/jpadilla/django-project-template)

## The backend

Inside the `backend` folder, execute `django-admin startproject cfehome .`

### Core Django

Use `python3 manage.py runserver 8000` to run Django

### API

Use `python3 manage.py startapp api` that will create the `api` folder and then add the `api` string in the `INSTALLED_APPS` array of the `settings.py` file of the `cfehome`.

It is a good idea to create a `urls.py` in the `api` folder just like it exists in the `cfehome` folder, in order to distinguish API urls from the others.

Add a urlpattern to point to the API urls with the `path('api/', include('api.urls'))` where `api.urls` is the relative path to the `urls.py` file in the `api` folder.

The `request` object in the `def api_home(request, ...)` is an `HttpRequest` object created by Django. 

`request.body` is a bytestream of string, so use `try: data = json.loads(request.body)` to hav a dict.

Use `request.headers` to access the headers of the request; however, it cannot be converted into JSON with `json.loads(...)` and `dict(...)` must be used.

Use `request.GET` to access the url query params as a QueryDict object.

#### The Django Model instance as an API response

First of all execute `python3 manage.py startapp products`, add `products` in the `INSTALLED_APPS` of the core `settings.py` file.

Now create a Python3 class Product that inherits the `models.Model` Django object and create some properties leveraging the `models` classes.

Now execute:
- `python3 manage.py makemigrations` to let the db know what is happening in the `model.py` file
- `python3 manage.py migrate` to make sure the db actually changes

In order to enter the shell of Django, execute `python3 manage.py shell`; now create a Product and insert it into the db with `Product.objects.create(title='a', content='b', price=0)`.

In the `views.py` of the `api`, use `Product.objects.all().order_by('?').first()` to retrieve all the products and pick a random one. 

Use `from django.forms.models import model_to_dict` and the method to automatically transform the model into a dictionary.

Currently, we are using the `JsonResponse` object, but we can use the `HttpResponse` to have a `text/html` content type (by default), or a different format with `HttpResponse(data, headers={'contentType': 'application/json'})`. However, in this case, we cannot pass the data as is (i.e. a dictionary) and without using `json.dumps(...)` because there may be complex types coming from Django, such as `Decimal`. 

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

### Imports

- `from . import views` to import the module `views` in the same folder
- `from .views import api_home` to import just one function from the `views` folder

### dir()

The dir() method returns the list of valid attributes of the passed object.