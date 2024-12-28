from decimal import Decimal

from tradebot.constants import settings
from tradebot.config import Config, PublicConnectorConfig, PrivateConnectorConfig, BasicConfig
from tradebot.strategy import Strategy
from tradebot.constants import ExchangeType, OrderSide, OrderType
from tradebot.exchange.binance import BinanceAccountType
from tradebot.schema import BookL1, Order
from tradebot.engine import Engine



BINANCE_API_KEY = settings.BINANCE.FUTURE.TESTNET_1.api_key
BINANCE_SECRET = settings.BINANCE.FUTURE.TESTNET_1.secret



class Demo(Strategy):
    def __init__(self):
        super().__init__()
        self.subscribe_bookl1(symbols=["BTCUSDT-PERP.BINANCE"])
        self.signal = True
        self.schedule(func=self.algo, seconds=1)
    
    def algo(self):
        print("algo")
    
    # def on_failed_order(self, order: Order):
    #     print(order)
    
    # def on_pending_order(self, order: Order):
    #     print(order)
    
    # def on_accepted_order(self, order: Order):
    #     print(order)
    
    # def on_filled_order(self, order: Order):
    #     print(order)
    
    # def on_bookl1(self, bookl1: BookL1):
    #     if self.signal:
    #         self.create_order(
    #             symbol="BTCUSDT-PERP.BINANCE",
    #             side=OrderSide.BUY,
    #             type=OrderType.MARKET,
    #             amount=Decimal("0.01"),
    #         )
    #         self.create_order(
    #             symbol="BTCUSDT-PERP.BINANCE",
    #             side=OrderSide.SELL,
    #             type=OrderType.MARKET,
    #             amount=Decimal("0.01"),
    #         )
    #         self.signal = False

config = Config(
    strategy_id="buy_and_sell_binance",
    user_id="user_test",
    strategy=Demo(),
    basic_config={
        ExchangeType.BINANCE: BasicConfig(
            api_key=BINANCE_API_KEY,
            secret=BINANCE_SECRET,
            testnet=True,
        )
    },
    public_conn_config={
        ExchangeType.BINANCE: [
            PublicConnectorConfig(
                account_type=BinanceAccountType.USD_M_FUTURE_TESTNET,
            )
        ]
    },
    private_conn_config={
        ExchangeType.BINANCE: [
            PrivateConnectorConfig(
                account_type=BinanceAccountType.USD_M_FUTURE_TESTNET,
            )
        ]
    }
)

engine = Engine(config)

if __name__ == "__main__":
    try:
        engine.start()
    finally:
        engine.dispose()
