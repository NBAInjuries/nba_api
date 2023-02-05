# based on https://stackoverflow.com/a/51897015/16179502

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class NBAApi(metaclass=Singleton):
    def __init__(self, proxy: str = '', sleep: int = 0, timeout: int = 25, cache_path: str = None):
        self.proxy = proxy
        self.sleep = sleep
        self.timeout = timeout
        self.cache_path = cache_path

