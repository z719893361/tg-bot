from typing import Callable, Dict, Awaitable
from httpx import AsyncClient
import logging
import asyncio
import time


logger = logging.getLogger("订单监控")

logger.setLevel(logging.ERROR)


class TransactionMonitor:
    def __init__(self, address, expires: int, callback: Callable[[str, float, int], Awaitable[None]]):
        """
        :param address:  钱包地址
        :param expires:  订单到期时间, 单位秒
        :param callback: 回调接口
        """
        self.address = address
        self.expires = expires
        self.client = AsyncClient()
        self.callback = callback
        self._stop = True

    async def _poll(self):
        try:
            result = await self.client.get(
                url='https://apilist.tronscanapi.com/api/token_trc20/transfers',
                params={
                    'relatedAddress': self.address,
                    'start_timestamp': round(time.time() - self.expires) * 1000
                },
                timeout=5
            )
            data = result.json()
        except Exception as e:
            logger.error(e)
            return
        for transfer in data.get('token_transfers', []):
            try:
                to_address = transfer['to_address']
                confirmed = transfer['confirmed']
                contract_ret = transfer['contractRet']
                if to_address == self.address and confirmed is True and contract_ret == 'SUCCESS':
                    quant = int(transfer['quant']) / 1000000
                    transaction_id = transfer['transaction_id']
                    await self.callback(transaction_id, quant, self.expires)
            except KeyError:
                pass
            except Exception as e:
                print(e)

    async def poll_order_deposit(self):
        while self._stop:
            try:
                await self._poll()
                await asyncio.sleep(5)
            except Exception as e:
                logger.error(e)

    def stop(self):
        self._stop = False


class UsdtTransactionMonitorThreadManager:
    def __init__(self):
        self.robot_id_monitor: Dict[int, TransactionMonitor] = {}

    async def add(self, robot_id: int, monitor: TransactionMonitor):
        if robot_id in self:
            return
        self.robot_id_monitor[robot_id] = monitor
        asyncio.create_task(monitor.poll_order_deposit())

    async def stop(self, robot_id: int):
        monitor = self.robot_id_monitor.get(robot_id)
        if monitor is None:
            return
        self.robot_id_monitor.pop(robot_id)
        monitor.stop()

    def get_monitor(self, robot_id: int):
        return self.robot_id_monitor.get(robot_id)

    async def update_monitor(self, robot_id: int, address: str, expires: int):
        monitor = self.get_monitor(robot_id)
        if monitor is None:
            return
        if monitor.address == address and monitor.expires == expires:
            return
        monitor.stop()
        self.robot_id_monitor.pop(robot_id)
        await self.add(robot_id, TransactionMonitor(address, expires, monitor.callback))

    def get_robots_id(self):
        return list(self.robot_id_monitor.keys())

    def __contains__(self, item):
        return item in self.robot_id_monitor


usdt_monitor_manage = UsdtTransactionMonitorThreadManager()
