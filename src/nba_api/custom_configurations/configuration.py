# based on https://stackoverflow.com/a/51897015/16179502
from nba_api.custom_configurations.cache import CacheCallbacks


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class NBAAPIConfiguration(metaclass=Singleton):
    def __init__(self, proxy: str = '', sleep: int = 0, timeout: int = 25, cache_callbacks: CacheCallbacks = None):
        self.proxy = proxy
        self.sleep = sleep
        self.timeout = timeout
        self.cache_callbacks = cache_callbacks

