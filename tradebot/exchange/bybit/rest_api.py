import hmac
import hashlib
import aiohttp
import asyncio
import msgspec
import orjson
from typing import Any, Dict, List
from urllib.parse import urljoin, urlencode
from decimal import Decimal

from tradebot.base import ApiClient
from tradebot.exchange.bybit.constants import BybitBaseUrl
from tradebot.exchange.bybit.error import BybitError
from tradebot.exchange.bybit.types import BybitResponse, BybitOrderResponse

class BybitApiClient(ApiClient):
    def __init__(
        self,  
        api_key: str = None,
        secret: str = None,
        timeout: int = 10,
        testnet: bool = False,
    ):
        """
        ### Testnet:
        `https://api-testnet.bybit.com`
        
        ### Mainnet:
        (both endpoints are available):
        `https://api.bybit.com`
        `https://api.bytick.com`
        
        ### Important:
        Netherland users: use `https://api.bybit.nl` for mainnet
        Hong Kong users: use `https://api.byhkbit.com` for mainnet
        Turkey users: use `https://api.bybit-tr.com` for mainnet
        Kazakhstan users: use `https://api.bybit.kz` for mainnet  
        """
        
        super().__init__(
            api_key=api_key,
            secret=secret,
            timeout=timeout,
        )
        self._recv_window = 5000
        
        if testnet:
            self._base_url = BybitBaseUrl.TESTNET.value
        else:
            self._base_url = BybitBaseUrl.MAINNET_1.value
        
        self._headers = {
            "Content-Type": "application/json",
            "User-Agent": "TradingBot/1.0",
            "X-BAPI-API-KEY": api_key,
        }
        
        self._response_decoder = msgspec.json.Decoder(BybitResponse)
        self._order_response_decoder = msgspec.json.Decoder(BybitOrderResponse)
        

    def _generate_signature(self, payload: str) -> List[str]:
        timestamp = str(self._clock.timestamp_ms())

        param = str(timestamp) + self._api_key + str(self._recv_window) + payload
        hash = hmac.new(
            bytes(self._secret, "utf-8"), param.encode("utf-8"), hashlib.sha256
        )
        signature = hash.hexdigest()
        return [signature, timestamp]
    
    async def _fetch(
        self,
        method: str,
        base_url: str,
        endpoint: str,
        payload: Dict[str, Any] = None,
        signed: bool = False,
    ):
        url = urljoin(base_url, endpoint)
        payload = payload or {}
        
        payload_str = (
            urlencode(payload) if method == "GET" 
            else orjson.dumps(payload).decode("utf-8")
        )

        headers = self._headers
        if signed:
            signature, timestamp = self._generate_signature(payload_str)
            headers = {
                **headers,
                "X-BAPI-TIMESTAMP": timestamp,
                "X-BAPI-SIGN": signature, 
                "X-BAPI-RECV-WINDOW": str(self._recv_window),
            }

        if method == "GET":
            url += f"?{payload_str}"
            payload_str = None
        
        try:
            self._log.debug(f"Request: {url} {payload_str}")
            response = await self._session.request(
                method=method,
                url=url,
                headers=headers,
                data=payload_str,
            )
            raw = await response.read()
            if response.status >= 400:
                raise BybitError(
                    code=response.status,
                    message=orjson.loads(raw) if raw else None,
                )
            bybit_response: BybitResponse = self._response_decoder.decode(raw)
            if bybit_response.retCode == 0:
                return raw
            else:
                raise BybitError(
                    code=bybit_response.retCode,
                    message=bybit_response.retMsg,
                )
        except aiohttp.ClientError as e:
            self._log.error(f"Client Error {method} Url: {url} {e}")
            raise
        except asyncio.TimeoutError:
            self._log.error(f"Timeout {method} Url: {url}")
            raise
        except Exception as e:
            self._log.error(f"Error {method} Url: {url} {e}")
            raise
    
    async def post_v5_order_create(self, category: str, symbol: str, side: str, order_type: str, qty: Decimal, **kwargs) -> BybitOrderResponse:
        """
        https://bybit-exchange.github.io/docs/v5/order/create-order
        """
        endpoint = "/v5/order/create"
        payload = {
            "category": category,
            "symbol": symbol,
            "side": side,
            "orderType": order_type,
            "qty": str(qty),
            **kwargs,
        }
        raw = await self._fetch("POST", self._base_url, endpoint, payload, signed=True)
        return self._order_response_decoder.decode(raw)
        
    async def post_v5_order_cancel(self, category: str, symbol: str, **kwargs) -> BybitOrderResponse:
        """
        https://bybit-exchange.github.io/docs/v5/order/cancel-order
        """
        endpoint = "/v5/order/cancel"
        payload = {
            "category": category,
            "symbol": symbol,
            **kwargs,
        }
        raw = await self._fetch("POST", self._base_url, endpoint, payload, signed=True)
        return self._order_response_decoder.decode(raw)

    def raise_error(self, raw: bytes, status: int, headers: Dict[str, Any]):
        pass
