#!/usr/bin/env python3
"""Dharma3 governance gate — cost / safety / observability for every agent.

Thin workflow wrapper over the ported `ai_runners` (Dharma 1's testable AI governance). Gives the
orchestrator a persistent, cross-process budget gate and telemetry it can call per wave / per agent.

Telemetry log defaults to memory/telemetry.jsonl (one JSON line per agent call).

Usage:
    python3 scripts/govern.py record --model claude-opus-4-8 --in 1200 --out 340 [--agent build:1-2] [--latency 850]
    python3 scripts/govern.py gate --ceiling 10.0          # exit 1 if cumulative spend ≥ ceiling
    python3 scripts/govern.py report                       # cost / latency / refusal summary
    python3 scripts/govern.py pricing                      # list known model prices
"""
import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from ai_runners.economics import PRICING  # noqa: E402

DEFAULT_LOG = ROOT / "memory" / "telemetry.jsonl"


def cost_usd(model, in_tok, out_tok):
    p = PRICING.get(model)
    if not p:
        return 0.0
    return round(in_tok / 1_000_000 * p["input"] + out_tok / 1_000_000 * p["output"], 6)


def read_log(path):
    path = Path(path)
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return rows


def cmd_record(a):
    c = cost_usd(a.model, a.in_tok, a.out_tok)
    rec = {
        "ts": time.time(),
        "model": a.model,
        "input_tokens": a.in_tok,
        "output_tokens": a.out_tok,
        "latency_ms": a.latency,
        "cost_usd": c,
        "agent": a.agent or "—",
    }
    log = Path(a.log)
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec) + "\n")
    total = sum(r.get("cost_usd", 0) for r in read_log(log))
    if a.model not in PRICING:
        print(f"  ⚠ unknown model '{a.model}' — cost counted as $0 (add it to ai_runners/economics.py)")
    print(f"  recorded {a.agent or a.model}: ${c:.6f}  ·  session total ${total:.4f}")
    return 0


def cmd_gate(a):
    total = sum(r.get("cost_usd", 0) for r in read_log(a.log))
    pct = (total / a.ceiling * 100) if a.ceiling else 0
    if total >= a.ceiling:
        print(f"  ⛔ BUDGET GATE: ${total:.4f} ≥ ceiling ${a.ceiling:.2f} ({pct:.0f}%). "
              f"Stop and hand off / raise ceiling before the next wave.")
        return 1
    flag = "  ⚠ over alert threshold" if pct >= 80 else ""
    print(f"  ✓ budget OK: ${total:.4f} / ${a.ceiling:.2f} ({pct:.0f}%){flag}")
    return 0


def cmd_report(a):
    rows = read_log(a.log)
    if not rows:
        print("  no telemetry yet (memory/telemetry.jsonl empty).")
        return 0
    total = sum(r.get("cost_usd", 0) for r in rows)
    lat = [r.get("latency_ms", 0) for r in rows if r.get("latency_ms")]
    by_agent = {}
    for r in rows:
        by_agent[r.get("agent", "—")] = by_agent.get(r.get("agent", "—"), 0) + r.get("cost_usd", 0)
    print(f"  calls: {len(rows)}  ·  total: ${total:.4f}  ·  "
          f"avg latency: {int(sum(lat)/len(lat)) if lat else 0}ms")
    for ag, c in sorted(by_agent.items(), key=lambda x: -x[1]):
        print(f"    {ag:<16} ${c:.4f}")
    return 0


def cmd_pricing(_a):
    for m, p in sorted(PRICING.items()):
        print(f"  {m:<22} in ${p['input']:.2f}/1M  out ${p['output']:.2f}/1M")
    return 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("record")
    r.add_argument("--model", required=True)
    r.add_argument("--in", dest="in_tok", type=int, required=True)
    r.add_argument("--out", dest="out_tok", type=int, required=True)
    r.add_argument("--latency", type=int, default=0)
    r.add_argument("--agent", default=None)
    r.add_argument("--log", default=str(DEFAULT_LOG))
    r.set_defaults(fn=cmd_record)

    g = sub.add_parser("gate")
    g.add_argument("--ceiling", type=float, required=True)
    g.add_argument("--log", default=str(DEFAULT_LOG))
    g.set_defaults(fn=cmd_gate)

    rp = sub.add_parser("report")
    rp.add_argument("--log", default=str(DEFAULT_LOG))
    rp.set_defaults(fn=cmd_report)

    pr = sub.add_parser("pricing")
    pr.set_defaults(fn=cmd_pricing)

    a = ap.parse_args()
    sys.exit(a.fn(a))


if __name__ == "__main__":
    main()
