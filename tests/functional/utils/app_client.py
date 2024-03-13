from collections.abc import Mapping
from typing import Any

from httpx import AsyncClient, Response

from tests.functional.utils.enums import EndpointsEnum, HTTPMethodEnum


class AppClient:
    def __init__(self, test_client: AsyncClient):
        self._client = test_client

    async def _request(
        self,
        method: HTTPMethodEnum,
        endpoint: EndpointsEnum,
        status_code: int,
        params: Mapping[str, Any] | None = None,
        as_json: bool = True,
    ) -> Response | dict:
        resp = await self._client.request(method=method, url=endpoint, params=params)
        assert resp.status_code == status_code, repr(resp)
        if as_json:
            return resp.json()
        return resp

    async def convert(
        self, amount: float, from_currency: str, to_currency: str, timestamp: int | None = None, status_code: int = 200
    ) -> dict[str, Any]:
        params = {"amount": amount, "from": from_currency, "to": to_currency}
        if timestamp is not None:
            params["timestamp"] = timestamp
        return await self._request(
            method=HTTPMethodEnum.GET,
            endpoint=EndpointsEnum.CONVERT,
            status_code=status_code,
            params=params,
        )
