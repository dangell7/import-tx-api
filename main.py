import asyncio
import json
import requests

# from xrpl.asyncio.clients import AsyncWebsocketClient


from typing import Dict, Any
from xrpl.clients import WebsocketClient
from xrpl.core.binarycodec.main import decode
from xrpl.models.transactions import AccountSet
from xrpl.models.requests import Subscribe, StreamParameter
from xrpl.models.requests.ledger import Ledger

from server.services.lmdb import AppLMDBService

# async_client = AsyncWebsocketClient('wss://xahau-test.net')
xrpl_client = WebsocketClient("wss://s.altnet.rippletest.net:51233")
xahau_client = WebsocketClient("wss://xahau-test.net")


def validate_tx(burn_tx: Dict[str, Any], ledger_tx: Dict[str, Any]) -> bool:
    if (
        burn_tx["Account"] == ledger_tx["Account"]
        and burn_tx["TransactionType"] == ledger_tx["TransactionType"]
        and burn_tx["Sequence"] == ledger_tx["Sequence"]
        and burn_tx["LastLedgerSequence"] == ledger_tx["LastLedgerSequence"]
        and burn_tx["OperationLimit"] == ledger_tx["OperationLimit"]
        and burn_tx["Fee"] == ledger_tx["Fee"]
    ):
        return True
    return False


def get_burn_tx_hash(ledger_index: int, burn_tx: Dict[str, Any]) -> str:

    # DA: try this but it might not work for multi signed txs
    # prefix = hex(_TRANSACTION_HASH_PREFIX)[2:].upper()
    # encoded_str = bytes.fromhex(prefix + encode(self.to_xrpl()))
    # return sha512(encoded_str).digest().hex().upper()[:64]

    with xrpl_client as _:
        ledger_info = Ledger(
            ledger_index=ledger_index,
            transactions=True,
            expand=True,
        )
        response = xrpl_client.request(ledger_info)
        ledger: Dict[str, Any] = response.result.get("ledger")
        for tx in ledger.get("transactions"):
            if validate_tx(burn_tx, tx):
                return tx["hash"]


def main():
    with xahau_client as client:
        print("Connected to Xahaud on wss://xahau-test.net")
        req = Subscribe(streams=[StreamParameter.TRANSACTIONS])
        client.send(req)
        for message in client:
            if 'transaction' not in message:
                continue
            
            tx: Dict[str, Any] = message.get('transaction')
            if tx and tx.get('TransactionType') == 'Import':
                blob: str = tx['Blob']
                byte_blob = bytes.fromhex(blob)
                burn_dump = json.loads(byte_blob.decode("utf-8"))
                burn_tx_blob: str = burn_dump["transaction"]["blob"]
                burn_tx: Dict[str, Any] = decode(burn_tx_blob)
                burn_ledger_index: str = burn_dump["ledger"]["index"]
                burn_hash: str = get_burn_tx_hash(burn_ledger_index, burn_tx)
                client: AppLMDBService = AppLMDBService()
                client.create(burn_hash,  json.dumps(tx).encode('utf-8'))


if __name__ == "__main__":
    main()
    # asyncio.run(main())


