# Loop Closer

Every open loop in your head, out on the table and closed by tonight. (Task Tinder, dopamine edition. The install command is still `ticket-run`.)

You know the loops: the reply you owe, the form that's been open in a tab for a week, the thing you've been avoiding so long it's grown teeth. They don't sit still. They circle, and every lap costs you a little. This gets all of them out of your head in five minutes, turns each one into a card with a first move you could do half-asleep, and deals them in an order that makes closing them feel like a game instead of a reckoning.

**Try it right now, no install:** https://loganhc-09.github.io/ticket-run-skill/

## How this got made

The whole brief was three messages to Claude. Verbatim:

> can we build the most dopamine jacked version of my task tinder just for today? i have a long list of shit to get done most of which i've been procrastinating on

> let's use every psychological / ui ux / adhd coach hack known to humanity

Then, the next day:

> you know the new task tinder dopamine mode you made for me yesterday? could we put that into a skill for people? it starts off with the brain dump then whips up a sequence for you?

That's it. No spec, no wireframe. The second message is where every mechanic in the app came from: XP, combo multiplier, random tickets with a jackpot, focus timer, a "shrink it" door for cards that feel like a wall, recess every three clears, a cash-out recap that ends on a high. Claude pulled 24 named hacks from ADHD coaching and UX research and mapped each one to a mechanic. The app lists them under "hacks in play" so you can see what's being done to you.

The third message turned a one-day artifact into this skill. You say "brain dump," Claude takes whatever comes out, and the deck shows up. Close a loop, swipe, next.

## Use it

**In Claude (app or website).** You need a paid plan.

1. Download **ticket-run.skill** from the [Releases page](https://github.com/loganhc-09/ticket-run-skill/releases/latest). Don't unzip it.
2. claude.ai → your name (bottom-left) → **Settings** → **Capabilities** → **Skills** → **Upload skill**. Pick the file.
3. New chat. Type **brain dump**. Set a timer, talk or type, hit send.
4. Tap the deck's open-in-new-tab button so the cards have room. Before you close it, tap **cash out** and **copy recap**.

No Skills section in step 2? Your plan doesn't have custom skills on yet. The demo link at the top still works.

**Claude Code:**

```
/plugin marketplace add loganhc-09/ticket-run-skill
/plugin install ticket-run@ticket-run
```

**Cursor:** unzip `ticket-run.skill`, drop the `ticket-run` folder into `~/.cursor/skills/`.

Trigger phrases: "brain dump", "task tinder", "ticket run", "I have a million things", "make today a game". Or paste the list and say you can't start.

## What Claude does with your dump

- Takes it as-is. No item-by-item interrogation. Show up empty-handed and it runs a 5-minute guided dump instead: walk the rooms in your head, name every loop that's open.
- One card per task: a size (S ≤5 min, M ~15, L ~30, BOSS 45+ or long-avoided), a first move you could do half-asleep, and one anchor if something's due today.
- Deals the deck so quick wins build a combo before the big scary thing.
- When you come back with the recap, celebrates first. Skips are never counted.

## Feedback I want

- Did the sizes feel honest, or did dread inflate something?
- Was the first move on each card actually the first two minutes, or a restatement of the task?
- Smalls first, boss last: did that get you moving, or did you want the boss on top?
- Anything that felt like a chore instead of a game.

Open an Issue.

## Layout

```
plugins/ticket-run/skills/ticket-run/
├── SKILL.md                     the flow and the rules
├── references/sequencing.md     sizing, first moves, dealing order
├── references/hacks.md          the 24 mechanics and what they mean for copy
├── scripts/build.py             deck.json → page
└── assets/ticket-run.template.html
```

Rebuild the demo page from the sample dump:

```
python3 plugins/ticket-run/skills/ticket-run/scripts/build.py \
  plugins/ticket-run/skills/ticket-run/assets/example-deck.json --out demo.html
```

MIT licensed. Early build; edges still being sanded.
