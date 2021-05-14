Built on [`terra-python-sdk`](https://github.com/terra-project/terra-sdk-python) from the legends at [Terra](http://terra.money/)\
Just took the API parts and modified to work with [Akash](https://akash.network/) blockchain.\
\
This does *not* allow you to send any transactions to the chain, for that please use the official akash software.\
Solely for block exploration purposes on a Python interface.\
Recommended for interactive platforms like colab and jupyter\
\
Very brief tutorial on Colab [![](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1wyYOE8cZZVEmiGdlIpibT6_rbtRozrni?usp=sharing)

## Setup
`git clone https://github.com/coranium/akash-python-api.git`\
`cd akash-python-api`\
`pip install terra_sdk`

## Quickstart
Get API_URL and CHAIN_ID from https://github.com/ovrclk/net\

Initialise client using:\
`from lcd import LCDClient`
`akash = LCDClient(chain_id=CHAIN_ID, url=API_URL)`

Most modules from `terra-python-sdk` should work. Refer to their [docs](https://terra-project.github.io/terra-sdk-python/).
