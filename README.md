# Monad Testnet Farming Notes

Crypto dev experimenting with on-chain automation. Notes from things I'm actually running.

## What this is

A Python script that farms the Monad testnet — 1,960 transactions in 14 days. Zero cost (testnet MON is free from the faucet).

## The Numbers

| Date | Transactions | Running Total |
|------|-------------|---------------|
| Start | 0 | 0 |
| Day 2 | +561 | 561 |
| Day 4 | +35 | 596 |
| Day 5 | +1,364 | 1,960 |

Switching from steady drip (1 tx/3min) to burst mode (20 tx in 20s, then 60s rest) was the breakthrough.

## Quick Start

```bash
pip install web3 eth-account

# Create wallet file at ~/.hermes/wallets/airdrop_farm.json
# Get testnet MON: https://testnet.monad.xyz

python3 monad_burst.py
```

## What's Inside

- `monad_burst.py` — Burst transaction script (20 tx per round)
- `01-monad-playbook.md` — Full writeup with code and lessons learned
- `render_cover.py` + `verify_cover.py` — Cover image tools

## Updates

I post daily transaction logs on a small Telegram group I run. Link in the article.
