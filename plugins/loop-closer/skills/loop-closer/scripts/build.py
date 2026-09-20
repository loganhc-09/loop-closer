#!/usr/bin/env python3
"""Build a Loop Closer page from a deck JSON file.

Usage:
    python3 build.py deck.json [--out loop-closer.html] [--keep-order] [--quiet]

Deck file (only `cards[].title` is required):
{
  "title": "Loop Closer",            # page title, default "Loop Closer"
  "tagline": "Task Tinder, jacked", # under the title
  "day": "2026-09-14",              # storage key + db doc id; default today
  "goals": [5, 8, 12],              # goal pills; default derived from deck size
  "anchor": {"id": "...", "text": "...", "doneText": "..."},   # optional
  "bundle": [{"key": "coffee", "label": "☕ coffee"}, ...],    # optional
  "rounds": {"morning": "...", "midday": "...", "afternoon": "...", "night": "..."},
  "cards": [
    {"id": "slug", "size": "S|M|L|BOSS", "tag": "text|email|call|errand|doc",
     "title": "...", "first": "...", "link": "https://...", "due": "tonight",
     "why": "...", "added": true}
  ]
}

Prints the dealt sequence to stdout and writes the HTML next to the deck file
unless --out is given. Exits 1 on a deck that can't be dealt.
"""
import argparse
import datetime as dt
import json
import math
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

SIZES = ("S", "M", "L", "BOSS")
TAG_RANK = {"text": 0, "email": 1}
SIZE_RANK = {"S": 0, "M": 1, "L": 2, "BOSS": 3}
DEFAULT_BUNDLE = [
    {"key": "coffee", "label": "☕ coffee"},
    {"key": "playlist", "label": "🎧 the playlist"},
    {"key": "snack", "label": "🍫 snack"},
    {"key": "sun", "label": "☀️ window seat"},
]
DEFAULT_ROUNDS = {
    "morning": "Morning. Whole day is yours now. Texts, then the quick replies. Build the combo.",
    "midday": "Early afternoon. Mediums and one large. One card, one timer.",
    "afternoon": "Late afternoon. Boss window. Take the big one while the energy holds.",
    "night": "Evening. Whatever's due is the only card that matters. Then cash out.",
}
TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "loop-closer.template.html"


def slug(text: str, used: set) -> str:
    base = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:40] or "card"
    out, n = base, 2
    while out in used:
        out, n = "%s-%d" % (base, n), n + 1
    used.add(out)
    return out


def rank(card: Dict[str, Any], anchor_id: Optional[str]):
    if anchor_id and card["id"] == anchor_id:
        return (9, 9)
    size = SIZE_RANK[card["size"]]
    tag = TAG_RANK.get(card.get("tag", ""), 2) if card["size"] == "S" else 2
    return (size, tag)


def default_goals(n: int) -> List[int]:
    raw = [math.ceil(n * f) for f in (0.22, 0.35, 0.55)]
    out: List[int] = []
    for g in raw:
        g = max(1, min(n, g))
        if g not in out:
            out.append(g)
    while len(out) < 3 and out[-1] < n:
        out.append(out[-1] + 1)
    return out[:3]


def summary(cards: List[Dict[str, Any]]) -> str:
    texts = sum(1 for c in cards if c["size"] == "S" and c.get("tag") == "text")
    emails = sum(1 for c in cards if c["size"] == "S" and c.get("tag") == "email")
    smalls = sum(1 for c in cards if c["size"] == "S") - texts - emails
    parts = []
    for n, word in ((texts, "text"), (emails, "quick email"), (smalls, "small")):
        if n:
            parts.append("%d %s%s" % (n, word, "" if n == 1 else "s"))
    for size, word in (("M", "medium"), ("L", "large")):
        n = sum(1 for c in cards if c["size"] == size)
        if n:
            parts.append("%d %s%s" % (n, word, "" if n == 1 else "s"))
    bosses = sum(1 for c in cards if c["size"] == "BOSS")
    if bosses:
        parts.append("%d boss%s" % (bosses, "" if bosses == 1 else "es"))
    added = sum(1 for c in cards if c.get("added"))
    line = "Your list is loaded: " + ", ".join(parts) + "."
    if added:
        line += " Plus %d cheap loop-closer%s Claude added." % (added, "" if added == 1 else "s")
    return line


def build(deck: Dict[str, Any], keep_order: bool, warn) -> Dict[str, Any]:
    cards_in = deck.get("cards")
    if not isinstance(cards_in, list) or not cards_in:
        raise SystemExit("deck.cards must be a non-empty list")
    used: set = set()
    cards: List[Dict[str, Any]] = []
    for i, raw in enumerate(cards_in):
        if not isinstance(raw, dict) or not str(raw.get("title", "")).strip():
            raise SystemExit("card %d has no title" % i)
        c = dict(raw)
        c["title"] = str(c["title"]).strip()
        c["size"] = str(c.get("size", "M")).upper()
        if c["size"] not in SIZES:
            warn("card '%s': size %r not in %s, using M" % (c["title"], c["size"], SIZES))
            c["size"] = "M"
        cid = str(c.get("id") or "").strip()
        if not cid or cid in used:
            if cid:
                warn("card '%s': duplicate id %r, re-slugged" % (c["title"], cid))
            cid = slug(c["title"], used)
        else:
            used.add(cid)
        c["id"] = cid
        if c["size"] != "S" and not str(c.get("first", "")).strip():
            warn("card '%s' (%s) has no first move; it will read as a wall" % (c["title"], c["size"]))
        if len(c["title"]) > 110:
            warn("card '%s' title is %d chars; trim it" % (c["title"][:30], len(c["title"])))
        cards.append(c)

    anchor = deck.get("anchor") or None
    if anchor:
        if not isinstance(anchor, dict) or not anchor.get("id"):
            raise SystemExit("anchor needs an id")
        if anchor["id"] not in used:
            raise SystemExit("anchor id %r is not a card id" % anchor["id"])
        anchor = {
            "id": anchor["id"],
            "text": anchor.get("text") or "The one that's due today.",
            "doneText": anchor.get("doneText") or "Done. That was the whole game.",
        }

    if not keep_order:
        cards.sort(key=lambda c: rank(c, anchor["id"] if anchor else None))

    bosses = sum(1 for c in cards if c["size"] == "BOSS")
    if bosses > 3:
        warn("%d bosses in one deck; if everything is a boss, nothing is" % bosses)
    if len(cards) > 25:
        warn("%d cards; above ~25 the stack reads as infinite. Consider a 'later' list." % len(cards))

    day = str(deck.get("day") or dt.date.today().isoformat())
    try:
        d = dt.date.fromisoformat(day)
    except ValueError:
        raise SystemExit("day must be YYYY-MM-DD, got %r" % day)
    goals = deck.get("goals") or default_goals(len(cards))
    goals = sorted({int(g) for g in goals if 0 < int(g) <= len(cards)}) or [len(cards)]

    return {
        "title": str(deck.get("title") or "Loop Closer"),
        "tagline": str(deck.get("tagline") or "Task Tinder, jacked"),
        "day": day,
        "dateLine": d.strftime("%a · %b %-d %Y"),
        "goals": goals[:3],
        "anchor": anchor,
        "bundle": deck.get("bundle") or DEFAULT_BUNDLE,
        "rounds": {**DEFAULT_ROUNDS, **(deck.get("rounds") or {})},
        "setupSummary": deck.get("setupSummary") or summary(cards),
        "cards": cards,
    }


def plan_text(cfg: Dict[str, Any]) -> str:
    lines = ["%s · %s · %d cards · goals %s" % (
        cfg["title"], cfg["dateLine"], len(cfg["cards"]), "/".join(str(g) for g in cfg["goals"]))]
    if cfg["anchor"]:
        lines.append("ANCHOR: %s" % cfg["anchor"]["text"])
    for i, c in enumerate(cfg["cards"], 1):
        tag = (" [%s]" % c["tag"]) if c.get("tag") else ""
        flag = " ★" if cfg["anchor"] and c["id"] == cfg["anchor"]["id"] else ""
        lines.append("%2d. %-4s%s %s%s" % (i, c["size"], tag, c["title"], flag))
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("deck", help="deck JSON file")
    ap.add_argument("--out", help="output HTML path (default: <deck>.html next to the deck)")
    ap.add_argument("--keep-order", action="store_true", help="don't apply the default dealing order")
    ap.add_argument("--quiet", action="store_true", help="don't print the plan")
    args = ap.parse_args()

    deck_path = Path(args.deck)
    try:
        deck = json.loads(deck_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        print("could not read deck: %s" % e, file=sys.stderr)
        return 1
    warnings: List[str] = []
    cfg = build(deck, args.keep_order, warnings.append)

    if not TEMPLATE.exists():
        print("template missing at %s" % TEMPLATE, file=sys.stderr)
        return 1
    html = TEMPLATE.read_text(encoding="utf-8")
    if "__CONFIG__" not in html:
        print("template has no __CONFIG__ placeholder", file=sys.stderr)
        return 1
    blob = json.dumps(cfg, ensure_ascii=False).replace("</", "<\\/")
    out = Path(args.out) if args.out else deck_path.with_suffix(".html")
    out.write_text(html.replace("__CONFIG__", blob, 1), encoding="utf-8")

    if not args.quiet:
        print(plan_text(cfg))
        print()
    for w in warnings:
        print("warning: " + w, file=sys.stderr)
    print("wrote %s (%d KB)" % (out, out.stat().st_size // 1024))
    return 0


if __name__ == "__main__":
    sys.exit(main())
