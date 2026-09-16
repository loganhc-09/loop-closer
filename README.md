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

1. Takes it as-is. No item-by-item interrogation. If you show up empty-handed, it gives you a 5-minute guided dump instead: walk the rooms in your head (messages owed, dated things, the one you've been avoiding, life admin), and for anything big, say what it actually needs.
2. Makes a card per task: size (S ≤5 min, M ~15, L ~30, BOSS 45+ or long-avoided), a first move written so you could do it half-asleep, a tag for texts and emails, a link if you mentioned one, and one anchor if something is due today.
3. Builds the page with `scripts/build.py` and hands it over in under ten lines: the link, the goal you get to pick, the sequence in groups, one line of coaching.
4. When you come back with the recap, celebrates first. Skips and shelved cards are never counted.

## Just want to see it? (no install, no code)

**Open this on your phone or laptop:** https://loganhc-09.github.io/ticket-run-skill/

That's a demo deck with made-up tasks so you can feel the swipe, the timer, and the cash-out. Tap **+ dump my list** at the bottom to put your own things in. It won't size them or write first moves for you (that's the part Claude does), but you'll get the idea in about a minute.

## Using it in Claude (the app or website), step by step

You don't need Claude Code or a terminal for this. You need a paid Claude plan.

1. Go to the [Releases page](https://github.com/loganhc-09/ticket-run-skill/releases/latest) and click **ticket-run.skill** to download it. It's a small zip file. Don't unzip it.
2. Open claude.ai and click your name or initials in the bottom-left corner, then **Settings**.
3. Click **Capabilities** in the left menu, scroll to **Skills**, and click **Upload skill** (the wording may be slightly different). Pick the file you just downloaded.
4. Start a new chat and type: **brain dump**. Claude will explain what's about to happen and ask for everything on your mind. Set a timer, talk or type, hit send.
5. Claude builds your deck and shows it in the chat. Tap the little **open in full screen** or **open in new tab** button on it so the cards have room. Before you close it, tap **cash out** and **copy recap** so nothing's lost.

If step 3 doesn't show a Skills section, your plan or workspace doesn't have custom skills turned on yet. The demo link above still works.

## For people with a terminal (Claude Code or Cursor)

Claude Code, two commands:

```
/plugin marketplace add loganhc-09/ticket-run-skill
/plugin install ticket-run@ticket-run
```

Cursor: download and unzip `ticket-run.skill`, then move the `ticket-run` folder into `~/.cursor/skills/`. Claude Code also picks it up from `~/.claude/skills/`.

To rebuild the demo page yourself from the sample dump:

```
python3 plugins/ticket-run/skills/ticket-run/scripts/build.py \
  plugins/ticket-run/skills/ticket-run/assets/example-deck.json --out demo.html
open demo.html
```

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
