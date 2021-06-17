"""Data objects pertaining to accounts."""

from __future__ import annotations

from typing import List

import attr

from lcd.core import AccAddress, Coins
from lcd.util.json import JSONSerializable

from .public_key import PublicKey

__all__ = ["Account", "PeriodicVestingAccount"]


@attr.s
class Account(JSONSerializable):
    """Stores information about an account."""

    address: AccAddress = attr.ib()
    """"""

    public_key: PublicKey = attr.ib()
    """"""

    account_number: int = attr.ib(converter=int)
    """"""

    sequence: int = attr.ib(converter=int)
    """"""

    def to_data(self) -> dict:
        return {
            "type": "cosmos-sdk/BaseAccount",
            "value": {
                "address": self.address,
                "public_key": self.public_key.to_data(),
                "account_number": str(self.account_number),
                "sequence": str(self.sequence),
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> Account:
        data = data["value"]
        return cls(
            address=data["address"],
            public_key=PublicKey.from_data(data["public_key"]),
            account_number=data["account_number"],
            sequence=data["sequence"],
        )

# TODO
@attr.s
class PeriodicVestingAccount(Account):
    """Stores information about an account with vesting."""

    address: AccAddress = attr.ib()
    """"""

    public_key: PublicKey = attr.ib()
    """"""

    account_number: int = attr.ib(converter=int)
    """"""

    sequence: int = attr.ib(converter=int)
    """"""

    original_vesting: Coins = attr.ib(converter=Coins)
    """"""

    delegated_free: Coins = attr.ib(converter=Coins)
    """"""

    delegated_vesting: Coins = attr.ib(converter=Coins)
    """"""

    end_time: int = attr.ib(converter=int)
    """"""

    start_time: int = attr.ib(converter=int)
    """"""

    vesting_periods: List[dict] = attr.ib()
    """"""

    def to_data(self) -> dict:
        return {
            "type": "cosmos-sdk/PeriodicVestingAccount",
            "value": {
                "address": self.address,
                "public_key": self.public_key and self.public_key.to_data(),
                "account_number": str(self.account_number),
                "sequence": str(self.sequence),
                "original_vesting": self.original_vesting.to_data(),
                "delegated_free": self.delegated_free.to_data(),
                "delegated_vesting": self.delegated_vesting.to_data(),
                "end_time": str(self.end_time),
                "start_time": str(self.start_time),
                "vesting_periods": self.vesting_periods,
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> PeriodicVestingAccount:
        data = data["value"]
        account = data["base_vesting_account"]
        base_account = account["base_account"]
        return cls(
            address=base_account["address"],
            public_key=PublicKey.from_data(base_account["public_key"]),
            account_number=base_account["account_number"],
            sequence=base_account["sequence"],
            original_vesting=Coins.from_data(account["original_vesting"]),
            delegated_free=Coins.from_data(account["delegated_free"]),
            delegated_vesting=Coins.from_data(account["delegated_vesting"]),
            end_time=account["end_time"],
            start_time=data["start_time"],
            vesting_periods=data["vesting_periods"],
        )
