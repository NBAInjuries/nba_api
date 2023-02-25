import json
from typing import Union

from nba_api.custom_configurations.cache import ParametersType
from nba_api.custom_configurations.configuration import NBAAPIConfiguration


def add_to_cache(endpoint: str, parameters: ParametersType, data):
    """
    Add item to cache
    :param endpoint: Endpoint
    :param parameters: Params of api request
    :param data: Result to be added
    """
    # only add valid results to cache
    try:
        data.get_dict()
    except Exception as e:
        raise e

    cache_callbacks = NBAAPIConfiguration().cache_callbacks

    # no cache setup
    if not cache_callbacks:
        return

    cache_entity = cache_callbacks.does_entity_exist(endpoint, parameters)
    data = _build_cache_payload(data)

    # entity does not exist, create entity and return its data
    if not cache_entity:
        cache_callbacks.create_entity(endpoint, parameters, data)
        return

    # entity exists but it is no longer valid. needs an update
    cache_callbacks.update_entity(cache_entity, parameters, data)


def retrieve_from_cache(endpoint: str, parameters: ParametersType):
    """
    Retrieve item from the cache
    :param endpoint: Endpoint
    :param parameters: Params of api request
    :return: None if no item in cache, otherwise cache result
    """
    cache_callbacks = NBAAPIConfiguration().cache_callbacks

    # no cache setup
    if not cache_callbacks:
        return None

    cache_entity = cache_callbacks.does_entity_exist(endpoint, parameters)

    # entity does not exist in cache
    if not cache_entity:
        return None

    # entity exists and does not need a refresh
    if cache_callbacks.is_entity_valid(cache_entity):
        return _retrieve_cache_payload(cache_entity.data)

    # entity exists but is not valid, it will be refreshed after this call
    return None


def _build_cache_payload(data) -> dict:
    """
    Apply cache payload in format we will store it in
    :param data: API result
    :return: Formatted payload
    """
    return {
        'url': data._url,
        'status_code': data._status_code,
        'response': data.get_dict()
    }


def _retrieve_cache_payload(payload) -> Union[dict, None]:
    """
    Retrieve cache result in a format that nba_api will understand it
    :param payload: Result from cache
    :return: Formatted payload
    """
    if not payload:
        return None

    payload['response'] = json.dumps(payload['response'])
    return payload
