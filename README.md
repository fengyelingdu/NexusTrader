# TradeBotPro

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/source/_static/logo-dark.png">
  <source media="(prefers-color-scheme: light)" srcset="docs/source/_static/logo-light.png">
  <img alt="TradeBotPro Logo" src="docs/source/_static/logo-light.png">
</picture>

TradeBotPro is a flexible and powerful trading bot framework designed to interact with various cryptocurrency exchanges. It provides a robust architecture for managing exchange connections, order placements, and real-time data streaming via WebSockets.

## Features

- Support for multiple cryptocurrency exchanges (currently implemented: Binance, Bybit, OKX)
- Asynchronous operations using `asyncio`
- WebSocket support for real-time data streaming
- Order management (limit orders, market orders)
- Account management
- Extensible architecture for easy addition of new exchanges

## Why We Are Faster Than Other Bots

- We utilize [uvloop](https://github.com/MagicStack/uvloop) to enhance the event loop's performance, achieving speeds that are 2-4 times faster than the default event loop.
- We employ [picows](https://github.com/tarasko/picows), a Cython-based WebSocket framework, which can match the performance of C++'s Boost.Beast. Other Python frameworks, such as `websockets` and `aiohttp`, are comparatively slower.
- We leverage `msgspec` for data serialization and deserialization, which outperforms alternatives like `orjson`, `ujson`, and `json`. All data classes are defined as `msgspec.Struct`, which is more efficient than traditional `dataclass`.
- All orders are managed using `asyncio.Queue`.
- The core components (MessageBus, Clock, etc.) are implemented in Rust, with the Python code generated by the [nautilius](https://github.com/nautilius/nautilius) framework.

## Compare with other frameworks

| Framework | Websocket Package |
|-----------|-------|
| TradeBotPro | picows |
| [crypto-feed](https://github.com/bmoscon/cryptofeed) | [websockets](https://websockets.readthedocs.io/en/stable/) |
| [ccxt](https://github.com/bmoscon/cryptofeed) | [aiohttp](https://docs.aiohttp.org/en/stable/client_reference.html) |
| [binance-futures-connector](https://github.com/binance/binance-futures-connector-python) | [websocket-clienr](https://websocket-client.readthedocs.io/en/latest/examples.html) |
| [python-okx](https://github.com/okxapi/python-okx) | websockets |
| [unicorn-binance-websocket-api](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api) | websockets |


## Installation

To install TradeBotPro, use pip:

```
pip install tradebotpro
```

## Quick Start

Here's a basic example of how to use TradeBotPro:

```python
import asyncio
from tradebot.exchange import BinanceExchangeManager, BinanceOrderManager
from tradebot.constants import KEYS

async def main():
    config = {
        'exchange_id': 'binance',
        'sandbox': True,
        'apiKey': KEYS['binance_future_testnet']['API_KEY'],
        'secret': KEYS['binance_future_testnet']['SECRET'],
        'enableRateLimit': False,
    }
    
    exchange = BinanceExchangeManager(config)
    await exchange.load_markets()
    order_manager = BinanceOrderManager(exchange)
    
    res = await order_manager.place_limit_order(
        symbol='BTC/USDT:USDT',
        side='buy',
        price=59695,
        amount=0.01,
        positionSide='LONG',
    )
    
    print(res)

if __name__ == "__main__":
    asyncio.run(main())
```

## Core Components

### ExchangeManager

The `ExchangeManager` class handles the initialization and management of exchange connections. It's responsible for loading markets and providing a unified interface for interacting with different exchanges.

### OrderManager

The `OrderManager` class manages order-related operations such as placing and canceling orders. It provides methods for creating limit and market orders, as well as canceling existing orders.

### WebsocketManager

The `WebsocketManager` class handles WebSocket connections for real-time data streaming. It provides methods for subscribing to various data streams such as order book updates, trades, and user data.

## Supported Exchanges

TradeBotPro currently supports the following exchanges:

1. Binance
2. Bybit
3. OKX

Each exchange has its own implementation of the core components, allowing for exchange-specific features and optimizations.

## Advanced Usage

### Subscribing to WebSocket Streams

Here's an example of how to subscribe to a WebSocket stream:

```python
import asyncio
from tradebot.exchange import BinanceWebsocketManager
from tradebot.constants import Url

async def callback(msg):
    print(msg)

async def main():
    ws_manager = BinanceWebsocketManager(Url.Binance.Spot)
    await ws_manager.subscribe_kline("BTCUSDT", interval='1s', callback=callback)
    
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
```

### Error Handling

TradeBotPro provides custom exceptions for better error handling. For example, the `OrderResponseError` is raised when there's an issue with an order operation:

```python
from tradebot.exceptions import OrderResponseError

try:
    res = await order_manager.place_limit_order(...)
except OrderResponseError as e:
    print(f"Error placing order: {e}")
```

## Contributing

Contributions to TradeBotPro are welcome! Please refer to our [contribution guidelines](CONTRIBUTING.md) for more information on how to get started.

## License

TradeBotPro is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Documentation

Documentation is available at [Read the Docs](https://your-project-name.readthedocs.io/).

### Building Docs Locally

1. Install documentation dependencies:
   ```bash
   pip install -r docs/requirements.txt
   ```

2. Build the documentation:
   ```bash
   cd docs
   make html
   ```

The generated documentation will be in `docs/build/html`.
