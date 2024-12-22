# TradeBotPro

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/RiverTrading/tradebot-pro-doc/main/docs/source/_static/logo-dark.png">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/RiverTrading/tradebot-pro-doc/main/docs/source/_static/logo-light.png">
  <img alt="TradeBotPro Logo" src="https://raw.githubusercontent.com/RiverTrading/tradebot-pro-doc/main/docs/source/_static/logo-light.png">
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

| Framework | Websocket Package | Data Serialization | Strategy Support |
|-----------|-------|-------|-------|
| TradeBotPro | [picows](https://picows.readthedocs.io/en/stable/introduction.html#installation) | [msgspec](https://jcristharif.com/msgspec/) | ✅ |
| [HummingBot](https://github.com/hummingbot/hummingbot?tab=readme-ov-file) | aiohttp | [ujson](https://pypi.org/project/ujson/) | ✅ |
| [Freqtrade](https://github.com/freqtrade/freqtrade) | websockets | [orjson](https://github.com/ijl/orjson) | ✅ |
| [crypto-feed](https://github.com/bmoscon/cryptofeed) | [websockets](https://websockets.readthedocs.io/en/stable/) | [yapic.json](https://pypi.org/project/yapic.json/) | ❌ |
| [ccxt](https://github.com/bmoscon/cryptofeed) | [aiohttp](https://docs.aiohttp.org/en/stable/client_reference.html) | json | ❌ |
| [binance-futures-connector](https://github.com/binance/binance-futures-connector-python) | [websocket-client](https://websocket-client.readthedocs.io/en/latest/examples.html) | json | ❌ |
| [python-okx](https://github.com/okxapi/python-okx) | websockets | json | ❌ |
| [unicorn-binance-websocket-api](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api) | websockets | [ujson](https://pypi.org/project/ujson/) | ❌ |

## Multi-Mode Support

TradeBotPro supports multiple modes of operation to cater to different trading strategies and requirements. Each mode allows for flexibility in how trading logic is executed based on market conditions or specific triggers.

### Event-Driven Mode

In this mode, trading logic is executed in response to real-time market events. The methods `on_bookl1`, `on_trade`, and `on_kline` are triggered whenever relevant data is updated, allowing for immediate reaction to market changes.

```python
class Demo(Strategy):
    def __init__(self):
        super().__init__()
        self.subscribe_bookl1(symbols=["BTCUSDT-PERP.BINANCE"])
    
    def on_bookl1(self, bookl1: BookL1):
        # implement the trading logic Here
        pass
```

### Timer Mode

This mode allows you to schedule trading logic to run at specific intervals. You can use the `schedule` method to define when your trading algorithm should execute, making it suitable for strategies that require periodic checks or actions.

```python
class Demo2(Strategy):
    def __init__(self):
        super().__init__()
        self.schedule(self.algo, trigger="interval", seconds=1)
    
    def algo(self):
        # run every 1 second
        # implement the trading logic Here
        pass
```

### Custom Signal Mode

In this mode, trading logic is executed based on custom signals. You can define your own signals and use the `on_custom_signal` method to trigger trading actions when these signals are received. This is particularly useful for integrating with external systems or custom event sources.

```python
class Demo3(Strategy):
    def __init__(self):
        super().__init__()
        self.signal = True
    
    def on_custom_signal(self, signal: object):
        # implement the trading logic Here,
        # signal can be any object, it is up to you to define the signal
        pass
```

## Quick Start

Here's a basic example of how to use TradeBotPro, demonstrating a simple buy and sell strategy on OKX.

```python
from decimal import Decimal

from tradebot.constants import settings
from tradebot.config import Config, PublicConnectorConfig, PrivateConnectorConfig, BasicConfig
from tradebot.strategy import Strategy
from tradebot.constants import ExchangeType, OrderSide, OrderType
from tradebot.exchange.okx import OkxAccountType
from tradebot.schema import BookL1, Order
from tradebot.engine import Engine

# Retrieve API credentials from settings
OKX_API_KEY = settings.OKX.DEMO_1.api_key
OKX_SECRET = settings.OKX.DEMO_1.secret
OKX_PASSPHRASE = settings.OKX.DEMO_1.passphrase

class Demo(Strategy):
    def __init__(self):
        super().__init__()
        self.subscribe_bookl1(symbols=["BTCUSDT-PERP.OKX"])  # Subscribe to the order book for the specified symbol
        self.signal = True  # Initialize signal to control order execution
    
    def on_failed_order(self, order: Order):
        print(order)  # Log failed orders
    
    def on_pending_order(self, order: Order):
        print(order)  # Log pending orders
    
    def on_accepted_order(self, order: Order):
        print(order)  # Log accepted orders
    
    def on_partially_filled_order(self, order: Order):
        print(order)  # Log partially filled orders
    
    def on_filled_order(self, order: Order):
        print(order)  # Log filled orders
    
    def on_bookl1(self, bookl1: BookL1):
        if self.signal:  # Check if the signal is active
            # Create a market buy order
            self.create_order(
                symbol="BTCUSDT-PERP.OKX",
                side=OrderSide.BUY,
                type=OrderType.MARKET,
                amount=Decimal("0.1"),
            )
            # Create a market sell order
            self.create_order(
                symbol="BTCUSDT-PERP.OKX",
                side=OrderSide.SELL,
                type=OrderType.MARKET,
                amount=Decimal("0.1"),
            )
            self.signal = False  # Deactivate the signal after placing orders
        

# Configuration for the trading strategy
config = Config(
    strategy_id="okx_buy_and_sell",
    user_id="user_test",
    strategy=Demo(),
    basic_config={
        ExchangeType.OKX: BasicConfig(
            api_key=OKX_API_KEY,
            secret=OKX_SECRET,
            passphrase=OKX_PASSPHRASE,
            testnet=True,  # Use testnet for safe trading
        )
    },
    public_conn_config={
        ExchangeType.OKX: [
            PublicConnectorConfig(
                account_type=OkxAccountType.DEMO,  # Specify demo account type
            )
        ]
    },
    private_conn_config={
        ExchangeType.OKX: [
            PrivateConnectorConfig(
                account_type=OkxAccountType.DEMO,  # Specify demo account type
            )
        ]
    }
)

# Initialize the trading engine with the configuration
engine = Engine(config)

if __name__ == "__main__":
    try:
        engine.start()  # Start the trading engine
    finally:
        engine.dispose()  # Ensure resources are cleaned up

```
This example illustrates how easy it is to switch between different exchanges and strategies by modifying the `config` class. For instance, to switch to Binance, you can adjust the configuration as follows, and change the symbol to `BTCUSDT-PERP.BINANCE`.

```python
from tradebot.exchange.binance import BinanceAccountType

config = Config(
    strategy_id="buy_and_sell_binance",
    user_id="user_test",
    strategy=Demo(),
    basic_config={
        ExchangeType.BINANCE: BasicConfig(
            api_key=BINANCE_API_KEY,
            secret=BINANCE_SECRET,
            testnet=True,  # Use testnet for safe trading
        )
    },
    public_conn_config={
        ExchangeType.BINANCE: [
            PublicConnectorConfig(
                account_type=BinanceAccountType.USD_M_FUTURE_TESTNET,  # Specify account type for Binance
            )
        ]
    },
    private_conn_config={
        ExchangeType.BINANCE: [
            PrivateConnectorConfig(
                account_type=BinanceAccountType.USD_M_FUTURE_TESTNET,  # Specify account type for Binance
            )
        ]
    }
)
```

## Contributing

Contributions to TradeBotPro are welcome! Please refer to our [contribution guidelines](CONTRIBUTING.md) for more information on how to get started.

## License

TradeBotPro is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Documentation

Documentation is available at [Read the Docs](https://your-project-name.readthedocs.io/).
