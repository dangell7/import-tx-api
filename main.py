import os
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
xrpl_client = WebsocketClient(os.environ['XRPL_WSS_ENDPOINT'])
xahau_client = WebsocketClient(os.environ['XAHAU_WSS_ENDPOINT'])

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
        print(f"Connected to Xahaud on {os.environ['XAHAU_WSS_ENDPOINT']}")
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
                print(f'BURN HASH: {burn_hash}')
                client.create(burn_hash,  json.dumps(tx).encode('utf-8'))



def backfill(start: int, end: int):
    with xahau_client as client:
        print(f"Connected to XRPL on {os.environ['XAHAU_WSS_ENDPOINT']}")

        for ledger_index in range(start, end + 1):
            ledger_info = Ledger(
                ledger_index=ledger_index,
                transactions=True,
                expand=True,
            )
            response = client.request(ledger_info)
            ledger: Dict[str, Any] = response.result.get("ledger")

            if not ledger or 'transactions' not in ledger:
                print(f"Invalid Ledger")
                continue

            if ledger.get("transactions") == []:
                print(f"No transactions found in ledger {ledger_index}")
                continue

            for tx in ledger.get("transactions"):
                if tx.get('TransactionType') == 'Import':
                    blob: str = tx['Blob']
                    byte_blob = bytes.fromhex(blob)
                    burn_dump = json.loads(byte_blob.decode("utf-8"))
                    burn_tx_blob: str = burn_dump["transaction"]["blob"]
                    burn_tx: Dict[str, Any] = decode(burn_tx_blob)
                    burn_ledger_index: str = burn_dump["ledger"]["index"]
                    burn_hash: str = get_burn_tx_hash(burn_ledger_index, burn_tx)
                    print(f'BURN HASH: {burn_hash}')
                    lmdb_client: AppLMDBService = AppLMDBService()
                    lmdb_client.create(burn_hash, json.dumps(tx).encode('utf-8'))

            print(f"Processed ledger {ledger_index}")

import argparse
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="XRPL Import Transaction Processor")
    parser.add_argument("--backfill", action="store_true", help="Run the backfill process")
    parser.add_argument("--start", type=int, help="Starting ledger index for backfill")
    parser.add_argument("--end", type=int, help="Ending ledger index for backfill")

    args = parser.parse_args()

    if args.backfill:
        if args.start is None or args.end is None:
            start_ledger_index = 9025000  # Replace with the starting ledger index you want to backfill from
            end_ledger_index = 9025167    # Replace with the ending ledger index you want to backfill to
            backfill(start_ledger_index, end=end_ledger_index)
        else:
            backfill(start=args.start, end=args.end)
    else:
        main()
    # asyncio.run(main())
