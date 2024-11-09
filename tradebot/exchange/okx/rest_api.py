from tradebot.base import ApiClient
from tradebot.exchange.okx import OkxAccountType
import msgspec
from tradebot.exchange.okx.types import (
    OKXPlaceOrderResponse,
    OKXCancelOrderResponse,
)
from typing import Dict, Any
import orjson
from tradebot.exchange.okx.error import OKXHttpError
import hmac
import base64
import asyncio
import aiohttp
from datetime import datetime, timezone


class OkxApiClient(ApiClient):
    def __init__(
        self,
        api_key: str = None,
        secret: str = None,
        passphrase: str = None,
        testnet: bool = False,
        timeout: int = 10,
    ):
        super().__init__(
            api_key=api_key,
            secret=secret,
            timeout=timeout,
        )
        self._base_url = "https://aws.okx.com"
        self._passphrase = passphrase
        self._testnet = testnet
        self._place_order_decoder = msgspec.json.Decoder(OKXPlaceOrderResponse)
        self._cancel_order_decoder = msgspec.json.Decoder(OKXCancelOrderResponse)

        self._headers = {
            "Content-Type": "application/json",
            "User-Agent": "TradingBot/1.0",
        }

    def raise_error(self, raw: bytes, status: int, headers: Dict[str, Any]):
        if 400 <= status < 500:
            raise OKXHttpError(status, orjson.loads(raw), headers)
        elif status >= 500:
            raise OKXHttpError(status, orjson.loads(raw), headers)

    async def place_order(
        self, instId: str, tdMode: str, side: str, ordType: str, sz: str, **kwargs
    ) -> OKXPlaceOrderResponse:
        """
        Place a new order
        https://www.okx.com/docs-v5/en/#rest-api-trade-place-order
        """
        endpoint = "/api/v5/trade/order"
        payload = {
            "instId": instId,
            "tdMode": tdMode,
            "side": side,
            "ordType": ordType,
            "sz": sz,
            **kwargs,
        }
        raw = await self._fetch("POST", endpoint, payload=payload, signed=True)
        return self._place_order_decoder.decode(raw)

    async def cancel_order(
        self, instId: str, ordId: str = None, clOrdId: str = None
    ) -> OKXCancelOrderResponse:
        """
        Cancel an existing order
        https://www.okx.com/docs-v5/en/#rest-api-trade-cancel-order
        """
        endpoint = "/api/v5/trade/cancel-order"
        payload = {"instId": instId}
        if ordId:
            payload["ordId"] = ordId
        if clOrdId:
            payload["clOrdId"] = clOrdId

        raw = await self._fetch("POST", endpoint, payload=payload, signed=True)
        return self._cancel_order_decoder.decode(raw)

    def _generate_signature(self, message: str) -> str:
        mac = hmac.new(
            bytes(self._secret, encoding="utf8"),
            bytes(message, encoding="utf-8"),
            digestmod="sha256",
        )
        return base64.b64encode(mac.digest()).decode()

    async def get_signature(
        self, ts: str, method: str, request_path: str, payload: Dict[str, Any] = None
    ) -> str:
        body = ""
        if payload:
            body = orjson.dumps(payload).decode()

        sign_str = f"{ts}{method}{request_path}{body}"
        signature = self._generate_signature(sign_str)
        return signature

    def get_timestamp(self) -> str:
        return (
            datetime.now(timezone.utc)
            .isoformat(timespec="milliseconds")
            .replace("+00:00", "Z")
        )

    async def get_headers(
        self, ts: str, method: str, request_path: str, payload: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        headers = self._headers
        signature = await self.get_signature(ts, method, request_path, payload)
        headers.update(
            {
                "OK-ACCESS-KEY": self._api_key,
                "OK-ACCESS-SIGN": signature,
                "OK-ACCESS-TIMESTAMP": ts,
                "OK-ACCESS-PASSPHRASE": self._passphrase,
            }
        )
        if self._testnet:
            headers["x-simulated-trading"] = "1"
        return headers

    async def _fetch(
        self,
        method: str,
        endpoint: str,
        params: Dict[str, Any] = None,
        payload: Dict[str, Any] = None,
        signed: bool = False,
    ) -> bytes:
        url = f"{self._base_url}{endpoint}"
        request_path = endpoint
        headers = self._headers
        timestamp = self.get_timestamp()

        if params:
            query_string = "&".join([f"{k}={v}" for k, v in sorted(params.items())])
            request_path = f"{endpoint}?{query_string}"
            url = f"{url}?{query_string}"

        if signed and self._api_key:
            headers = await self.get_headers(timestamp, method, request_path, payload)

        try:
            response = await self._session.request(
                method=method,
                url=url,
                headers=headers,
                data=orjson.dumps(payload) if payload else None,
            )
            raw = await response.read()
            self.raise_error(raw, response.status, response.headers)
            return raw
        except aiohttp.ClientError as e:
            self._log.error(f"Client Error {method} Url: {url} {e}")
            raise
        except asyncio.TimeoutError:
            self._log.error(f"Timeout {method} Url: {url}")
            raise
        except Exception as e:
            self._log.error(f"Error {method} Url: {url} {e}")
            raise
