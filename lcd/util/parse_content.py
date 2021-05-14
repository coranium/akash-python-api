from lcd.core.distribution.proposals import CommunityPoolSpendProposal
from lcd.core.gov.proposals import TextProposal
from lcd.core.params.proposals import ParameterChangeProposal
from lcd.core.treasury.proposals import (
    RewardWeightUpdateProposal,
    TaxRateUpdateProposal,
)

from .base import create_demux

parse_content = create_demux(
    [
        CommunityPoolSpendProposal,
        TextProposal,
        ParameterChangeProposal,
        RewardWeightUpdateProposal,
        TaxRateUpdateProposal,
    ]
)
