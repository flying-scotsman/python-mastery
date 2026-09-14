from functools import wraps

def logformat(fmt):
    def logged(func):
        print(f'Adding logging to {func.__name__}')
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(fmt.format(func=func))
            return func(*args, **kwargs)
        return wrapper
    return logged

logged = logformat("Calling {func.__name__}")

class Spam:
    @logged
    def instance_method(self):
        pass

    @logged
    @classmethod
    def class_method(cls):
        pass

    @logged
    @staticmethod
    def static_method():
        pass

    @logged
    @property
    def property_method(self):
        pass