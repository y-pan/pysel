def SuppressExceptionVoid(func):
    def func_wrapper(*args, **kwargs):  # any number of args, kwargs need to be the last continual, 
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"[SuppressExceptionVoid]: {e}")
            pass
    return func_wrapper

def SuppressExceptionTrue(func):  # True then error
    def func_wrapper(*args, **kwargs):  # any number of args
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"[SuppressExceptionTrue]: {e}")
            return True
    return func_wrapper

def SuppressExceptionEmptyString(func):
    def func_wrapper(*args, **kwargs):  # any number of args
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"[SuppressExceptionEmptyString]: {e}")
            return ''
    return func_wrapper

def SuppressExceptionEmptyStringTuple(func):
    def func_wrapper(*args, **kwargs):  # any number of args
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"[SuppressExceptionEmptyStringTuple]: {e}")
            return '',''
    return func_wrapper