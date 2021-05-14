from __future__ import annotations

from asyncio import AbstractEventLoop, get_event_loop
from json import JSONDecodeError
from typing import Optional, Union
from urllib.parse import urljoin

import nest_asyncio
from aiohttp import ClientSession

from lcd.util.exceptions import LCDResponseError
from lcd.util.json import dict_to_data

from .api.auth import AsyncAuthAPI, AuthAPI
from .api.bank import AsyncBankAPI, BankAPI
from .api.distribution import AsyncDistributionAPI, DistributionAPI
from .api.deployment import AsyncDeploymentAPI, DeploymentAPI
from .api.gov import AsyncGovAPI, GovAPI
from .api.mint import AsyncMintAPI, MintAPI
from .api.slashing import AsyncSlashingAPI, SlashingAPI
from .api.staking import AsyncStakingAPI, StakingAPI
from .api.tendermint import AsyncTendermintAPI, TendermintAPI
from .lcdutils import AsyncLCDUtils, LCDUtils


class AsyncLCDClient:
    def __init__(
        self,
        url: str,
        chain_id: Optional[str] = None,
        loop: Optional[AbstractEventLoop] = None,
        _create_session: bool = True,  # don't create a session (used for sync LCDClient)
    ):
        if loop is None:
            loop = get_event_loop()
        self.loop = loop
        if _create_session:
            self.session = ClientSession(
                headers={"Accept": "application/json"}, loop=self.loop
            )

        self.chain_id = chain_id
        self.url = url
        self.last_request_height = None

        self.auth = AsyncAuthAPI(self)
        self.bank = AsyncBankAPI(self)
        self.distribution = AsyncDistributionAPI(self)
        self.deployment = AsyncDeploymentAPI(self)
        self.gov = AsyncGovAPI(self)
        self.mint = AsyncMintAPI(self)
        self.slashing = AsyncSlashingAPI(self)
        self.staking = AsyncStakingAPI(self)
        self.tendermint = AsyncTendermintAPI(self)
        self.utils = AsyncLCDUtils(self)


    async def _get(
        self, endpoint: str, params: Optional[dict] = None, raw: bool = False
    ):
        async with self.session.get(
            urljoin(self.url, endpoint), params=params
        ) as response:
            try:
                result = await response.json(content_type=None)
            except JSONDecodeError:
                raise LCDResponseError(message=str(response.reason), response=response)
            if not 200 <= response.status < 299:
                raise LCDResponseError(message=result.get("error"), response=response)
        self.last_request_height = result.get("height")
        return result if raw else result["result"]

    async def _post(
        self, endpoint: str, data: Optional[dict] = None, raw: bool = False
    ):
        async with self.session.post(
            urljoin(self.url, endpoint), json=data and dict_to_data(data)
        ) as response:
            try:
                result = await response.json(content_type=None)
            except JSONDecodeError:
                raise LCDResponseError(message=str(response.reason), response=response)
            if not 200 <= response.status < 299:
                raise LCDResponseError(message=result.get("error"), response=response)
        self.last_request_height = result.get("height")
        return result if raw else result["result"]

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()


class LCDClient(AsyncLCDClient):
    """An object representing a connection to a node running the Terra LCD server."""

    url: str
    """URL endpoint of LCD server."""

    chain_id: str
    """Chain ID of blockchain network connecting to."""

    last_request_height: Optional[int]  # type: ignore
    """Height of response of last-made made LCD request."""

    auth: AuthAPI
    """:class:`AuthAPI<terra_sdk.client.lcd.api.auth.AuthAPI>`."""

    bank: BankAPI
    """:class:`BankAPI<terra_sdk.client.lcd.api.bank.BankAPI>`."""

    distribution: DistributionAPI
    """:class:`DistributionAPI<terra_sdk.client.lcd.api.distribution.DistributionAPI>`."""

    deployment: DeploymentAPI
    """:class:`DeploymentAPI<terra_sdk.client.lcd.api.deployment.DeploymentAPI>`."""

    gov: GovAPI
    """:class:`GovAPI<terra_sdk.client.lcd.api.gov.GovAPI>`."""

    mint: MintAPI
    """:class:`MintAPI<terra_sdk.client.lcd.api.mint.MintAPI>`."""

    slashing: SlashingAPI
    """:class:`SlashingAPI<terra_sdk.client.lcd.api.slashing.SlashingAPI>`."""

    staking: StakingAPI
    """:class:`StakingAPI<terra_sdk.client.lcd.api.staking.StakingAPI>`."""

    tendermint: TendermintAPI
    """:class:`TendermintAPI<terra_sdk.client.lcd.api.tendermint.TendermintAPI>`."""

    def __init__(
        self,
        url: str,
        chain_id: str = None,
    ):
        super().__init__(
            url,
            chain_id,
            _create_session=False,
            loop=nest_asyncio.apply(get_event_loop()),
        )

        self.auth = AuthAPI(self)
        self.bank = BankAPI(self)
        self.distribution = DistributionAPI(self)
        self.deployment = DeploymentAPI(self)
        self.gov = GovAPI(self)
        self.mint = MintAPI(self)
        self.slashing = SlashingAPI(self)
        self.staking = StakingAPI(self)
        self.tendermint = TendermintAPI(self)
        self.utils = LCDUtils(self)

    async def __aenter__(self):
        raise NotImplementedError(
            "async context manager not implemented - you probably want AsyncLCDClient"
        )

    async def __aexit__(self, exc_type, exc, tb):
        raise NotImplementedError(
            "async context manager not implemented - you probably want AsyncLCDClient"
        )

    async def _get(self, *args, **kwargs):
        # session has to be manually created and torn down for each HTTP request in a
        # synchronous client
        self.session = ClientSession(
            headers={"Accept": "application/json"}, loop=self.loop
        )
        try:
            result = await super()._get(*args, **kwargs)
        finally:
            await self.session.close()
        return result

    async def _post(self, *args, **kwargs):
        # session has to be manually created and torn down for each HTTP request in a
        # synchronous client
        self.session = ClientSession(
            headers={"Accept": "application/json"}, loop=self.loop
        )
        try:
            result = await super()._post(*args, **kwargs)
        finally:
            await self.session.close()
        return result
