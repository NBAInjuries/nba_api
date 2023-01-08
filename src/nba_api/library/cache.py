cache = {}


def add_to_cache(parameters, result):
    """
    Add item to cache
    :param parameters: Params of api request
    :param result: Result to be added
    """
    key = _generate_cache_key(parameters)

    cache[key] = result


def retrieve_from_cache(parameters):
    """
    Retrieve item from the cache
    :param parameters: Params of api request
    :return: None if no item in cache, otherwise cache result
    """
    key = _generate_cache_key(parameters)

    return cache.get(key)


def _generate_cache_key(parameters) -> str:
    """
    Build cache key based on method calling nba_api_call_or_retry
    :return: Cache key
    """
    return str(parameters)
