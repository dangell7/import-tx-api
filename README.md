

```
from server.services.lmdb import AppLMDBService

client: AppLMDBService = AppLMDBService()
client.create('key1', b'value1')
response = client.get('key1')
print(response)
```

```
from xrpl.models.requests.tx import Tx
tx_request = Tx(transaction='77B5E4519E65557CFCE0F88B1F5B886DBC7AA59E5EA626282DFBADEC36676C33')
response = client.request(tx_request)
tx = response.result
blob: str = tx.get('Blob')

byte_blob = bytes.fromhex(blob)
burn_dump = json.loads(byte_blob.decode("utf-8"))
burn_tx_blob: str = burn_dump["transaction"]["blob"]
burn_tx: Dict[str, Any] = decode(burn_tx_blob)
burn_ledger_index: str = burn_dump["ledger"]["index"]
burn_hash: str = get_burn_tx_hash(burn_ledger_index, burn_tx)
client: AppLMDBService = AppLMDBService()
client.create(burn_hash,  json.dumps(tx).encode('utf-8'))
```

```
client: AppLMDBService = AppLMDBService()
response = client.get('B821A5C6257BB8901C8321406D2A595BA2A3CF3EFEF80F139F909B63F888E53C').decode('utf-8')
print(response)
```