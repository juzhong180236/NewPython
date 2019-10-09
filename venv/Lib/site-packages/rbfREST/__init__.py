# -*- coding: utf-8 -*-

#  Copyright 2019-  DNB
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

# For Python 2
from __future__ import unicode_literals
from __future__ import division
from io import open
from .compat import IS_PYTHON_2, STRING_TYPES

from json import dumps, load, loads
from os import path
from yaml import load as load_yaml

from pygments import highlight, lexers, formatters
from requests.packages.urllib3 import disable_warnings

if IS_PYTHON_2:
    from urlparse import parse_qs, urljoin, urlparse
else:
    from urllib.parse import parse_qs, urljoin, urlparse

from robot.api import logger

from .keywords import Keywords
from .version import __version__


class rbfREST(Keywords):
    """rbfREST is a REST API testing library. 

    = The state =

    The library represents its own state as JSON itself, as an array of objects.
    Together these objects are commonly called instances.

    A single instance always has these three properties:

    - Request data as a JSON object
    - Response data as a JSON object
    - JSON Schema for the above two properties

    For each request-response, as soon as the response has been gotten
    (and the request did not timeout), a new instance is created with these
    properties.

    Request and response schemas are inferred if they are not already
    expected by using expectation keywords. All the validations the library
    implements are based on JSON Schema [http://json-schema.org/draft-07/json-schema-validation.html|draft-07] by default
   

    = The scope =

    All the assertion keywords, `Output` and `Output Schema` are effective
    in the scope of the last instance.

    The scope of the library itself is test suite, meaning the instances
    are persisted in memory until the execution of the test suite is finished,
    regardless whether successfully or not.

    The last request and response is easiest seen with `Output`.
    The output is written to terminal by default, as this is usually faster
    for debugging purposes than finding the right keyword in ``log.html``.

    All instances can be output to a file with `RESTinstances` which can
    be useful for additional logging.
    
    
    = Examples =
    
    HTTP return code validation
    | ${requestHeaders} |  `Load Headers`  | ${EXECDIR}/resources/headers/RequestHeaders.json |
    | `GET` | https://jsonplaceholder.typicode.com/users   | headers=${requestHeaders} |
    | `Assert If Field is Number` | response status   | 200 |
    
    Extract response fields
    | ${requestHeaders} |  `Load Headers`  | ${EXECDIR}/resources/headers/RequestHeaders.json |
    | ${response} | `GET` | https://jsonplaceholder.typicode.com/users?_limit=1   | headers=${requestHeaders} |
    | ${responseField} | `Get Value From Response` | ${response} | $..username |   
    
    Assert response field with value
    | ${requestHeaders} |  `Load Headers`  | ${EXECDIR}/resources/headers/RequestHeaders.json |
    | `GET` | https://jsonplaceholder.typicode.com/users?_limit=1 | headers=${requestHeaders} |
    | `Assert if field is string` | $..username | Bret | 
    
    Assert on multiple API requests
    | ${requestHeaders} |  `Load Headers`  | ${EXECDIR}/resources/headers/RequestHeaders.json |
    | `GET` | https://jsonplaceholder.typicode.com/users?_limit=1   | headers=${requestHeaders} |
    | ${response1} | `Extract Response For Assertions` |
    | `GET` | https://jsonplaceholder.typicode.com/users?_limit=2   | headers=${requestHeaders} |
    | ${response2} | `Extract Response For Assertions` |
    | `Assert if field is string` | $..username | Bret | response=${response1} |
    | `Assert if field is string` | $..username | Antonette | response=${response2} |
    
    """

    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'
    ROBOT_LIBRARY_VERSION = __version__

    # Altogether 24 keywords        context:
    # -------------------------------------------------------
    # 2 setting keywords            next instances
    # 3 expectation keywords        next instances
    # 7 operation keywords          next instance
    # 8 assertion keywords          last instance's schema
    # 4 I/O keywords                the last instance or none
    # -------------------------------------------------------

    def __init__(self, url=None,
                 ssl_verify=True,
                 accept="application/json, */*",
                 content_type="application/json",
                 user_agent="dnb-rf-restapi-library/%s" % (__version__),
                 proxies={},
                 schema={},
                 spec={},
                 instances=[]):
        self.request = {
            'method': None,
            'url': None,
            'scheme': "",
            'netloc': "",
            'path': "",
            'query': {},
            'body': None,
            'headers': {
                'Accept': rbfREST._input_string(accept),
                'Content-Type': rbfREST._input_string(content_type),
                'User-Agent': rbfREST._input_string(user_agent)
            },
            'proxies': rbfREST._input_object(proxies),
            'timeout': [None, None],
            'cert': None,
            'sslVerify': rbfREST._input_ssl_verify(ssl_verify),
            'allowRedirects': True
        }
        if url:
            url = rbfREST._input_string(url)
            if url.endswith('/'):
                url = url[:-1]
            if not url.startswith(("http://", "https://")):
                url = "http://" + url
            url_parts = urlparse(url)
            self.request['scheme'] = url_parts.scheme
            self.request['netloc'] = url_parts.netloc
            self.request['path'] = url_parts.path
        if not self.request['sslVerify']:
            disable_warnings()
        self.schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": url,
            "description": None,
            "default": True,
            "examples": [],
            "type": "object",
            "properties": {
                "request": {
                    "type": "object",
                    "properties": {}
                },
                "response": {
                    "type": "object",
                    "properties": {}
                }
            }
        }
        self.schema.update(self._input_object(schema))
        self.spec = {}
        self.spec.update(self._input_object(spec))
        self.instances = self._input_array(instances)


    @staticmethod
    def log_json(json, header="", also_console=True, sort_keys=False):
        json = dumps(json, ensure_ascii=False, indent=4,
                     separators=(',', ': ' ), sort_keys=sort_keys)
        logger.info("%s\n%s" % (header, json))    # no coloring for log.html
        if also_console:
            json_data = highlight(json,
                                  lexers.JsonLexer(),
                                  formatters.TerminalFormatter())
            logger.console("%s\n%s" % (header, json_data), newline=False)
        return json

    @staticmethod
    def _input_boolean(value):
        if isinstance(value, (bool)):
            return value
        try:
            json_value = loads(value)
            if not isinstance(json_value, (bool)):
                raise RuntimeError("Input is not a JSON boolean: %s" % (value))
        except ValueError:
            raise RuntimeError("Input is not valid JSON: %s" % (value))
        return json_value

    @staticmethod
    def _input_integer(value):
        if isinstance(value, (int)):
            return value
        try:
            json_value = loads(value)
            if not isinstance(json_value, (int)):
                raise RuntimeError("Input is not a JSON integer: %s" % (value))
        except ValueError:
            raise RuntimeError("Input is not valid JSON: %s" % (value))
        return json_value

    @staticmethod
    def _input_number(value):
        if isinstance(value, (float, int)):
            return value
        try:
            json_value = loads(value)
            if not isinstance(json_value, (float, int)):
                raise RuntimeError("Input is not a JSON number: %s" % (value))
        except ValueError:
            raise RuntimeError("Input is not valid JSON: %s" % (value))
        return json_value

    @staticmethod
    def _input_string(value):
        if value == "":
            return ""
        if isinstance(value, STRING_TYPES):
            if not value.startswith('"'):
                value = '"' + value
            if not value.endswith('"'):
                value = value + '"'
        try:
            json_value = loads(value)
            if not isinstance(json_value, STRING_TYPES):
                raise RuntimeError("Input is not a JSON string: %s" % (value))
        except ValueError:
            raise RuntimeError("Input not is valid JSON: %s" % (value))
        return json_value


    @staticmethod
    def _input_object(value):
        if isinstance(value, (dict)):
            return value
        try:
            if path.isfile(value):
                json_value = rbfREST._input_json_from_file(value)
            else:
                json_value = loads(value)
            if not isinstance(json_value, (dict)):
                raise RuntimeError("Input or file has no JSON object: %s" % (
                    value))
        except ValueError:
            raise RuntimeError("Input is not valid JSON or a file: %s" % (
                value))
        return json_value

    @staticmethod
    def _input_array(value):
        if isinstance(value, (list)):
            return value
        try:
            if path.isfile(value):
                json_value = rbfREST._input_json_from_file(value)
            else:
                json_value = loads(value)
            if not isinstance(json_value, (list)):
                raise RuntimeError("Input or file has no JSON array: %s" % (
                    value))
        except ValueError:
            raise RuntimeError("Input is not valid JSON or a file: %s" % (
                value))
        return json_value

    @staticmethod
    def _input_json_from_file(path):
        try:
            with open(path, encoding="utf-8") as file:
                return load(file)
        except IOError as e:
            raise RuntimeError("File '%s' cannot be opened:\n%s" % (path, e))
        except ValueError as e:
            try:
                with open(path, encoding="utf-8") as file:
                    return load_yaml(file)
            except ValueError:
                raise RuntimeError("File '%s' is not valid JSON or YAML:\n%s" %
                    (path, e))

    @staticmethod
    def _input_json_as_string(string):
        return loads(string)

    @staticmethod
    def _input_json_from_non_string(value):
        try:
            return rbfREST._input_json_as_string(dumps(value, ensure_ascii=False))
        except ValueError:
            raise RuntimeError("Input is not valid JSON: %s" % (value))

    @staticmethod
    def _input_client_cert(value):
        if value is None or value == "null":
            return None
        if isinstance(value, STRING_TYPES):
            return value
        if isinstance(value, (list)):
            if len(value) != 2:
                raise RuntimeError("Client cert given as a (Python) list, " +
                    "must have length of 2: %s" % (value))
            return value
        try:
            value = loads(value)
            if not isinstance(value, STRING_TYPES + (list)):
                raise RuntimeError("Input is not a JSON string " +
                    "or a list: %s" + (value))
        except ValueError:
            raise RuntimeError("Input is not a JSON string " +
                "or an array: %s " % (value))
        if isinstance(value, (list)):
            if len(value) != 2:
                raise RuntimeError("Client cert given as a JSON array, " +
                    "must have length of 2: %s" % (value))
        return value

    @staticmethod
    def _input_ssl_verify(value):
        try:
            return rbfREST._input_boolean(value)
        except RuntimeError:
            value = rbfREST._input_string(value)
            if not path.isfile(value):
                raise RuntimeError("SSL verify option is not " +
                    "a Python or a JSON boolean or a path to an existing " +
                    "CA bundle file: %s" % (value))
            return value

    @staticmethod
    def _input_timeout(value):
        if isinstance(value, (int, float)):
            return [value, value]
        if isinstance(value, (list)):
            if len(value) != 2:
                raise RuntimeError("Timeout given as a (Python) list, " +
                    "must have length of 2: %s" % (value))
            return value
        try:
            value = loads(value)
            if not isinstance(value, (int, float, list)):
                raise RuntimeError("Input is not a JSON integer, " +
                    "number or a list: %s" % (value))
        except ValueError:
            raise RuntimeError("Input is not valid JSON: %s" % (value))
        if isinstance(value, (list)):
            if len(value) != 2:
                raise RuntimeError("Timeout given as a JSON array, " +
                    "must have length of 2: %s" % (value))
            else:
                return value
        return [value, value]
