#!/usr/bin/env python3
"""Payment reconciliation."""

import json
from decimal import Decimal

latest = {}

with open("payments.jsonl", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(event, dict):
            continue
        txn_id = event.get("txn_id")
        if not txn_id:
            continue
        ts = event.get("ts")
        if txn_id not in latest or ts > latest[txn_id]["ts"]:
            latest[txn_id] = event


def parse_amount(value):
    if isinstance(value, str):
        value = value.replace(",", "").strip()
    return Decimal(str(value))


total = Decimal(0)
count = 0
for event in latest.values():
    if event["status"] == "success":
        total += parse_amount(event["amount"])
        count += 1

with open("expected.txt") as f:
    expected = int(f.read().strip())

if count != expected:
    print(f"Check failed: counted {count} successful payments, expected {expected}.")
    print("Something in the data isn't being handled the way the README describes.")
else:
    print(f"Check passed: {count} successful payments.")
    print(f"Your code: KOYA-{round(total)}")
