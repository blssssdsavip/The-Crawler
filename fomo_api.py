"""FOMO client. NOT INCLUDED IN THE ORIGINAL GUIDE.

The guide imports `Fomo` from `fomo_api` but never shows it. It is described as reading
the Privy bearer token from your own logged-in Chrome profile over the Chrome DevTools
Protocol (CDP), then calling:

    POST https://prod-api.fomo.family/proxy/filterTokens
    body: ["<address>:<netId>", ...]   (20 at a time)

FOMO has no public API, so you will need to fill this in yourself. The rest of the desk
expects exactly this interface:

    fomo.token()            -> refresh the bearer (called at the top of every cycle)
    fomo.tokens(ids)        -> {tid: {"symbol", "mcap", "liq", "vol24", "price",
                                       "holders", "change": {300, 3600, 14400, 86400},
                                       "created"}}
"""
import requests

FILTER_URL = "https://prod-api.fomo.family/proxy/filterTokens"
BATCH = 20


class Fomo:
    def __init__(self):
        self._bearer = None

    def token(self) -> str:
        """Return a fresh Privy bearer from your Chrome session. Implement this."""
        raise NotImplementedError(
            "fomo_api.Fomo.token() is not part of the published guide. "
            "Implement bearer retrieval for your own logged-in session.")

    def _raw(self, batch: list[str]) -> list[dict]:
        r = requests.post(FILTER_URL, json=batch, timeout=20,
                          headers={"Authorization": f"Bearer {self._bearer or self.token()}"})
        r.raise_for_status()
        return r.json()

    def _map(self, row: dict) -> dict:
        """Map FOMO's response fields onto the names collect.normalise() expects.
           Field names below follow the guide (marketCap, liquidity, volume24, holders,
           priceUSD, change5m/1/4/12/24, createdAt). Verify against a real response."""
        return {"symbol": row.get("symbol"),
                "mcap": row.get("marketCap") or 0,
                "liq": row.get("liquidity") or 0,
                "vol24": row.get("volume24") or 0,
                "price": row.get("priceUSD"),
                "holders": row.get("holders"),
                "change": {300: row.get("change5m"), 3600: row.get("change1"),
                           14400: row.get("change4"), 86400: row.get("change24")},
                "created": row.get("createdAt")}

    def tokens(self, ids: list[str]) -> dict:
        out = {}
        for i in range(0, len(ids), BATCH):
            batch = ids[i:i + BATCH]
            for tid, row in zip(batch, self._raw(batch)):
                if row:
                    out[tid] = self._map(row)
        return out
