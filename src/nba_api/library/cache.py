cache = {}


def add_to_cache(parameters, endpoint, result):
    """
    Add item to cache
    :param parameters: Params of api request
    :param endpoint: Endpoint
    :param result: Result to be added
    """
    # only add valid results to cache
    try:
        result.get_dict()
    except Exception as e:
        raise e

    key = _generate_cache_key(parameters, endpoint)

    cache[key] = result


def retrieve_from_cache(parameters, endpoint):
    """
    Retrieve item from the cache
    :param parameters: Params of api request
    :param endpoint: Endpoint
    :return: None if no item in cache, otherwise cache result
    """
    key = _generate_cache_key(parameters, endpoint)

    return cache.get(key)


def _generate_cache_key(parameters, endpoint) -> str:
    """
    Build cache key based on method calling nba_api_call_or_retry
    :return: Cache key
    """
    return endpoint + str(parameters)
