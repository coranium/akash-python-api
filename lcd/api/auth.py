from typing import Union

from lcd.core import AccAddress
from lcd.core.auth import Account, LazyGradedVestingAccount

from ._base import BaseAsyncAPI, sync_bind

__all__ = ["AsyncAuthAPI", "AuthAPI"]


class AsyncAuthAPI(BaseAsyncAPI):
    async def account_info(
        self, address: AccAddress
    ) -> Union[Account, LazyGradedVestingAccount]:
        """Fetches the account information.

        Args:
            address (AccAddress): account address

        Returns:
            Union[Account, LazyGradedVestingAccount]: account information
        """
        result = await self._c._get(f"/auth/accounts/{address}")
        if result["type"] == "cosmos-sdk/BaseAccount":
            return Account.from_data(result)
        else: # This doesn't work, need to find out what types akash uses.
            return LazyGradedVestingAccount.from_data(result)


class AuthAPI(AsyncAuthAPI):
    @sync_bind(AsyncAuthAPI.account_info)
    def account_info(
        self, address: AccAddress
    ) -> Union[Account, LazyGradedVestingAccount]:
        pass

    account_info.__doc__ = AsyncAuthAPI.account_info.__doc__
