import inspect


def raise_if_handler_not_found(handler,request):
    if not handler:
        raise HandlerNotFoundError(request)


def raise_if_request_none(request):
    if request == None:
        raise InvalidRequest()


def raise_if_handler_is_invalid(handler):
    isfunc = inspect.isfunction(handler)

    func = None
    if isfunc:
        func = handler
    else:
        if hasattr(handler, 'handle'):
            if inspect.isfunction(handler.handle):
                func = handler.handle
            elif inspect.ismethod(handler.handle):
                func = handler.__class__.handle

    if not func:
        raise InvalidHandlerError(func)
    sign = inspect.signature(func)
    params_l = len(sign.parameters.keys())
    if params_l != (1 if isfunc else 2):
        raise InvalidHandlerError(handler)

def raise_if_validator_is_invalid(validator):
    isfunc = inspect.isfunction(validator)

    func = None
    if isfunc:
        func = validator
    else:
        if hasattr(validator, 'validate'):
            if inspect.isfunction(validator.validate):
                func = validator.validate
            elif inspect.ismethod(validator.validate):
                func = validator.__class__.validate

    if not func:
        raise InvalidHandlerError(func)
    sign = inspect.signature(func)
    params_l = len(sign.parameters.keys())
    if params_l != (1 if isfunc else 2):
        raise InvalidHandlerError(validator)

class HandlerNotFoundError(Exception):
    def __init__(self, request):
        self.request = request
        super().__init__("Handler for request '{}' is not registered".format(request))


class InvalidRequest(Exception):
    def __init__(self):
        super().__init__("Request must be an object of defined class")


class InvalidHandlerError(Exception):
    def __init__(self, handler):
        self.handler = handler
        super().__init__("Incorrect handler: '{}'. Handler must be a class, that contains 'handle' method with args:(self,request:SomeRequestType) \
            or must be a function with args:(request:SomeRequestType) \
             where 'request' is object of request class. See examples on git".format(handler))

class InvalidValidatorError(Exception):
    def __init__(self, handler):
        self.handler = handler
        super().__init__("Incorrect validator: '{}'. Validator must be a class, that contains 'validate' method with args:(self,request:SomeRequestType) \
            or must be a function with args:(request:SomeRequestType) \
             where 'request' is object of request class. See examples on git".format(handler))
