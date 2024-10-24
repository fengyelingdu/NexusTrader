import time
import hmac
import base64
import asyncio

from typing import Literal
from typing import Any, Dict
from decimal import Decimal
from typing import Callable

from asynciolimiter import Limiter


from tradebot.types import (
    BookL1,
    Trade,
)
from tradebot.entity import EventSystem
from tradebot.base import WSManager
from tradebot.constants import EventType


from tradebot.exchange.okx.constants import STREAM_URLS
from tradebot.exchange.okx.constants import OkxAccountType


class OkxWSClient(WSManager):
    def __init__(
        self,
        account_type: OkxAccountType,
        handler: Callable[..., Any],
        api_key: str = None,
        secret: str = None,
        passphrase: str = None,
    ):
        self._api_key = api_key
        self._secret = secret
        self._passphrase = passphrase
        self._account_type = account_type
        if self.is_private:
            url = f"{STREAM_URLS[account_type]}/v5/private"
            self._authed = False
        else:
            url = f"{STREAM_URLS[account_type]}/v5/public"
        super().__init__(url, limiter=Limiter(2 / 1), handler=handler)

    @property
    def is_private(self):
        return (
            self._api_key is not None
            or self._secret is not None
            or self._passphrase is not None
        )

    def _get_auth_payload(self):
        timestamp = int(time.time())
        message = str(timestamp) + "GET" + "/users/self/verify"
        mac = hmac.new(
            bytes(self._secret, encoding="utf8"),
            bytes(message, encoding="utf-8"),
            digestmod="sha256",
        )
        d = mac.digest()
        sign = base64.b64encode(d)
        if self._api_key is None or self._passphrase is None or self._secret is None:
            raise ValueError("API Key, Passphrase, or Secret is missing.")
        arg = {
            "apiKey": self._api_key,
            "passphrase": self._passphrase,
            "timestamp": timestamp,
            "sign": sign.decode("utf-8"),
        }
        payload = {"op": "login", "args": [arg]}
        return self._encoder.encode(payload)

    async def _auth(self):
        if not self._authed:
            self._send(self._get_auth_payload())
            self._authed = True
            await asyncio.sleep(5)

    async def _subscribe(self, params: dict, subscription_id: str, auth: bool = False):
        if subscription_id not in self._subscriptions:
            await self.connect()
            await self._limiter.wait()

            if auth:
                await self._auth()

            payload = {
                "op": "subscribe",
                "args": [params],
            }
            self._subscriptions[subscription_id] = payload
            self._send(payload)
        else:
            print(f"Already subscribed to {subscription_id}")

    async def subscribe_order_book(
        self,
        symbol: str,
        channel: Literal[
            "books", "books5", "bbo-tbt", "books-l2-tbt", "books50-l2-tbt"
        ],
    ):
        """
        https://www.okx.com/docs-v5/en/#order-book-trading-market-data-ws-order-book-channel
        """
        params = {"channel": channel, "instId": symbol}
        subscription_id = f"{channel}.{symbol}"
        await self._subscribe(params, subscription_id)

    async def subscribe_trade(self, symbol: str):
        """
        https://www.okx.com/docs-v5/en/#order-book-trading-market-data-ws-all-trades-channel
        """
        params = {"channel": "trades", "instId": symbol}
        subscription_id = f"trade.{symbol}"
        await self._subscribe(params, subscription_id)

    async def subscribe_candlesticks(
        self,
        symbol: str,
        interval: Literal[
            "1s",
            "1m",
            "3m",
            "5m",
            "15m",
            "30m",
            "1H",
            "2H",
            "4H",
            "6H",
            "12H",
            "1D",
            "1W",
            "1M",
        ],
    ):
        """
        https://www.okx.com/docs-v5/en/#order-book-trading-market-data-ws-candlesticks-channel
        """
        channel = f"candle{interval}"
        params = {"channel": channel, "instId": symbol}
        subscription_id = f"{channel}.{symbol}"
        await self._subscribe(params, subscription_id)

    async def subscribe_account(self):
        params = {"channel": "account"}
        subscription_id = "account"
        await self._subscribe(params, subscription_id, auth=True)

    async def subscribe_positions(
        self, inst_type: Literal["MARGIN", "SWAP", "FUTURES", "OPTION", "ANY"] = "ANY"
    ):
        subscription_id = f"position.{inst_type}"
        params = {"channel": "positions", "instType": inst_type}
        await self._subscribe(params, subscription_id, auth=True)

    async def subscribe_orders(
        self, inst_type: Literal["MARGIN", "SWAP", "FUTURES", "OPTION", "ANY"] = "ANY"
    ):
        subscription_id = f"orders.{inst_type}"
        params = {"channel": "orders", "instType": inst_type}
        await self._subscribe(params, subscription_id, auth=True)

    async def subscrbe_fills(self):
        subscription_id = "fills"
        params = {"channel": "fills"}
        await self._subscribe(params, subscription_id, auth=True)

    async def _resubscribe(self):
        if self.is_private:
            self._authed = False
            await self._auth()
        for _, payload in self._subscriptions.items():
            await self._limiter.wait()
            self._send(payload)


class OkxWSManager(WSManager):
    def __init__(
        self,
        account_type: OkxAccountType,
        market: Dict[str, Any],
        market_id: Dict[str, Any],
        api_key: str = None,
        secret: str = None,
        passphrase: str = None,
    ):
        if api_key or secret or passphrase:
            url = f"{STREAM_URLS[account_type]}/v5/private"
        else:
            url = f"{STREAM_URLS[account_type]}/v5/public"

        super().__init__(url, limiter=Limiter(2 / 1), handler=self._callback)
        self._exchange_id = "okx"
        self._market = market
        self._market_id = market_id
        self._api_key = api_key
        self._secret = secret
        self._passphrase = passphrase

    async def subscribe_book_l1(self, symbol: str):
        channel = "bbo-tbt"

        market = self._market.get(symbol, None)
        symbol = market["id"] if market else symbol

        subscription_id = f"{channel}.{symbol}"

        if subscription_id not in self._subscriptions:
            await self._limiter.wait()
            payload = {
                "op": "subscribe",
                "args": [{"channel": channel, "instId": symbol}],
            }
            self._subscriptions[subscription_id] = payload
            self._send(payload)
        else:
            print(f"Already subscribed to {subscription_id}")

    async def subscribe_trade(self, symbol: str):
        channel = "trades"

        market = self._market.get(symbol, None)
        symbol = market["id"] if market else symbol

        subscription_id = f"{channel}.{symbol}"

        if subscription_id not in self._subscriptions:
            await self._limiter.wait()
            payload = {
                "op": "subscribe",
                "args": [{"channel": channel, "instId": symbol}],
            }
            self._subscriptions[subscription_id] = payload
            self._send(payload)
        else:
            print(f"Already subscribed to {subscription_id}")

    async def subscribe_kline(self, symbol: str, interval: str):
        pass

    async def _resubscribe(self):
        pass

    def _callback(self, msg):
        if "event" in msg:
            if msg["event"] == "error":
                self._log.error(str(msg))
            elif msg["event"] == "subscribe":
                pass
            elif msg["event"] == "login":
                self._log.info(f"Login successful: {msg}")
            elif msg["event"] == "channel-conn-count":
                self._log.info(f"Channel connection count: {msg['connCount']}")
        elif "arg" in msg:
            channel = msg["arg"]["channel"]
            match channel:
                case "bbo-tbt":
                    self._parse_bbo_tbt(msg)
                case "trades":
                    self._parse_trade(msg)

    def _parse_trade(self, msg):
        """
        {
            "arg": {
                "channel": "trades",
                "instId": "BTC-USD-191227"
            },
            "data": [
                {
                    "instId": "BTC-USD-191227",
                    "tradeId": "9",
                    "px": "0.016",
                    "sz": "50",
                    "side": "buy",
                    "ts": "1597026383085"
                }
            ]
        }
        """
        data = msg["data"][0]
        id = msg["arg"]["instId"]
        market = self._market_id[id]

        trade = Trade(
            exchange=self._exchange_id,
            symbol=market["symbol"],
            price=float(data["px"]),
            size=float(data["sz"]),
            timestamp=int(data["ts"]),
        )
        EventSystem.emit(EventType.TRADE, trade)

    def _parse_bbo_tbt(self, msg):
        """
        {
            'arg': {
                'channel': 'bbo-tbt',
                'instId': 'BTC-USDT'
            },
            'data': [{
                'asks': [['67201.2', '2.17537208', '0', '7']],
                'bids': [['67201.1', '1.44375999', '0', '5']],
                'ts': '1729594943707',
                'seqId': 34209632254
            }]
        }
        """
        data = msg["data"][0]
        id = msg["arg"]["instId"]
        market = self._market_id[id]

        bookl1 = BookL1(
            exchange=self._exchange_id,
            symbol=market["symbol"],
            bid=float(data["bids"][0][0]),
            ask=float(data["asks"][0][0]),
            bid_size=float(data["bids"][0][1]),
            ask_size=float(data["asks"][0][1]),
            timestamp=int(data["ts"]),
        )
        EventSystem.emit(EventType.BOOKL1, bookl1)
