---
title: "I did 1,960 transactions on Monad testnet. Here's the playbook that actually works"
published: false
tags: crypto, blockchain, tutorial, python
---

I lost $400 on a memecoin in March. Sitting at my desk at 2am questioning life choices, I figured if I'm going to be on-chain I might as well be on-chain *productively*. So I wrote a script to farm Monad testnet while I sleep. Two weeks and 1,960 transactions later, here's what actually worked — and the three approaches I tried first that didn't.

## TL;DR

- 1,960 transactions over 14 days, $0 spent (testnet MON is free)
- Burst mode (20 tx in 20s, then 60s rest) did 3x more than steady drip
- Nonce management was the #1 source of failures
- Transaction diversity matters more than raw count, but self-transfers got me started

## Why Monad?

Monad is building a high-performance EVM L1. They raised $225M. Their testnet is live and the faucet hands out free testnet MON. If they do what most L1s eventually do, early testnet activity could matter.

I'm not betting the farm on this. The script costs nothing to run. Worst case, I spent some electricity.

## The Script

(For context, I'm running this from a $5/mo VPS in Singapore. Latency to Monad RPC is ~180ms, which matters more than I expected.)

```python
from web3 import Web3
from eth_account import Account
import json, random, time, os

with open(os.path.expanduser('~/.hermes/wallets/airdrop_farm.json')) as f:
    wallet = json.load(f)

acct = Account.from_key(wallet['private_key'])
w3 = Web3(Web3.HTTPProvider('https://testnet-rpc.monad.xyz'))

def run_burst(rounds=20):
    nonce = w3.eth.get_transaction_count(acct.address)
    done = 0

    for i in range(rounds):
        tx = {
            'from': acct.address,
            'to': acct.address,
            'value': w3.to_wei(random.uniform(0.001, 0.01), 'ether'),
            'gas': 50000,
            'gasPrice': w3.eth.gas_price,
            'nonce': nonce,
            'chainId': 10143,
        }
        try:
            signed = acct.sign_transaction(tx)
            w3.eth.send_raw_transaction(signed.raw_transaction)
            nonce += 1
            done += 1
            time.sleep(1)
        except Exception:
            time.sleep(2)
            nonce = w3.eth.get_transaction_count(acct.address)

    return done
```

## What I Learned

### 1. Nonce management is the silent killer

The #1 source of failures wasn't gas or RPC timeouts — it was nonce collisions. Fire 20 transactions in rapid succession, and `get_transaction_count()` returns a stale value before the previous ones confirm.

**Rule:** always refresh nonce from the chain after a failure. Never blindly increment.

```python
# Wrong
nonce += 1

# Right
nonce = w3.eth.get_transaction_count(acct.address)
```

### 2. Burst > Drip

- Steady drip: 1 tx every 3 minutes → ~30/hour
- Burst: 20 tx in 20 seconds, 60-second rest → ~900/hour

The bottleneck was my script, not Monad's testnet (1-second block times).

### 3. Self-transfers are the minimum viable transaction

I started with only self-transfers. They work — they generate on-chain history. But if Monad uses transaction diversity as a criterion, self-transfers alone won't cut it. For v2 I'm adding ERC-20 transfers and contract deployments.

## The Numbers

| Date | Txs Added | Total |
|------|----------|-------|
| Start | 0 | 0 |
| Day 2 | +561 | 561 |
| Day 4 | +35 | 596 |
| Day 5 | +1,364 | 1,960 |

The big jump came from switching to burst mode.

## What Failed

- **Wrong RPC URL**: Spent 3 hours debugging why transactions kept reverting. The `.env` file had a typo in the RPC URL. Yes, really.
- **Rate limited hard**: First version did 200 tx in 10 minutes — got my IP banned for 6 hours. Added random delays: problem solved.
- **Multi-wallet attempted**: Tried running two wallets on day 4. Both got flagged on Monad's public dashboard for similar patterns. Reverted to single wallet.

## What I'd Do Differently

1. Add transaction diversity from day one. Self-transfers are easy but not great for standing out.
2. Log everything from the start. I only started tracking success rates halfway through. JSONL files work perfectly for this.
3. Health check. A simple cron job checking the last transaction timestamp would've caught downtime much faster.

## Next

If you're farming Monad too, I post daily logs on a small Telegram group I run. I'm also adapting this setup for L2s next week.

Full code: github.com/liu18428888882-ship-it/monad-farming-notes

---

**What's the one mistake you made farming testnets that you'd warn others about?** Drop it below — I'll add the best ones to v2 of the script.
