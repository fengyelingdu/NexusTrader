import asyncio
from typing import Dict
from decimal import Decimal
from nexustrader.constants import AccountType
from nexustrader.schema import OrderSubmit
from nexustrader.core.cache import AsyncCache
from nexustrader.core.nautilius_core import MessageBus
from nexustrader.core.entity import TaskManager
from nexustrader.core.registry import OrderRegistry
from nexustrader.exchange.bybit import BybitAccountType
from nexustrader.exchange.bybit.schema import BybitMarket
from nexustrader.base import ExecutionManagementSystem

class BybitExecutionManagementSystem(ExecutionManagementSystem):
    _market: Dict[str, BybitMarket]

    def __init__(
        self,
        market: Dict[str, BybitMarket],
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
        self._bybit_account_type: BybitAccountType = None

    def _build_order_submit_queues(self):
        for account_type in self._private_connectors.keys():
            if isinstance(account_type, BybitAccountType):
                self._order_submit_queues[account_type] = asyncio.Queue()

    def _set_account_type(self):
        account_types = self._private_connectors.keys()
        self._bybit_account_type = (
            BybitAccountType.UNIFIED_TESTNET
            if BybitAccountType.UNIFIED_TESTNET in account_types
            else BybitAccountType.UNIFIED
        )

    def _submit_order(
        self, order: OrderSubmit, account_type: AccountType | None = None
    ):
        if not account_type:
            account_type = self._bybit_account_type
        self._order_submit_queues[account_type].put_nowait(order)
        
    def _get_min_order_amount(self, symbol: str, market: BybitMarket) -> Decimal:
        book = self._cache.bookl1(symbol)
        min_order_amount = max(6 / (book.bid + book.ask), market.limits.amount.min)
        min_order_amount = self._amount_to_precision(symbol, min_order_amount, mode="ceil")
        return min_order_amount
