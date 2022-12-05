
# not needed for now but might help with building txs
# for now 
from aptos_sdk.account import Account
from aptos_sdk.client import RestClient
from aptos_sdk.account_address import AccountAddress
from aptos_sdk.bcs import Serializer
from aptos_sdk.transactions import (EntryFunction, TransactionArgument,
                                    TransactionPayload)
import requests

NODE_URL = "https://fullnode.mainnet.aptoslabs.com"

# Create a class to wrap the aptos client

url = "https://fullnode.devnet.aptoslabs.com/v1/transactions/by_hash/txn_hash"

headers = {"Content-Type": "application/json"}

response = requests.request("GET", url, headers=headers)

# print(response.text)
class AptosClient:

    def __init__():
        rest_client = RestClient(NODE_URL)

    def get_user(self,hash):
        resources = self.rest_client.get_resources(hash)

    