def run_async(func):
    '''
    Function decorater to make methods run in a thread
    '''
    from threading import Thread
    from functools import wraps

    @wraps(func)
    def async_func(*args, **kwargs):
        func_hl = Thread(target=func, args=args, kwargs=kwargs)
        func_hl.start()
        return func_hl

    return async_func

def attach_method(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator


