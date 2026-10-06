# RISK

```
One rule, no conversation, final authority, nobody overrules it.
  avg_6h = volume.h24 / 4
  ratio  = volume.h6 / avg_6h
  ratio < 0.20 -> CLOSE, fully, inside 60 seconds.
Poll every 5 minutes. No answer, retry twice, then CLOSE anyway.
The moment the close is filled, call book.release(). Until you do, the desk does
not scan.
```
