from dataclasses import dataclass
from eth_utils.crypto import keccak
import os
from eth_account import Account
from eth_account._utils.signing import (
    sign_transaction_dict,
)

max_tries = 2**26
# from eth_account import Account
#
# key = "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
# auth = {
#     "chainId": 1337,
#     "address": "0x5ce9454909639d2d17a3f753ce7d93fa0b9ab12e",
#     # If the tx sender is the same as the authority, the nonce needs to be 1 higher than the current (transaction) nonce.
#     # This is because the nonce is increased before tx execution and again when processing the authorization.
#     "nonce": 1,
# }
#
# signed_auth = Account.sign_authorization(auth, key)
# signed_auth
# SignedSetCodeAuthorization(chain_id=1337,
#  address=b'\\\xe9EI\tc\x9d-\x17\xa3\xf7S\xce}\x93\xfa\x0b\x9a\xb1.',
#  nonce=1,
#  y_parity=0,
#  r=52163433520757118830640642673035732532535423029712132518776649895118143897479,
#  s=57576671166887700066365341925867052133948674355067837907255957076179513983345,
#  signature='0x735375048fc96b87390b5a11c411fc57245d8e55038bf49e659d048a0d1a3f877f4b3db448845cb217812f23c6b345e99f2d21c44ec10e93a8f039814167417100',
#  authorization_hash=HexBytes('0x9026f77ed6740d6d08f0cdc0591a86b2232700020a816718fbf760785e9ca2f2'))
#
# tx = {
#     "gas": 100000,
#     "maxFeePerGas": 2000000000,
#     "maxPriorityFeePerGas": 2000000000,
#     "data": "0x252dba42",  # replace with calldata for the contract at the auth ``address``
#     "nonce": 0,
#     "to": "0x09616C3d61b3331fc4109a9E41a8BDB7d9776609",
#     "value": 0,
#     "accessList": (),
#     "authorizationList": [signed_auth],
#     "chainId": 1337,
# }
# signed = Account.sign_transaction(tx, key)
# w3.eth.send_raw_transaction(signed.raw_transaction)


@dataclass
class TX:
    _from: int
    to: int
    gas_price: int
    gas_limit: int
    value: int
    nonce: int = 0
    data: bytes = b"deadbeef"
    gas: int = 100000
    max_priority_fee: int = 2000000000
    max_fee: int = 2000000000
    chain_id: int = 1337
    key: str = "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    auth = {
        "chainId": chain_id,
        "address": "0x5ce9454909639d2d17a3f753ce7d93fa0b9ab12e",
        "nonce": nonce,
    }
    signed_auth = Account.sign_authorization(auth, key)
    account = Account.from_key(key)


def find(base: TX, prefix: str = "cafe"):
    for i in range(max_tries):
        suffix = os.urandom(32)
        data = bytes(base.data) + suffix

        tx = {
            "gas": base.gas,
            "gasPrice": base.gas,
            "data": data,
            "nonce": base.nonce,
            "to": "0x09616C3d61b3331fc4109a9E41a8BDB7d9776609",
            "value": base.value,
        }

        # encoded = rlp.encode(list(tx.values()))
        (_, _, _, encoded) = sign_transaction_dict(base.account._key_obj, tx)
        tx_hash = keccak(encoded).hex()
        # print(i)

        if tx_hash.startswith(prefix):
            signed = Account.sign_transaction(tx, base.key)
            return {
                "hash": signed.hash.hex(),
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
