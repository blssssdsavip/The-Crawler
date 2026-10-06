# THE ORDER (what CHIEF drops into the desk channel)

```json
{
  "order_id": "2026-09-23T10:15:00Z",
  "token": {"ticker": "...", "address": "...", "network_id": 1399811149, "chain": "solana"},
  "size_factor": 1.0,
  "confidence": 0.78,
  "why": {"shape": "crowd", "crowd_p": 0.91, "concentration_is_exit_risk": 0.14,
          "authority_risk": "renounced", "account_is_the_project": 0.97,
          "recycled_account": 0.06, "effort": 2.4},
  "model": "jev-1.13.0"
}
```

```
THE ORDER, WORKED IN THIS SEQUENCE, NOBODY SKIPS AHEAD

1. SIZE   reads token + size_factor. Computes the ticket. Returns dollars, or 0 with a
          reason. A 0 ends the order here.
2. FILLS  reads the ticket. Checks the fee floor BEFORE sending. Sends one market order.
          Reports filled, fill_price, slippage_bps, partial.
3. RISK   starts its timer the moment a fill is reported. Polls every 5 minutes.
          Fires on its own authority.
4. CHIEF  logs the order id, the model id and every answer that produced it, then
          sends the line to Telegram.

NOBODY RE-READS `why`. It is there for the log, not as an input.
NO ORDER IS ALSO AN ORDER. When pick returns nothing, CHIEF sends one line saying so.
```
