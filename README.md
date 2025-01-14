<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/RiverTrading/tradebot-pro-doc/main/docs/source/_static/logo-dark.png">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/RiverTrading/tradebot-pro-doc/main/docs/source/_static/logo-light.png">
  <img alt="TradeBotPro Logo" src="https://raw.githubusercontent.com/RiverTrading/tradebot-pro-doc/main/docs/source/_static/logo-light.png">
</picture>


---

![License](https://img.shields.io/badge/license-MIT-blue.svg)![Python](https://img.shields.io/badge/python-3.10%2B-blue)![Version](https://img.shields.io/badge/version-1.0.0-blue)

- **Docs**: https://nautilustrader.io/docs/
- **Support**: [quantweb3.ai@gmail.com](mailto:quantweb3.ai@gmail.com)

## Introduction

TradeBot is a professional-grade open-source quantitative trading platform, specifically designed for **large capital
management** and **complex strategy development**, dedicated to providing high-performance, scalable, and user-friendly
quantitative trading solutions.

## Overview

### Core Advantages

1. **Professionally Optimized Order Algorithms：** Deep optimization for algorithmic orders including TWAP, effectively
   reducing market impact costs. Users can easily integrate their own execution signals to achieve more efficient and
   precise order execution.
2. **Professional Arbitrage Strategy Support：**Provides professional optimization for various arbitrage strategies,
   including funding rate arbitrage and cross-exchange arbitrage, supporting real-time tracking and trading of thousands
   of trading pairs to help users easily capture arbitrage opportunities.
3. **Full-Featured Quantitative Trading Framework：** Users don't need to build frameworks or handle complex exchange
   interface details themselves. TradeBot has integrated professional position management, order management, fund
   management, and statistical analysis modules, allowing users to focus on writing strategy logic and quickly implement
   quantitative trading.
4. **Multi-Market Support and High Scalability：** Supports large-scale multi-market tracking and high-frequency strategy
   execution, covering a wide range of trading instruments, making it an ideal choice for professional trading needs.

### Why TradeBot Is More Efficient?

  - **Enhanced Event Loop Performance**: TradeBot leverages [uvloop](https://github.com/MagicStack/uvloop), a high-performance event loop, delivering speeds up to 2-4 times faster than Python's default asyncio loop.

  - **High-Performance WebSocket Framework**: Built with [picows](https://github.com/tarasko/picows), a Cython-based WebSocket library that matches the speed of C++'s Boost.Beast, significantly outperforming Python alternatives like websockets and aiohttp.

  - **Optimized Data Serialization**: Utilizing `msgspec` for serialization and deserialization, TradeBot achieves unmatched efficiency, surpassing tools like `orjson`, `ujson`, and `json`. All data classes are implemented with `msgspec.Struct` for maximum performance.

  - **Scalable Order Management**: Orders are handled efficiently using `asyncio.Queue`, ensuring seamless processing even at high volumes.

  - **Rust-Powered Core Components**: Core modules such as the MessageBus and Clock are implemented in Rust, combining Rust's speed and reliability with Python's flexibility through the [nautilius](https://github.com/nautilius/nautilius) framework.

### Comparison with Other Frameworks

| Framework                                                    | Websocket Package                                            | Data Serialization                                 | Strategy Support | Advantages                                         | Disadvantages                                     |
| ------------------------------------------------------------ | ------------------------------------------------------------ | -------------------------------------------------- | ---------------- | -------------------------------------------------- | ------------------------------------------------- |
| **TradeBotPro**                                              | [picows](https://picows.readthedocs.io/en/stable/introduction.html#installation) | [msgspec](https://jcristharif.com/msgspec/)        | ✅                | Professionally optimized for speed and low latency | Requires some familiarity with async workflows    |
| [HummingBot](https://github.com/hummingbot/hummingbot?tab=readme-ov-file) | aiohttp                                                      | [ujson](https://pypi.org/project/ujson/)           | ✅                | Widely adopted with robust community support       | Slower WebSocket handling and limited flexibility |
| [Freqtrade](https://github.com/freqtrade/freqtrade)          | websockets                                                   | [orjson](https://github.com/ijl/orjson)            | ✅                | Flexible strategy support                          | Higher resource consumption                       |
| [crypto-feed](https://github.com/bmoscon/cryptofeed)         | [websockets](https://websockets.readthedocs.io/en/stable/)   | [yapic.json](https://pypi.org/project/yapic.json/) | ❌                | Simple design for feed-only use                    | Lacks trading support and advanced features       |
| [ccxt](https://github.com/bmoscon/cryptofeed)                | [aiohttp](https://docs.aiohttp.org/en/stable/client_reference.html) | json                                               | ❌                | Great REST API support                             | Limited WebSocket performance                     |
| [binance-futures-connector](https://github.com/binance/binance-futures-connector-python) | [websocket-client](https://websocket-client.readthedocs.io/en/latest/examples.html) | json                                               | ❌                | Optimized for Binance-specific integration         | Limited to Binance Futures                        |
| [python-okx](https://github.com/okxapi/python-okx)           | websockets                                                   | json                                               | ❌                | Dedicated to OKX trading                           | Limited to OKX platform                           |
| [unicorn-binance-websocket-api](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api) | websockets                                                   | [ujson](https://pypi.org/project/ujson/)           | ❌                | Easy-to-use for Binance users                      | Restricted to Binance and resource-heavy          |

### Architecture (data flow)

![Architecture](/Users/mac/go/src/tradebot-pro/docs/source/_static/arch.png "architecture")

### Features

- 🌍 Multi-Exchange Integration: Effortlessly connect to top exchanges like Binance, Bybit, and OKX, with an extensible design to support additional platforms.
- ⚡ Asynchronous Operations: Built on asyncio for highly efficient, scalable performance, even during high-frequency trading.
- 📡 Real-Time Data Streaming: Reliable WebSocket support for live market data, order book updates, and trade execution notifications.
- 📊 Advanced Order Management: Execute diverse order types (limit, market, stop) with optimized, professional-grade order handling.
- 📋 Account Monitoring: Real-time tracking of balances, positions, and PnL across multiple exchanges with integrated monitoring tools.
- 🛠️ Modular Architecture: Flexible framework to add exchanges, instruments, or custom strategies with ease.
- 🔄 Strategy Execution & Backtesting: Seamlessly transition from strategy testing to live trading with built-in tools.
- 📈 Scalability: Designed to handle large-scale, multi-market operations for retail and institutional traders alike.
- 💰 Risk & Fund Management: Optimize capital allocation and control risk exposure with integrated management tools.
- 🔔 Instant Notifications: Stay updated with alerts for trades, market changes, and custom conditions.

### Supported Exchanges

| OKX                                                          | **Binance**                                                  | BYBIT                                                        |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| <img src="https://www.okx.com/cdn/assets/imgs/226/EB771F0EE8994DD5.png" width="100"> | <img src="https://cryptologos.cc/logos/binance-coin-bnb-logo.png" width="100"> | <img src="https://raw.githubusercontent.com/bybit-web3/bybit-web3.github.io/main/docs/images/bybit-logo.png" width="100"> |

## Getting Started

### Installation (From PyPI)

We recommend using the latest supported version of Python and setting
up [tradebot](https://pypi.org/project/nautilus_trader/) in a virtual environment to isolate dependencies

To install the latest binary wheel (or sdist package) from PyPI using Pythons pip package manager:

    pip install -U tradebot

### Quick Start

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

This example illustrates how easy it is to switch between different exchanges and strategies by modifying the `config`
class. For instance, to switch to Binance, you can adjust the configuration as follows, and change the symbol to
`BTCUSDT-PERP.BINANCE`.

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

## Multi-Mode Support

TradeBotPro supports multiple modes of operation to cater to different trading strategies and requirements. Each mode
allows for flexibility in how trading logic is executed based on market conditions or specific triggers.

### Event-Driven Mode

In this mode, trading logic is executed in response to real-time market events. The methods `on_bookl1`, `on_trade`, and
`on_kline` are triggered whenever relevant data is updated, allowing for immediate reaction to market changes.

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

This mode allows you to schedule trading logic to run at specific intervals. You can use the `schedule` method to define
when your trading algorithm should execute, making it suitable for strategies that require periodic checks or actions.

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

In this mode, trading logic is executed based on custom signals. You can define your own signals and use the
`on_custom_signal` method to trigger trading actions when these signals are received. This is particularly useful for
integrating with external systems or custom event sources.

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

## Contributing

Thank you for considering contributing to TradeBotPro! We greatly appreciate any effort to help improve the project. If
you have an idea for an enhancement or a bug fix, the first step is to open
an [issue](https://github.com/Quantweb3-ai/tradebot-pro/issues) on GitHub. This allows us to discuss your proposal and
ensure it aligns with the project's goals, while also helping to avoid duplicate efforts.

When you're ready to start working on your contribution, please review the guidelines in
the [CONTRIBUTING.md](CONTRIBUTING.md) file. Depending on the nature of your contribution, you may also need to sign a
Contributor License Agreement (CLA) to ensure it can be included in the project.

> **Note**
> Pull requests should be directed to the `main` branch (the default branch), where new features and improvements are
> integrated before release.

Thank you again for your interest in TradeBotPro! We look forward to reviewing your contributions and collaborating with
you to make the project even better.

## VIP Privileges

Trading on our platform is free. Become a VIP customer to enjoy exclusive technical support privileges for $199 per month ([Subscription Here](https://quantweb3.ai))—or get VIP status at no cost by opening an account through our partnership links.

Our partners include global leading trading platforms like Bybit, OKX, ZFX, Bison and others. By opening an account through our referral links, you'll enjoy these benefits:

Instant Account Benefits

1. Trading Fee Discounts: Exclusive discounts to lower your trading costs.
2. VIP Service Support: Contact us after opening your account to become our VIP customer. Enjoy exclusive events and benefits for the ultimate VIP experience.

Act now and join our VIP program!

> Click the links below to register

- [Bybit](https://partner.bybit.com/b/90899)
- [OKX](http://www.okx.com/join/80353297)
- [ZFX](https://zfx.link/46dFByp)
- [Bison](https://m.bison.com/#/register?invitationCode=1002)

## Social

Connect with us on your favorite platforms:

[![X (Twitter)](https://img.shields.io/badge/X_(Twitter)-000000?style=for-the-badge&logo=x&logoColor=white)](https://x.com/quantweb3_ai) Stay updated with our latest news, features, and announcements.

[![Discord](https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/BR8VGRrXFr) Join our community to discuss ideas, get support, and connect with other users.

[![Telegram](https://img.shields.io/badge/Telegram-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/+6e2MtXxoibM2Yzlk) Receive instant updates and engage in real-time discussions.

## See Also

We recommend exploring related tools and projects that can enhance your trading workflows:

- **[Nexus](https://github.com/Quantweb3-ai/nexus):** A robust exchange interface optimization solution that integrates
  seamlessly with trading bots like TradeBotPro, enabling faster and more reliable trading execution.

## License

TradeBotPro is available on GitHub under the MIT License. Contributions to the project are welcome and require the
completion of a Contributor License Agreement (CLA). Please review the contribution guidelines and submit a pull
request. See the [LICENSE](LICENSE) file for details.
