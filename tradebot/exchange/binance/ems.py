import asyncio
from decimal import Decimal
from typing import Dict
from tradebot.constants import AccountType
from tradebot.schema import BaseMarket, OrderSubmit, InstrumentId
from tradebot.core.cache import AsyncCache
from tradebot.core.nautilius_core import MessageBus
from tradebot.core.entity import TaskManager
from tradebot.core.registry import OrderRegistry
from tradebot.exchange.binance import BinanceAccountType
from tradebot.exchange.binance.schema import BinanceMarket
from tradebot.base import ExecutionManagementSystem


class BinanceExecutionManagementSystem(ExecutionManagementSystem):
    _market: Dict[str, BinanceMarket]
    
    BINANCE_SPOT_PRIORITY = [
        BinanceAccountType.ISOLATED_MARGIN,
        BinanceAccountType.MARGIN,
        BinanceAccountType.SPOT_TESTNET,
        BinanceAccountType.SPOT,
    ]

    def __init__(
        self,
        market: Dict[str, BinanceMarket],
        cache: AsyncCache,
        msgbus: MessageBus,
        task_manager: TaskManager,
        registry: OrderRegistry,
    ):
        super().__init__(
            market=market,
            cache=cache,
            msgbus=msgbus,
            task_manager=task_manager,
            registry=registry,
        )
        self._binance_spot_account_type: BinanceAccountType = None
        self._binance_linear_account_type: BinanceAccountType = None
        self._binance_inverse_account_type: BinanceAccountType = None
        self._binance_pm_account_type: BinanceAccountType = None

    def _set_account_type(self):
        account_types = self._private_connectors.keys()

        if BinanceAccountType.PORTFOLIO_MARGIN in account_types:
            self._binance_pm_account_type = BinanceAccountType.PORTFOLIO_MARGIN
            return

        for account_type in self.BINANCE_SPOT_PRIORITY:
            if account_type in account_types:
                self._binance_spot_account_type = account_type
                break

        self._binance_linear_account_type = (
            BinanceAccountType.USD_M_FUTURE_TESTNET
            if BinanceAccountType.USD_M_FUTURE_TESTNET in account_types
            else BinanceAccountType.USD_M_FUTURE
        )

        self._binance_inverse_account_type = (
            BinanceAccountType.COIN_M_FUTURE_TESTNET
            if BinanceAccountType.COIN_M_FUTURE_TESTNET in account_types
            else BinanceAccountType.COIN_M_FUTURE
        )

    def _instrument_id_to_account_type(
        self, instrument_id: InstrumentId
    ) -> AccountType:
        if self._binance_pm_account_type:
            return self._binance_pm_account_type
        if instrument_id.is_spot:
            return self._binance_spot_account_type
        elif instrument_id.is_linear:
            return self._binance_linear_account_type
        elif instrument_id.is_inverse:
            return self._binance_inverse_account_type

    def _build_order_submit_queues(self):
        for account_type in self._private_connectors.keys():
            if isinstance(account_type, BinanceAccountType):
                self._order_submit_queues[account_type] = asyncio.Queue()

    def _submit_order(
        self, order: OrderSubmit, account_type: AccountType | None = None
    ):
        if not account_type:
            account_type = self._instrument_id_to_account_type(order.instrument_id)
        self._order_submit_queues[account_type].put_nowait(order)
    
    def _get_min_order_amount(self, symbol: str, market: BinanceMarket) -> Decimal:
        pass
