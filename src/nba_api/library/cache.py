import ast
import json
import os
from typing import Union, Dict

import pandas as pd

from nba_api.nba_api import NBAApi

local_cache = {}

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
    configurations: NBAApi = NBAApi()

    try:
        if configurations.cache_path:
            _to_json_cache(key, result)
        else:
            local_cache[key] = _build_cache_payload(result)
    except Exception as e:
        print(f"Cache failure with exception: {e}")


def retrieve_from_cache(parameters, endpoint):
    """
    Retrieve item from the cache
    :param parameters: Params of api request
    :param endpoint: Endpoint
    :return: None if no item in cache, otherwise cache result
    """
    key = _generate_cache_key(parameters, endpoint)
    configurations: NBAApi = NBAApi()

    try:
        if configurations.cache_path:
            return _get_from_json_cache(key)
        else:
            return _retrieve_cache_payload(local_cache.get(key))
    except Exception as e:
        print(f"Cache failure with exception: {e}")
        return None


def _generate_cache_key(parameters, endpoint) -> str:
    """
    Build cache key based on method calling nba_api_call_or_retry
    :return: Cache key
    """
    parameters = list(filter(lambda tup: not tup[1] == '', parameters))
    return endpoint + ':' + str(parameters)


def _generate_json_cache_path(key: str) -> str:
    """
    Generate the path where json file will be located
    :param key: Key of cache
    :return: Json path
    """
    configurations: NBAApi = NBAApi()

    return configurations.cache_path + f'{key}.json'


def _json_file_exists(path: str) -> bool:
    """
    If the provided path already exists
    :param path: Json path
    :return: True if the path exists
    """
    return os.path.exists(path)


def _to_json_cache(key: str, result):
    """
    Write result to persistent json cache
    :param key: Cache key
    :param result: Result of API
    """
    path = _generate_json_cache_path(key)

    # we've already written this file, don't overwrite
    if _json_file_exists(path):
        return

    file_content = _build_cache_payload(result)

    with open(path, 'w') as cache_file:
        json.dump(file_content, cache_file, indent=2)


def _get_from_json_cache(key: str) -> Union[Dict, None]:
    """
    Retrieve item from persistent json cache
    :param key: Cache key
    :return: Csv converted to pandas object
    """
    path = _generate_json_cache_path(key)

    if not _json_file_exists(path):
        return None

    with open(path, "r") as cache_file:
        file_content = json.load(cache_file)

    file_content = _retrieve_cache_payload(file_content)

    return file_content


def _build_cache_payload(result) -> Dict:
    """
    Apply cache payload in format we will store it in
    :param result: API result
    :return: Formatted payload
    """
    return {
        'url': result._url,
        'status_code': result._status_code,
        'response': result.get_dict()
    }


def _retrieve_cache_payload(payload) -> Union[Dict, None]:
    """
    Retrieve cache result in a format that nba_api will understand it
    :param payload: Result from cache
    :return: Formatted payload
    """
    if not payload:
        return None

    payload['response'] = json.dumps(payload['response'])
    return payload
