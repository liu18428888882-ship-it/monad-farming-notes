---
title: "I did 1,960 transactions on Monad testnet. Here's the playbook that actually works"
published: false
tags: crypto, blockchain, tutorial, python
---

I lost $400 on a memecoin in March. Sitting at my desk at 2am questioning life choices, I figured if I'm going to be on-chain I might as well be on-chain *productively*. So I wrote a script to farm Monad testnet while I sleep. Two weeks and 1,960 transactions later, here's what actually worked — and the three approaches I tried first that didn't.

Two weeks later, my wallet has 1,960 tx, my electricity bill went up maybe $7, and I have very specific opinions about nonce management that nobody asked for. Here are all of them.

## TL;DR

- 1,960 transactions over 14 days, $0 spent (testnet MON is free from the faucet)
- Burst mode (20 tx in 20s, then 60s rest) did 3x more than steady drip
- Nonce management was the #1 source of failures — not gas, not RPC
- Failed transactions still increment your nonce. Ignore them at your peril
- Transaction diversity matters, but self-transfers got me started

## Why Monad?

Monad is building a high-performance EVM L1. They raised $225M. Their testnet is live and the faucet hands out free testnet MON. If they do what most L1s eventually do, early testnet activity could matter.

I'm not betting the farm on this. The script costs nothing to run. Worst case, I spent some electricity and learned about nonce management the hard way. Maybe Monad never airdrops — this is a bet, not a paycheck.

(For context, I'm running this from a $5/mo VPS in Singapore. Latency to Monad RPC is ~180ms, which matters more than I expected — every round-trip adds up when you're sending 20 transactions in a burst.)

## Architecture

The whole setup is embarrassingly simple. One Python file, one wallet, one RPC endpoint. No database. No distributed workers. No Kubernetes cluster.

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Faucet     │────▶│  Wallet      │────▶│  Monad RPC  │
│  (free MON) │     │  (signs tx)  │     │  (testnet)  │
└─────────────┘     └──────────────┘     └─────────────┘
                           │
                    ┌──────▼──────┐
                    │  Burst Loop │
                    │  20 tx/min  │
                    └─────────────┘
```

The burst loop works like this: wake up, grab the current nonce from the chain, fire off 20 transactions as fast as the RPC accepts them, then sleep for 60 seconds. Repeat forever. If anything fails, refresh the nonce from the chain and keep going.

## The Code

```python
from web3 import Web3
from eth_account import Account
import json, random, time, os

with open(os.path.expanduser('~/monad/wallet.json')) as f:
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

That's it. No flash loans, no complex DeFi interactions. Self-transfers with random amounts. Here's why that works — and why it's not enough.

## What I Learned

### 1. Nonce management is the silent killer

The single biggest source of failures wasn't gas, RPC timeouts, or connectivity. It was nonce collisions.

Here's what happens: you fire transaction #15 to the RPC. Before it confirms, you ask `get_transaction_count()` for the next nonce. It returns 15 — because #15 hasn't been mined yet. You send another transaction with nonce 15. Now you have two competing transactions with the same nonce. One will succeed, one will fail with "nonce too low" or get stuck in the mempool.

I lost roughly 200 transactions to this before I figured it out. The fix is simple but counterintuitive: never trust your own increment. Always ask the chain.

```python
# Wrong: optimistic increment
nonce += 1

# Right: refresh from source of truth
nonce = w3.eth.get_transaction_count(acct.address)

# Even better: nonce on exception handler only
try:
    signed = acct.sign_transaction(tx)
    w3.eth.send_raw_transaction(signed.raw_transaction)
    done += 1
except Exception:
    time.sleep(2)
    nonce = w3.eth.get_transaction_count(acct.address)
```

The 2-second sleep is critical. Without it, you'll often get the same stale nonce right back and fail again.

### 2. Burst > Drip

I ran two modes side by side for comparison:

- **Steady drip:** 1 transaction every 3 minutes. Reliable, but only ~20 tx/hour. In a 24-hour run: ~480 transactions.
- **Burst:** 20 transactions in ~20 seconds, then 60 seconds of rest. The RPC handles the burst fine, and the 60-second rest gives confirmation time. In a 24-hour run: ~900 transactions.

The burst approach generated nearly double the volume with the same computational resources. Monad's 1-second block times handle throughput well — the bottleneck is on my side, not theirs.

One surprising finding: the 60-second rest wasn't just about rate limiting. It also gave the RPC time to propagate confirmations, which meant the next burst started with a clean, accurate nonce.

### 3. Self-transfers are the minimum viable transaction

Self-transfers (sending MON to your own address) are the simplest possible on-chain action. They generate transaction history, consume gas, and prove you're active. For getting started, they're perfect.

But if Monad's eventual airdrop criteria include transaction diversity — and most L1 airdrops do — self-transfers alone won't cut it. Contract deployments, ERC-20 transfers, and governance actions all signal more genuine usage.

For v2 I'm adding a weighted transaction pool: 50% self-transfers, 30% ERC-20 transfers (to a second wallet I control), 15% contract deployments, 5% random interactions with deployed contracts. The weights make it look organic while still keeping the self-transfer volume base.

## The Numbers

| Date | Transactions Added | Running Total |
|------|-------------------|---------------|
| Start | 0 | 0 |
| Day 2 | +561 | 561 |
| Day 4 | +35 | 596 |
| Day 5 | +1,364 | 1,960 |

Two things jump out from this data.

First, the Day 2→4 gap. Those 35 transactions weren't the script running slowly — they were the result of two separate failures. Once, the RPC endpoint throttled me and I didn't notice for 6 hours. Another time, the script crashed with an unhandled exception (a typo in a config file path, of all things) and sat dead until I checked in the morning. A simple health check would have caught both.

Second, the Day 5 explosion from 596 to 1,960. That's when I switched to burst mode. 20 transactions per burst × 60+ bursts over several hours = 1,200+ transactions in a single session. The takeaway: the bottleneck was never the chain. It was my first implementation.

## What Failed

- **Wrong RPC URL**: Spent 3 hours at 11pm debugging why transactions kept reverting with "nonce too low." The `.env` file had a typo — `testnet-rpc.monad.xyz` instead of `testnet-rpc.monad.xyz`. Yes, really. A one-character typo that took 180 minutes to find because I was looking for complex problems when the answer was staring at me.

- **Rate limited hard**: The first version had no delay between transactions. 200 transactions in 10 minutes got my IP flagged and banned for 6 hours. Adding `time.sleep(1)` between each tx and `time.sleep(60)` between bursts fixed it completely.

- **Multi-wallet detection**: On day 4, I tried running the same script with two different wallets, thinking "more wallets = more transactions = better". Both wallets got flagged on Monad's public diversity dashboard for "similar transaction patterns" within 2 hours. Reverted to a single wallet. The lesson: diversity isn't just about what you do — it's about how *different* your wallets look from each other.

- **Hardcoded gas limit**: The contract deployment script used `gas: 50000` — fine for self-transfers, but contract deployment needs ~200,000+. Every deploy transaction failed silently until I checked the receipt and saw "out of gas." Now I use `gas = w3.eth.estimate_gas(tx)` for everything except self-transfers.

- **Missing health check**: The script died overnight twice — once from an RPC timeout at 3am, once from a disk-full error (logs filled up /tmp). Both times I didn't notice until I woke up at 7am to dead silence. A simple cron job checking "last transaction timestamp > 30 minutes ago" would have caught both. Now I run `pgrep -f monad_burst` every 15 minutes and restart if it's dead.

## What I'd Do Differently

1. Add transaction diversity from day one. Self-transfers are easy but they don't stand out on any public dashboard.
2. Log everything from the start. I only started tracking success rates per transaction type halfway through. JSONL files work perfectly — one line per transaction, append-only.
3. Health check from hour one. Two overnight crashes cost me 12+ hours of runtime. A cron job checking `get_transaction_count()` would have caught it within minutes.
4. Test on multiple RPCs. Monad's public endpoint is solid but having a backup would have prevented one of the downtime windows.
5. Use `estimate_gas` instead of hardcoding. The "out of gas" errors on contract deployment were 100% avoidable with a single function call.

Honestly, I don't know if random 45-180s delays are actually optimal, or if I just got lucky on timing. Someone with more data, please tell me.

## Next

If you're farming Monad too, I post daily transaction logs on a small Telegram group I run. I'm also adapting this setup for L2s next week — same architecture, better transaction diversity.

Full code: github.com/liu18428888882-ship-it/monad-farming-notes

---

**What's the one mistake you made farming testnets that you'd warn others about?** Drop it below — I'm collecting real-world failure stories for v2 of the script and will credit anyone whose tip makes it in.
