# Ticket Run

Brain dump in, swipeable task deck out. One day, one deck.

You tell Claude everything on your mind, in whatever shape it comes out. Claude sizes each item, writes a two-minute first move on every card, deals the deck so quick wins build a combo before the big scary thing, and hands you a one-page app: XP by size, a combo multiplier, random tickets with a jackpot, a focus timer, a "shrink it" door for cards that feel like a wall, recess every three clears, and a cash-out recap that ends the day on a high.

Built for brains that run on interest, novelty, challenge, and urgency rather than importance. Every mechanic maps to a named finding; the app lists them under "hacks in play."

Early build. It works; the edges are still being sanded. Feedback welcome in Issues.

## Install (Claude Code)

```
/plugin marketplace add loganhc-09/ticket-run-skill
/plugin install ticket-run@ticket-run
```

Then in any session, dump your list. Trigger phrases that work: "brain dump", "task tinder", "ticket run", "I have a million things", "help me get through my list", "make today a game". Or just paste the list and say you can't start.

If you'd rather skip the plugin system, download `ticket-run.skill` from the Releases tab, unzip it, and drop the `ticket-run` folder into `~/.claude/skills/`. The same folder works in Cursor (`~/.cursor/skills/`), and the `.skill` file can be uploaded to claude.ai under Settings, Capabilities, Skills.

## What Claude does with your dump

1. Takes it as-is. No item-by-item interrogation.
2. Makes a card per task: size (S ≤5 min, M ~15, L ~30, BOSS 45+ or long-avoided), a first move written so you could do it half-asleep, a tag for texts and emails, a link if you mentioned one, and one anchor if something is due today.
3. Builds the page with `scripts/build.py` and hands it over in under ten lines: the link, the goal you get to pick, the sequence in groups, one line of coaching.
4. When you come back with the recap, celebrates first. Skips and shelved cards are never counted.

## Trying it without installing

`plugins/ticket-run/skills/ticket-run/assets/example-deck.json` is a sample dump. Build it and open the result:

```
python3 plugins/ticket-run/skills/ticket-run/scripts/build.py \
  plugins/ticket-run/skills/ticket-run/assets/example-deck.json --out demo.html
open demo.html
```

Works on a phone too; AirDrop the file or open it from Files.

## What I'd love feedback on

- Did the sizes feel honest, or did something get inflated by dread?
- Was the first move on each card actually the first two minutes, or a restatement of the task?
- Did the dealing order (smalls first, boss last) get you moving, or would you have wanted the boss on top?
- Anything in the app that felt like a chore instead of a game.

## Layout

```
plugins/ticket-run/skills/ticket-run/
├── SKILL.md                     the flow and the rules
├── references/sequencing.md     sizing, first moves, dealing order
├── references/hacks.md          the 24 mechanics and what they mean for copy
├── scripts/build.py             deck.json → page
└── assets/ticket-run.template.html
```

MIT licensed.
