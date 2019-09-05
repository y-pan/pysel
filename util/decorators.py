def safe_print_args(*args, **kwargs):
    try:
        print("[[   safe_print => args   ]]")
        print(*args)
        print("[[   safe_print => kwargs   ]]")
        print(', '.join(['{}={!r}'.format(k, v) for k, v in kwargs.items()]))
    except:
        print("[[ --- safe_print => exceptioned :( --- ]]")
        pass

def SuppressExceptionReturnVoid(func):
    def func_wrapper(*args, **kwargs):  # any number of args, kwargs need to be the last continual, 
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"[SuppressExceptionVoid]: {e}")
            safe_print_args(*args, **kwargs)
            pass
    return func_wrapper

def SuppressExceptionReturnNone(func):
    def func_wrapper(*args, **kwargs):  # any number of args, kwargs need to be the last continual, 
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"[SuppressExceptionReturnNone]: {e}")
            safe_print_args(*args, **kwargs)
            return None
    return func_wrapper

def SuppressExceptionReturnZero(func):
    def func_wrapper(*args, **kwargs):  # any number of args, kwargs need to be the last continual, 
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"[SuppressExceptionReturnZero]: {e}")
            safe_print_args(*args, **kwargs)
            return 0
    return func_wrapper

def SuppressExceptionReturnTrue(func):  # True then error
    def func_wrapper(*args, **kwargs):  # any number of args
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"[SuppressExceptionTrue]: {e}")
            safe_print_args(*args, **kwargs)
            return True
    return func_wrapper

def SuppressExceptionReturnEmptyString(func):
    def func_wrapper(*args, **kwargs):  # any number of args
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"[SuppressExceptionEmptyString]: {e}")
            safe_print_args(*args, **kwargs)
            return ''
    return func_wrapper

def SuppressExceptionReturnEmptyStringTuple(func):
    def func_wrapper(*args, **kwargs):  # any number of args
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"[SuppressExceptionEmptyStringTuple]: {e}")
            safe_print_args(*args, **kwargs)
            return '',''
    return func_wrapper
