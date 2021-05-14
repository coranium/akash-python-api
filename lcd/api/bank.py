from lcd.core import AccAddress, Coins, Coin

from ._base import BaseAsyncAPI, sync_bind

__all__ = ["AsyncBankAPI", "BankAPI"]


class AsyncBankAPI(BaseAsyncAPI):
    async def balance(self, address: AccAddress) -> Coins:
        """Fetches an account's current balance.

        Args:
            address (AccAddress): account address

        Returns:
            Coin: balance of address in uakt
        """
        res = await self._c._get(f"/bank/balances/{address}")

        return Coins.from_data(res)
    
    async def supply(self) -> Coin:
        """Fetches total supply of AKT. TODO: add in IBC coins.

        Returns:
            Coin: Total Supply of coinz
        """
        res = await self._c._get(f"/cosmos/bank/v1beta1/supply/uakt", raw=True)
        
        return Coin.from_data(res['amount'])


class BankAPI(AsyncBankAPI):
    @sync_bind(AsyncBankAPI.balance)
    def balance(self, address: AccAddress) -> Coins:
        pass

    balance.__doc__ = AsyncBankAPI.balance.__doc__

    @sync_bind(AsyncBankAPI.supply)
    def supply(self, address: AccAddress) -> Coin:
        pass

    supply.__doc__ = AsyncBankAPI.supply.__doc__
