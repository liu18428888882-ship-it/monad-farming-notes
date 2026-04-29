# Hermes Monad Playbook

Automated Monad testnet farming agent — 1,960 transactions in 14 days. Zero cost, open source.

## Why

Monad raised $225M to build a high-performance EVM-compatible L1. Their testnet is live and the faucet is free. Most L1s airdrop to early users. This agent automates testnet activity to build on-chain history.

## Real Numbers

| Date | Transactions | Running Total |
|------|-------------|---------------|
| Start | 0 | 0 |
| Day 2 | +561 | 561 |
| Day 4 | +35 | 596 |
| Day 5 | +1,364 | 1,960 |

The jump from 596 to 1,960 happened when switching from steady drip (1 tx/3min) to burst mode (20 tx in 20s, then 60s rest).

## Quick Start

```bash
# 1. Install dependencies
pip install web3 eth-account

# 2. Create wallet file at ~/.hermes/wallets/airdrop_farm.json
#    Format: {"address": "0x...", "private_key": "..."}

# 3. Get testnet MON from faucet
#    https://testnet.monad.xyz

# 4. Run the agent
python3 monad_burst.py
```

## What's Inside

- `monad_burst.py` — Burst transaction agent (20 tx per round)
- `01-monad-playbook.md` — Full writeup with code, architecture, and lessons learned
- `render_cover.py` — Cover image generator (Playwright + HTML)

## Follow Along

Daily updates on Telegram: [@HermesGGYY_bot](https://t.me/HermesGGYY_bot)
