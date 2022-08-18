# mediatr_py

[![PyPI](https://img.shields.io/pypi/v/mediatr-ez)](https://pypi.org/project/mediatr-ez)
[![Python](https://img.shields.io/pypi/pyversions/mediatr-ez)](https://pypi.org/project/mediatr-ez) 
[![Downloads](https://img.shields.io/pypi/dm/mediatr-ez)](https://pypi.org/project/mediatr-ez) 

<img src="https://ca.slack-edge.com/TEDLBFWD9-U01QFV0159R-2593823811d3-512" alt="Alt text" title="Optional title">

<a href="https://www.buymeacoffee.com/khoavadevs" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>

This is an async implementation of Mediator pattern with pipline behaviors.

It is a port of [Mediatr](https://github.com/jbogard/MediatR) from .Net C#

Requirements:
* Python >= 3.8

## Usage:

install [mediatr](https://pypi.org/project/mediatr-ez/):

`pip install mediatr-ez`

### Define your request class

```py

class GetArrayQuery():
    def __init__(self,items_count:int):
        self.items_count = items_count

```

### Define your handler class or function

```py
import Mediator from mediatr

@Mediator.handler
async def get_array_handler(request:GetArrayQuery):
    items = list()
    for i in range(0, request.items_count):
        items.append(i)
    return items
    
# or just Mediator.register_handler(get_array_handler)
    
```

or class:

```py
@Mediator.handler
class GetArrayQueryHandler():
    def handle(self,request:GetArrayQuery):
        items = list()
        for i in range(0, request.items_count):
            items.append(i)
        return items
        
# or just Mediator.register_handler(GetArrayQueryHandler)
```

### Define your validator class or function

```py
import Mediator from mediatr

@Mediator.validator
async def get_array_validator(request:GetArrayQuery):
    if request.items_count > 0:
        ...etc
    else: 
        raise Exception("Sorry, items_count number below zero")
    
# or just Mediator.register_validator(get_array_handler)
    
```

or class:

```py
@Mediator.validator
class GetArrayQueryValidator():
    def validate(self,request:GetArrayQuery):
        if request.items_count > 0:
        ...etc
    else: 
        raise Exception("Sorry, items_count number below zero")
        
# or just Mediator.register_validator(GetArrayQueryHandler)
```

### Run mediator

```py
import Mediator from mediatr

mediator = Mediator()

request = GetArrayQuery(5)

result = await mediator.send_async(request)

# result = mediator.send(request) in synchronous mode

print(result) // [0,1,2,3,4]

```

> If you are using synchronous `mediator.send(request)` method, try to define synchronous handlers and behaviors
>
> In another case use `asyncio` module for manual manage of event loop in synchronous code


### Run mediator statically, without instance

```py
import Mediator from mediatr

request = GetArrayQuery(5)

result = await Mediator.send_async(request)
# or:
result = Mediator.send(request) #in synchronous mode. Async handlers and behaviors will not blocking!

print(result) // [0,1,2,3,4]

```

Note that instantiation of `Mediator(handler_class_manager = my_manager_func)` is useful if you have custom handlers creation. For example using an injector.
By default class handlers are instantiated with simple init:  `SomeRequestHandler()`. handlers or behaviors as functions are executed directly. 


## Using custom handler factory for handlers as classes

If your handlers registered as functions, it just executes them.

In case with handlers, declared as classes with method `handle` Mediator uses function, that instantiates handlers.

```py
def default_handler_class_manager(HandlerCls:type,is_behavior:bool=False):
    return HandlerCls()

```


For example, if you want to instantiate them with dependency injector or custom, pass your own factory function to Mediator:

```py
def my_class_handler_manager(handler_class, is_behavior=False):
    
    if is_behavior:
        # custom logic
        pass

    return injector.get(handler_class)

mediator = Mediator(handler_class_manager=my_class_handler_manager)

```
PS:


The `next` function in behavior is `async`, so if you want to take results or if your behavior is async, use `middle_results = await next()`


Handler may be async too, if you need.

## Using with generic typing support (version >= 1.2):

```py

from mediatr import Mediator, GenericQuery


class UserModel(BaseModel): # For example sqlalchemy ORM entity
    id = Column(String,primary_key=True)
    name = Column(String)


class FetchUserQuery(GenericQuery[UserModel])
    def __init__(self,user_id:str):
        self.user_id = user_id


mediator = Mediator()

request = FetchUserQuery(user_id = "123456")

user = mediator.send(request) # type of response will be a UserModel


# -------------------------------------------------------------

@Mediator.handler
class FetchUserQueryHandler():

    def handle(self, request:FetchUserQuery):
        db_session = Session() #sqlalchemy session
        return db_session.query(UserModel).filter(UserModel.id == request.user_id).one()

# or handler as simple function:
@Mediator.handler
def fetch_user_query_handler(request:FetchUserQuery):
    db_session = Session() #sqlalchemy session
    return db_session.query(UserModel).filter(UserModel.id == request.user_id).one()


```

Please give a star if the library is useful for you :smiley:
