# Sizing, first moves, and dealing order

This is the judgment layer. The app rewards by size and coaches by tag, so a sloppy size or a
vague first move shows up as a card the user swipes left on three times.

## Sizing

| Size | Minutes | XP | Timer | What it looks like |
|---|---|---|---|---|
| S | ≤ 5 | 10 | 5 | A text. A one-line reply. A booking. Sending something already written. |
| M | ~15 | 25 | 10 | A real email. A decision. A small fix. A calendar hold with two slots. |
| L | ~30 | 50 | 25 | A doc pass. A draft. Reviewing someone's work. Filling a form with thought. |
| BOSS | 45+ | 100 | 25 | The thing they've been avoiding for weeks. Anything with "finish" or "finalize" in it. |

Rules of thumb:

- Size by minutes, not dread. "Text Stacey about the measuring tape" that's been on the list
  for a month is an S. The month of avoidance is why it's on the deck, not why it's big.
- "Decide X" is an M, and the first move says so: "Pick one of these three. Deciding is the task."
- "Go through / review / edit" is an L. If the material is more than a few pages, BOSS.
- A BOSS should be rare. One or two per deck. If everything is a boss, nothing is.
- When torn between two sizes, pick the smaller one. The app has a "shrink it" door and a
  "did the first move only" chip credit, so under-sizing is recoverable. Over-sizing makes the
  card look like a wall.

## First moves

The first move is the whole trick. It converts "a task" into "the next two minutes." Write it
as if the user will read it at 4pm with no context and no willpower.

Good first moves:

- Text: the literal words. `"Bringing a measuring tape, fyi." Send.`
- Reply: `Open the last thread. Answer the one question they asked. Send.`
- Already-drafted thing: `It's already written and it's good. Open the draft, read it once, send.`
- Scheduling: `Send two slots from tomorrow afternoon. Or drop a calendar invite directly.`
- Decision: `Pick one: (a) ..., (b) ..., (c) .... Then send the message. Deciding is the task.`
- Doc pass: `Open essay 1. Terse comments, one holistic note at the end. Then essay 2.`
- Boss: `The six docs exist. Fill company #1's brackets. Export PDF. Then the next one.`
- Unclear task: `Write the one question you'd ask if someone were sitting here. That sentence is the task now.`

Failed first moves:

- Restating the title. Title "Write the report", first move "Write the report."
- Advice. "Try to focus on the key points." That's not a move.
- A plan with five steps. Give the first step; the timer and "chain it" handle the rest.
- Anything with "should", "consider", or "make sure".

For S cards the app labels the box "2-min rule · just do it", so a first move is optional. Add
one anyway when you can write the actual words; it removes the last decision.

## Tags

`text`, `email`, `call`, `errand`, `doc`. Tags feed the coach line ("Texts first. Thirty
seconds each, three in a row lights the combo." / "Email run. Same tab, same energy, don't
reread anything twice."). Tag anything that's a message; leave the rest untagged.

## Dealing order

Default sequence, applied by `build.py` as a stable sort:

1. Texts (S, tag text). Thirty seconds each. Three in a row lights the combo multiplier.
2. Quick emails (S, tag email). Same tab, same energy.
3. Other smalls.
4. Mediums.
5. Larges.
6. Bosses.
7. The anchor, last. The banner has "jump to it" for when the combo is hot.

Why smalls first: the combo multiplier (×1.5 at 2, ×2 at 4, ×3 at 6) makes the first boss
worth up to 300 XP if they arrive at it with momentum. The coach line says exactly this when
the combo hits 4 and a non-boss is on top. Momentum, then the frog.

When to override with `--keep-order`:

- The day is short and there's one thing that matters. Put it on top, make it the anchor too.
- They said "I need to do X before anything else." Believe them.
- Two tasks are sequential (send the draft, then text that it's sent). Keep them adjacent.

## The anchor

One card gets a banner and a "jump to it" button. It's for a real deadline today: the send
that has to go out tonight, the form due at midnight, the call at 3. If there's nothing like
that, skip the anchor. A fake deadline trains them to ignore the banner.

Anchor copy: `text` is the banner while it's open ("Ep26 recap: press send. The one rule.")
and `doneText` replaces it after ("Recap SENT. Streak 2. That's the whole game."). Both under
~60 characters. Give the anchor card a `due: "tonight"` chip too.

## Goal pills

`build.py` picks three goal counts from the deck size (roughly 22%, 35%, 55% of cards,
labeled gentle / solid / menace). The middle one is preselected. The user chooses, so the goal
is theirs; that's the autonomy half of self-determination theory doing work. You can override
with `"goals": [3, 5, 8]` in the deck file if the default looks wrong for the day.

## Deck size

Sweet spot is 12 to 25 cards. Under 8 the combo never gets going; consider asking what else
is rattling around. Over 25, the stack looks infinite even though only three cards show. Ask
which ten they'd be glad to have done by tonight, deal those plus the smalls, and hand the rest
back as a plain "later" list in your message.
