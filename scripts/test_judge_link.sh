#!/usr/bin/env bash
# Run from a bot's own terminal, not your laptop.
# Check: shape.choice is one of the options, probabilities sum to 1,
# model is a version string (not an alias).
curl -X POST "$JUDGE_URL" -H "Authorization: Bearer $DESK_SECRET" \
  -H "Content-Type: application/json" \
  -d '{"question_set":"market","state":{"ticker":"TEST","age_minutes":42,
       "holder_count":310,"change":{"5m":0.04,"1h":0.22,"24h":0.61},
       "buys_h1":540,"sells_h1":120,"liquidity_usd":48000,"mcap_usd":310000,
       "volume_h24":610000,"intended_ticket_usd":900}}'
