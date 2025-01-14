import os
import json
import random
import time

import requests

from urllib.parse import quote_plus

from nba_api.library.cache import retrieve_from_cache, add_to_cache
from nba_api.custom_configurations.configuration import NBAAPIConfiguration

try:
    from nba_api.library.debug.debug import DEBUG
except ImportError:
    DEBUG = False


try:
    from nba_api.library.debug.debug import DEBUG_STORAGE
except ImportError:
    DEBUG_STORAGE = False


try:
    from nba_api.library.debug.debug import PROXY
except ImportError:
    PROXY = ''


if DEBUG:
    from hashlib import md5
    print('DEBUG MODE')

# for when we error out
class NBAAPIReturnException(Exception):
    pass


class NBAResponse:
    def __init__(self, response, status_code, url):
        self._response = response
        self._status_code = status_code
        self._url = url

    def get_response(self):
        return self._response

    def get_dict(self):
        return json.loads(self._response)

    def get_json(self):
        return json.dumps(self.get_dict())

    def valid_json(self):
        try:
            self.get_dict()
        except ValueError:
            return False
        return True

    def get_url(self):
        return self._url


class NBAHTTP:

    nba_response = NBAResponse

    base_url = None

    parameters = None

    headers = None

    def clean_contents(self, contents):
        return contents

    def send_api_request(self, endpoint, parameters, referer=None, proxy=None, headers=None, timeout=None, raise_exception_on_error=False):
        if not self.base_url:
            raise Exception('Cannot use send_api_request from _HTTP class.')
        base_url = self.base_url.format(endpoint=endpoint)
        endpoint = endpoint.lower()
        self.parameters = parameters
        configurations: NBAAPIConfiguration = NBAAPIConfiguration()

        if headers is None:
            request_headers = self.headers
        else:
            request_headers = headers

        if referer:
            request_headers['Referer'] = referer

        request_proxy = configurations.proxy

        timeout = configurations.timeout

        proxies = None
        if request_proxy:
            proxies = {
                "http": request_proxy,
                "https": request_proxy,
            }

        url = None
        status_code = None
        contents = None

        # Sort parameters by key... for some reason this matters for some requests...
        parameters = sorted(parameters.items(), key=lambda kv: kv[0])

        in_cache = retrieve_from_cache(endpoint=endpoint, parameters=parameters)
        if in_cache:
            return self.nba_response(**in_cache)

        if DEBUG and DEBUG_STORAGE:
            print(endpoint, parameters)
            directory_name = 'debug_storage'
            parameter_string = '&'.join('{}={}'.format(key, '' if val is None else quote_plus(str(val))) for key, val in parameters)
            url = "{}?{}".format(base_url, parameter_string)
            print(url)
            file_name = "{}-{}.txt".format(endpoint, md5(parameter_string.encode('utf-8')).hexdigest())
            file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'debug', directory_name)
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            file_path = os.path.join(file_path, file_name)
            print(file_name, os.path.isfile(file_path))
            if os.path.isfile(file_path):
                f = open(file_path, 'r')
                contents = f.read()
                f.close()
                print('loading from file...')

        if not contents:
            if configurations.sleep:
                time.sleep(configurations.sleep)

            response = requests.get(url=base_url, params=parameters, headers=request_headers, proxies=proxies, timeout=timeout)
            url = response.url
            status_code = response.status_code
            contents = response.text

        contents = self.clean_contents(contents)
        if DEBUG and DEBUG_STORAGE:
            f = open(file_path, 'w')
            f.write(contents)
            f.close()
            print(url)

        if status_code != 200:
            filled_in_params = list(
                filter(lambda tup: tup[1] and not tup[1] == "", parameters)
            )
            pretty_parameters = [f"{value[0]}:{value[1]}" for value in filled_in_params]

            raise NBAAPIReturnException(f"Error code '{status_code}' with endpoint '{endpoint}' and parameters"
                                        f" '{pretty_parameters}'")

        data = self.nba_response(response=contents, status_code=status_code, url=url)

        if raise_exception_on_error and not data.valid_json():
            raise Exception('InvalidResponse: Response is not in a valid JSON format.')

        add_to_cache(endpoint=endpoint, parameters=parameters, data=data)

        return data
