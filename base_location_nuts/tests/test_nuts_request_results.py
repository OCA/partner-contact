# Copyright 2024 Moduon Team S.L. <info@moduon.team>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from json import dumps

from requests.models import Response

NUTS = [
    {
        "s": {"type": "uri", "value": "http://data.europa.eu/nuts/code/PT"},
        "code": {"type": "literal", "value": "PTa"},
        "region_name": {"type": "literal", "value": "PTa Portugal"},
        "level": {"type": "literal", "value": "0"},
    },
    {
        "s": {"type": "uri", "value": "http://data.europa.eu/nuts/code/PT1"},
        "code": {"type": "literal", "value": "PT1a"},
        "region_name": {"type": "literal", "value": "PT1a Continente"},
        "level": {"type": "literal", "value": "1"},
        "parent": {"type": "literal", "value": "PTa"},
    },
    {
        "s": {"type": "uri", "value": "http://data.europa.eu/nuts/code/ES"},
        "code": {"type": "literal", "value": "ESa"},
        "region_name": {"type": "literal", "value": "ESa España"},
        "level": {"type": "literal", "value": "0"},
    },
    {
        "s": {"type": "uri", "value": "http://data.europa.eu/nuts/code/ES2"},
        "code": {"type": "literal", "value": "ES2a"},
        "region_name": {"type": "literal", "value": "ES2a Noreste"},
        "level": {"type": "literal", "value": "1"},
        "parent": {"type": "literal", "value": "ESa"},
    },
    {
        "s": {"type": "uri", "value": "http://data.europa.eu/nuts/code/ES24"},
        "code": {"type": "literal", "value": "ES24a"},
        "region_name": {"type": "literal", "value": "ES24a Aragón"},
        "level": {"type": "literal", "value": "2"},
        "parent": {"type": "literal", "value": "ES2a"},
    },
    {
        "s": {"type": "uri", "value": "http://data.europa.eu/nuts/code/ES243"},
        "code": {"type": "literal", "value": "ES243a"},
        "region_name": {"type": "literal", "value": "ES243a Zaragoza"},
        "level": {"type": "literal", "value": "3"},
        "parent": {"type": "literal", "value": "ES24a"},
    },
    {
        "s": {"type": "uri", "value": "http://data.europa.eu/nuts/code/ES30"},
        "code": {"type": "literal", "value": "ES30a"},
        "region_name": {"type": "literal", "value": "ES30a Comunidad de Madrid"},
        "level": {"type": "literal", "value": "2"},
        "parent": {"type": "literal", "value": "ES3a"},
    },
    {
        "s": {"type": "uri", "value": "http://data.europa.eu/nuts/code/ES300"},
        "code": {"type": "literal", "value": "ES300a"},
        "region_name": {"type": "literal", "value": "ES300a Madrid"},
        "level": {"type": "literal", "value": "3"},
        "parent": {"type": "literal", "value": "ES30a"},
    },
]


def create_response_ok():
    response = Response()
    response.code = "200"
    response.status_code = 200
    content = {
        "head": {},
        "results": {"distinct": False, "ordered": True, "bindings": NUTS},
    }
    response._content = dumps(content).encode()
    return response


def create_response_error():
    response = Response()
    response.code = "403"
    response.status_code = 403
    content = {
        "head": {},
        "results": {"distinct": False, "ordered": True, "bindings": []},
    }
    response._content = dumps(content).encode()
    return response
