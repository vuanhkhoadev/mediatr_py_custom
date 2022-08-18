import inspect
import asyncio
from typing import Any, Awaitable, Callable, Optional, TypeVar, Generic, Union

from mediatr.exceptions import raise_if_handler_not_found, raise_if_request_none, raise_if_handler_is_invalid, raise_if_validator_is_invalid


__handlers__ = {}
__validators__ = {}
TResponse = TypeVar('TResponse')
class GenericQuery(Generic[TResponse]):
    pass

@staticmethod
def default_handler_class_manager(HandlerCls:type,is_behavior:bool=False):
    return HandlerCls()

def extract_request_handler_type(handler) -> type:
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

    raise_if_handler_is_invalid(handler)

    sign = inspect.signature(func)
    items = list(sign.parameters)
    return sign.parameters.get(items[0]).annotation if isfunc else sign.parameters.get(items[1]).annotation


def extract_request_validator_type(handler) -> type:
    isfunc = inspect.isfunction(handler)

    func = None
    if isfunc:
        func = handler
    else:
        if hasattr(handler, 'validate'):
            if inspect.isfunction(handler.validate):
                func = handler.validate
            elif inspect.ismethod(handler.validate):
                func = handler.__class__.validate

    raise_if_validator_is_invalid(handler)

    sign = inspect.signature(func)
    items = list(sign.parameters)
    return sign.parameters.get(items[0]).annotation if isfunc else sign.parameters.get(items[1]).annotation

async def __return_await__(result):
    return await result if inspect.isawaitable(result) or inspect.iscoroutine(result) else result


class Mediator():
    """Class of mediator as entry point to send requests and get responses"""

    handler_class_manager = default_handler_class_manager
    
    def __init__(self, handler_class_manager: Callable = None):
        if handler_class_manager:
            self.handler_class_manager = handler_class_manager

    async def send_async(self: Union["Mediator",GenericQuery[TResponse]], request: Optional[GenericQuery[TResponse]] = None) -> Awaitable[TResponse]:
        self1 = Mediator if not request else self
        request = request or self

        raise_if_request_none(request)
        handler = None
        validator = None
        if __handlers__.get(request.__class__):
            handler = __handlers__[request.__class__]
        elif __handlers__.get(request.__class__.__name__):
            handler =__handlers__[request.__class__.__name__]

        if __validators__.get(request.__class__):
            validator = __validators__[request.__class__]
        elif __validators__.get(request.__class__.__name__):
            validator = __validators__[request.__class__.__name__]

        raise_if_handler_not_found(handler,request)
        handler_func = None
        validator_func = None
        handler_obj = None

        handler_obj = self1.handler_class_manager(handler)
        handler_func = handler_obj.handle

        if validator:
            validator_func = handler_obj.validate
            validator_result = asyncio.create_task(validator_func(request))
            await validator_result

        return await handler_func(request)
             
    @staticmethod
    def register_handler(handler):
        """Append handler function or class to global handlers dictionary"""
        request_type = extract_request_handler_type(handler)
        if not __handlers__.get(request_type):
            __handlers__[request_type] = handler

    @staticmethod
    def register_validator(validator):
        """Append handler function or class to global handlers dictionary"""
        request_type = extract_request_validator_type(validator)
        if not __validators__.get(request_type):
            __validators__[request_type] = validator

    @staticmethod
    def handler(handler):
        """Append handler function or class to global handlers dictionary"""
        Mediator.register_handler(handler)
        return handler

    @staticmethod
    def validator(validator):
        """Append handler function or class to global handlers dictionary"""
        Mediator.register_validator(validator)
        return validator




