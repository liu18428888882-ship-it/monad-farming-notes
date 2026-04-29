#!/usr/bin/env python3
"""Monad farmer with proper nonce management and retry."""
import json, random, time, os
from web3 import Web3
from eth_account import Account

with open(os.path.expanduser('~/.hermes/wallets/airdrop_farm.json')) as f:
    w = json.load(f)
acct = Account.from_key(w['private_key'])
w3 = Web3(Web3.HTTPProvider('https://testnet-rpc.monad.xyz'))
addr = acct.address

bal = float(w3.from_wei(w3.eth.get_balance(addr), 'ether'))
nonce = w3.eth.get_transaction_count(addr)
done = 0

for i in range(20):
    tx = {
        'from': addr, 'to': addr,
        'value': w3.to_wei(random.uniform(0.001, 0.01), 'ether'),
        'gas': 50000, 'gasPrice': w3.eth.gas_price,
        'nonce': nonce, 'chainId': 10143,
    }
    try:
        s = w3.eth.account.sign_transaction(tx, acct.key)
        w3.eth.send_raw_transaction(s.raw_transaction)
        nonce += 1
        done += 1
        time.sleep(1)  # Wait for block inclusion
    except Exception as e:
        # Refresh nonce from chain and retry
        time.sleep(2)
        nonce = w3.eth.get_transaction_count(addr)

print(f"Done: {done}")
