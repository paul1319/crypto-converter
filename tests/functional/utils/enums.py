from enum import Enum


class HTTPMethodEnum(str, Enum):
    GET = "GET"


class EndpointsEnum(str, Enum):
    CONVERT = "/api/v1/quotes/convert"
