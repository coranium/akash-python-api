from typing import List, Optional

import attr

from lcd.core import AccAddress

from ._base import BaseAsyncAPI, sync_bind

__all__ = ["AsyncDeploymentAPI", "DeploymentAPI"]

class AsyncDeploymentAPI(BaseAsyncAPI):
    async def info(
        self,
        owner: AccAddress = None,
        dseq: int = None,
    ) -> dict:
        """Fetches info about a deployment

        Args:
            owner (AccAddress): deployment owner account address.
            dseq (int): dseq.

        Raises:
            TypeError: if both ``owner`` or ``dseq`` are ``None``.

        Returns:
            Deployment: deployment
        """
        if owner is not None and dseq is not None:
            params = {
            "id.owner": owner,
            "id.dseq": dseq,
        }
            res = await self._c._get(
                f"/akash/deployment/v1beta1/deployments/info",
                params,
                raw=True
            )
            return res
        else:
            raise TypeError("arguments delegator and validator cannot both be None")

    async def get_all(
        self,
        owner: Optional[AccAddress] = None,
        dseq: Optional[int] = None,
        state: Optional[str] = None,
        limit: Optional[int] = 100,
    ) -> List:
        '''Fetches a list of deployment info with optional filters
        
        Args:
            owner (AccAddress): deployment owner account address.
            dseq (int): dseq.

        Returns:
            List[Deployment]: bunch of deployments
        ''' 
        params = {
            "filters.owner": owner,
            "filters.dseq": dseq,
            'filters.state': state,
            'pagination.limit':limit,
        }

        # temporary fix to get rid of optional params/payload
        for x in list(params.keys()):
            if params[x] is None:
                del params[x]

        
        res = await self._c._get(
                f"/akash/deployment/v1beta1/deployments/list",
                params,
                raw=True
            )

        return res['deployments']

class DeploymentAPI(AsyncDeploymentAPI):
    @sync_bind(AsyncDeploymentAPI.info)
    def info(
        self,
        owner: AccAddress = None,
        dseq: int = None,
    ) -> dict:
        pass

    info.__doc__ = AsyncDeploymentAPI.info.__doc__

    @sync_bind(AsyncDeploymentAPI.get_all)
    def get_all(
        self,
        owner: Optional[AccAddress] = None,
        dseq: Optional[int] = None,
        state: Optional[str] = None,
        limit: Optional[int] = 100,
    ) -> List:
        pass
    get_all.__doc__ = AsyncDeploymentAPI.get_all.__doc__
