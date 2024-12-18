from decimal import Decimal

from tradebot.constants import KEYS
from tradebot.config import Config, PublicConnectorConfig, PrivateConnectorConfig, BasicConfig
from tradebot.strategy import Strategy
from tradebot.constants import ExchangeType, OrderSide, OrderType
from tradebot.exchange.bybit import BybitAccountType
from tradebot.schema import Order, OrderSubmit
from tradebot.engine import Engine

BYBIT_API_KEY = KEYS["bybit_testnet_2"]["API_KEY"]
BYBIT_SECRET = KEYS["bybit_testnet_2"]["SECRET"]




class Demo(Strategy):
    def __init__(self):
        super().__init__()
        self.subscribe_bookl1(symbols=["BTCUSDT-PERP.BYBIT"])
        self.subscribe_trade(symbols=["BTCUSDT-PERP.BYBIT"])
        
        self.schedule(self.algo, seconds=0.1)
        self.signal = True
        self.uuid = None
    
    def on_pending_order(self, order: Order):
        print(order)
    
    def on_accepted_order(self, order: Order):
        print(order)
    
    def on_partially_filled_order(self, order: Order):
        print(order)
    
    def on_filled_order(self, order: Order):
        print(order)
    
    def algo(self):
        bookl1 = self.cache.bookl1("BTCUSDT-PERP.BYBIT")
        if bookl1:
            if self.signal:
                bid, ask = bookl1.bid, bookl1.ask
                bid = self.price_to_precision("BTCUSDT-PERP.BYBIT", bid)
                ask = self.price_to_precision("BTCUSDT-PERP.BYBIT", ask)
                
                order: OrderSubmit = self.create_order(
                    symbol="BTCUSDT-PERP.BYBIT",
                    side=OrderSide.BUY,
                    type=OrderType.LIMIT,
                    amount=Decimal("0.001"),
                    price=bid,
                )
                print("order uuid", order.uuid)
                self.uuid = order.uuid
                self.signal = False


config = Config(
    strategy_id="buy_and_sell",
    user_id="user_test",
    strategy=Demo(),
    basic_config={
        ExchangeType.BYBIT: BasicConfig(
            api_key=BYBIT_API_KEY,
            secret=BYBIT_SECRET,
            testnet=True,
        )
    },
    public_conn_config={
        ExchangeType.BYBIT: [
            PublicConnectorConfig(
                account_type=BybitAccountType.LINEAR_TESTNET,
            ),
            PublicConnectorConfig(
                account_type=BybitAccountType.SPOT_TESTNET,
            ),
        ]
    },
    private_conn_config={
        ExchangeType.BYBIT: [
            PrivateConnectorConfig(
                account_type=BybitAccountType.ALL_TESTNET,
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
