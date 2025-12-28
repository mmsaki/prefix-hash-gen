from dataclasses import dataclass
from eth_utils.crypto import keccak
import rlp
import os

max_tries = 2**26


@dataclass
class TX:
    _from: int
    to: int
    nonce: int
    gas_price: int
    gas_limit: int
    value: int
    data: bytes


def find(base: TX, prefix: str = "cafe"):
    for _ in range(max_tries):
        suffix = os.urandom(16)
        data = base.data + suffix

        tx = {
            "nonce": base.nonce,
            "gas_price": base.gas_price,
            "gas_limit": base.gas_limit,
            "to": base.to,
            "from": base._from,
            "value": base.value,
            "data": data,
        }

        encoded = rlp.encode(list(tx.values()))
        tx_hash = keccak(encoded).hex()

        if tx_hash.startswith(prefix):
            return {
                "hash": tx_hash,
                "suffix": suffix.hex(),
                "calldata": data,
            }

    return None


def main():
    print("Hello from prefix-hash-gen!")
    tx = TX(
        0x04655832BCB0A9A0BE8C5AB71E4D311464C97AF5,
        0x04655832BCB0A9A0BE8C5AB71E4D311464C97AF5,
        0,
        0,
        0,
        0,
        bytes(0),
    )
    result = find(tx)
    if result:
        print(f"Found hash: {result['hash']}")
        print(f"Suffix: {result['suffix']}")
        print(f"Calldata: {result['calldata'].hex()}")
    else:
        print("No hash found with the given prefix")


if __name__ == "__main__":
    main()
