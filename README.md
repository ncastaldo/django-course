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

### From the API view to the Django REST framework view

Use:
- `from rest_framework.response import Response`, which is a wrapper for the data
- `from rest_framework.decorators import api_view`, which is a decorator

Now we can transform the `api_home` method into a REST enpoint buy using `@api_view(["GET"])` as annotation and `Response(data)` as return value.   

### Django Rest Framework Model Serializer



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

### Decorators

Decorators provide a simple syntax for calling higher-order functions. By definition, a decorator is a function that takes another function and extends the behavior of the latter function without explicitly modifying it.

Put simply: decorators wrap a function, modifying its behavior.

Instead, Python allows you to use decorators in a simpler way with the `@` symbol, sometimes called the “pie” syntax.

Example:

```python
def do_twice(func):
    @functools.wraps(func)
    def wrapper_do_twice(*args, **kwargs):
        func(*args, **kwargs)
        return func(*args, **kwargs)
    return wrapper_do_twice

@my_decorator
def say_whee():
    print("Whee!")
```

We use `*args, **kwargs` to permit any number of arguments and keyword-arguments.
Moreover, make sure the wrapper function returns the return value of the decorated function.

After being decorated, `say_whee()` has gotten very confused about its identity. It now reports being the wrapper_do_twice() inner function inside the do_twice() decorator. Although technically true, this is not very useful information.

To fix this, decorators should use the `@functools.wraps` decorator, which will preserve information about the original function. 

### Classes as Decorators

The typical way to maintain state is by using classes. 

Recall that the decorator syntax `@my_decorator` is just an easier way of saying `func = my_decorator(func)`. Therefore, if `my_decorator` is a class, it needs to take `func` as an argument in its `.__init__()` method. Furthermore, the class instance needs to be callable so that it can stand in for the decorated function.

For a class instance to be callable, you implement the special .__call__() method.

```python
class Counter:
    def __init__(self, start=0):
        self.count = start

    def __call__(self):
        self.count += 1
        print(f"Current count is {self.count}")
```

The .__call__() method is executed each time you try to call an instance of the class:

```python
counter = Counter()
counter()
# Current count is 1
counter()
# Current count is 2
```

Real world example:

```python
import functools

class CountCalls:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.num_calls = 0

    def __call__(self, *args, **kwargs):
        self.num_calls += 1
        print(f"Call {self.num_calls} of {self.func.__name__!r}")
        return self.func(*args, **kwargs)

@CountCalls
def say_whee():
    print("Whee!")
```

The `.__init__()` method must store a reference to the function and can do any other necessary initialization. The `.__call__()` method will be called instead of the decorated function. It does essentially the same thing as the `wrapper()` function in our earlier examples. Note that you need to use the `functools.update_wrapper()` function instead of `@functools.wraps`.

### Closures

Remember the `nonlocal` keyword. `start` is the so called free variable.

```python
def counter(start):
    def inc(step=1):
        nonlocal start # otherwise not defined
        start += step
        print(start)

    return inc

increment = counter(3)
increment(3) # 6
increment(2) # 8
```

In Python we can inspect the closure with `increment.__code__.co_freevars` and `increment.__closure__`.

### The underscores _

####  Single Leading Underscore: _bar
The underscore prefix (i.e. `_bar`) is meant as a hint to another programmer that a variable or method starting with a single underscore is intended for internal use.

```python
class Test:
    def __init__(self):
        self.foo = 11
        self._bar = 23
```

#### Single Trailing Underscore: class_

Sometimes the most fitting name for a variable is already taken by a keyword. Therefore names like class or def cannot be used as variable names in Python. 

```python
def make_object(name, class):
    pass
# SyntaxError: "invalid syntax"

def make_object(name, class_):
     pass
# OK!
```

#### Double Leading Underscore: __bar -> Name Mangling

A double underscore prefix causes the Python interpreter to **rewrite the attribute name** in order to avoid naming conflicts in subclasses.

This is also called **name mangling** -the interpreter changes the name of the variable in a way that makes it harder to create collisions when the class is extended later.

```python
class Test:
    def __init__(self):
        self.foo = 11
        self._bar = 23
        self.__baz = 23

t = Test()
dir(t) # ['_Test__baz', '__class__', ...,  '_bar', 'foo']
```

### \_\_init\_\_ vs \_\_call\_\_

In Python, functions are first-class objects and instances of Classes (aka Objects), can be treated as if they were functions: pass them to other methods/functions and call them.

- ` __init__` is used to initialize newly created object
- ` __call__` implements function call operator

```python
class Foo:
    def __init__(self, a, b, c):
        # ...

    def __call__(self, d, e, f):
        # ...
        
x = Foo(1, 2, 3) # __init__
x(4, 5, 6) # __call__
```


