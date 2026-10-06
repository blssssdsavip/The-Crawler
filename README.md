# The Crawler

A memecoin scanning desk: code fetches, Jev (TypeSafe) judges, code decides, Grok Bot trades.
Based on the public "Megabrain (Jev) & Six Grok Bots" setup guide by @savipww.

> ⚠️ **This is not financial advice.** Every threshold here is the original author's,
> tuned on their own bank over one week. Run in shadow mode first. Memecoin trading
> on fresh launches carries a high risk of total loss.

## The funnel

```
0. UNIVERSE  GeckoTerminal new_pools, 3 chains          -> fresh launches
1. LIST      FOMO filterTokens, 20 per call             -> hundreds, one batch
2. FREE CUT  age, liquidity, volume, mcap. No network   -> tens
3. TRADE CUT DexScreener buys and sells, one per token  -> a handful
4. DOSSIER   GeckoTerminal info + chain RPC + X         -> three per cycle
5. JUDGE     market + chain + social per token          -> scored shortlist
6. PICK      one choice over the shortlist              -> one token, or none
```

## Layout

| File | Role |
|---|---|
| `judge.py` | FastAPI service. Only process holding `TYPESAFE_API_KEY`. |
| `judge_client.py` | What every seat uses to call the judge. |
| `questions.py` | Every question set (market, solana, bsc, robinhood, social, pick). |
| `collect.py` | Universe, shortlist, trade counts, dossier. |
| `thresholds.py` | Every number. Retune here only. |
| `filter.py` | free_kill → trade_kill → chain_kill → soft_kill. |
| `pick.py` | Final choice over survivors + size factor. |
| `book.py` | One-position guard and rejection bench (SQLite). |
| `main.py` | The cycle loop. Defaults to shadow mode. |
| `fomo_api.py` | **Stub.** Not included in the original guide — you must implement it. |
| `desk.py` | `ShadowDesk` stand-in for the Grok Bot side. |
| `prompts/` | Seat prompts: handoff, SOCIAL, SIZE, FILLS, RISK, order sequence. |
| `scripts/` | Key test, judge link test, judge launcher. |

## Setup

```bash
pip install -r requirements.txt        # python 3.10+
cp .env.example .env                    # fill in, then export the vars

./scripts/test_key.sh                   # prove the TypeSafe key works
export DESK_SECRET="$(openssl rand -hex 24)"
./scripts/run_judge.sh                  # judge + cloudflared tunnel
./scripts/test_judge_link.sh            # run from a bot's terminal

python main.py                          # shadow mode by default (SHADOW=1)
```

## What's missing from the original guide

- **`fomo_api.Fomo`** is imported but never shown. `fomo_api.py` here is a stub with the
  interface the rest of the code expects; `token()` raises `NotImplementedError`.
- **The Grok Bot side** (`desk.read_x`, `desk.send_to_seats`, Telegram reporting) lives on
  the bots, not in this repo. `desk.py` gives a local shadow-mode stand-in.
- **The original six-seat setup** the guide builds on is a separate post and is not included.

## Rate limits and failures

- GeckoTerminal free tier: 10 calls/min. 6 go to the universe, 3 to dossiers. Use
  `universe(pages=1)` for 3 more dossiers.
- 429 GeckoTerminal → back off a full minute. 429 DexScreener → lower `DEX_BUDGET`.
- 422 from Jev → question is malformed. Never retry.
- Judge unreachable → skip the cycle. No fallback to guessing.
