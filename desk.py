"""The Grok Bot side of the desk. main.py needs five methods from it.

ShadowDesk is a local stand-in for shadow week: it logs would-be orders to
shadow_log.jsonl and prints reports. Replace it with your real Grok Bot wiring
(SOCIAL's X plugin, Telegram, and the SIZE -> FILLS -> RISK handoff) when you go live."""
import json, os, time


class ShadowDesk:
    def bank(self) -> float:
        return float(os.environ.get("BANK_USD", "1000"))

    def read_x(self, handle):
        return None             # SOCIAL's X plugin fills this in production

    def log_shadow(self, order, stats):
        with open("shadow_log.jsonl", "a") as f:
            f.write(json.dumps({"ts": time.time(), "order": order, "stats": stats},
                               default=str) + "\n")

    def report(self, order, stats):
        if order:
            print(f"ORDER {order['token']['ticker']} size_factor={order['size_factor']}")
        else:
            print(f"no trade this cycle: {stats}")

    def send_to_seats(self, order):
        raise NotImplementedError("wire this to SIZE -> FILLS -> RISK on your Grok Bot desk")
