---
name: ticket-run
description: "Turn a messy brain dump into a swipeable, game-like task deck for one day (Task Tinder, dopamine mode). The user dumps everything on their mind; you size each item, write a 2-minute first move for it, sequence the deck so quick wins build a combo before the big scary thing, and ship a one-page app with XP, timers, random tickets, and a cash-out recap. Use this whenever someone lists a pile of things they need to do and sounds stuck, scattered, overwhelmed, or avoidant. Triggers: 'brain dump', 'task tinder', 'ticket run', 'dopamine mode', 'make today a game', 'I have a million things', 'help me get through my list', 'ADHD mode', 'I can't start', 'gamify my day'. Trigger even if they never ask for an app, and even if the dump is a voice-memo transcript or a half-sentence list."
---

# Ticket Run

One day. One deck. The user brain-dumps, you deal the cards, they swipe. The app does the
dopamine: XP by size, a combo multiplier, random tickets with a jackpot, a focus timer, a "shrink
it" door for scary cards, recess every three clears, and a cash-out recap that ends the day on a
high. The mechanics are already built. Your job is the part that needs judgment: turning what
they said into cards worth swiping, in an order that gets them moving.

Why it works: an ADHD-ish brain doesn't run on importance, it runs on interest, novelty,
challenge, and urgency. A to-do list offers none of those. A deck with a timer, a multiplier,
and a first move printed on every card offers all four. `references/hacks.md` explains each
mechanic and where it shows up, so your card copy and coaching stay consistent with what the
app is doing.

## The flow

### 1. Take the dump as it comes

Accept whatever they give you: a voice memo transcript, a bulleted list, a rant, a paragraph
with "oh and also" three times. Don't interrogate them item by item. Every question you ask is
one more thing standing between them and the first swipe. If something is ambiguous, make a
reasonable card and let them fix it in the app (there's a "dump my list" button that adds cards
live).

If they invoked the skill with nothing to dump, ask for it in one line and stop:
"Dump everything. Messy is fine. One line per thing or just talk."

### 2. Make the cards

Read `references/sequencing.md` before this step. The short version:

- **Size** by honest minutes, not by how it feels. S ≤ 5 min (a text, a one-line reply, a
  booking), M ~15 (a real email, a decision, a small fix), L ~30 (a doc pass, a draft, a review),
  BOSS = 45+ or anything they've clearly been avoiding for weeks. Dread inflates size; a
  30-second text that's been sitting for a month is still an S.
- **First move** on every card: the literal first two minutes, written so they could do it
  half-asleep. For texts and quick replies, write the actual words to send. For anything bigger,
  name the one small piece with an edge to grab. A first move that just restates the task
  ("Write the report") is a failed first move.
- **Tag** texts, emails, calls, errands. The app uses tags to coach ("texts first, three in a
  row lights the combo").
- **Link** when they mentioned a place (a doc, an inbox, a form). One tap beats one search.
- **Anchor**: if one thing has a real deadline today, it becomes the anchor: a banner at the top
  with a "jump to it" button. One anchor, never two. If nothing is due today, no anchor.
- **Only their items.** Don't invent tasks. If the conversation clearly contains a cheap
  loop-closer they forgot (a reply that's already drafted, a form they mentioned), you may add it
  with `"added": true` so the card is labeled as yours. Rare, not routine.

### 3. Write the deck file

Save a JSON file (in your scratchpad or working dir) shaped like this:

```json
{
  "title": "Ticket Run",
  "day": "2026-09-14",
  "anchor": {"id": "send-invoice", "text": "Invoice to Sam goes out today. The one rule.", "doneText": "Invoice SENT. That was the whole game."},
  "cards": [
    {"id": "text-dana", "size": "S", "tag": "text", "title": "Text Dana about Saturday",
     "first": "\"Hey, still on for Sat? 10 works for me.\" Send."},
    {"id": "send-invoice", "size": "M", "tag": "email", "due": "today",
     "title": "Send the September invoice to Sam",
     "first": "Open last month's invoice. Duplicate it. Change the dates and the line items. Send.",
     "link": "https://..."},
    {"id": "deck-v2", "size": "BOSS", "title": "Rework the pitch deck for Thursday",
     "first": "Open the deck. Fix slide 2 only. Stop there if you need to."}
  ]
}
```

Fields: `title` is required. `size` defaults to M. `id` is optional (the build script slugs
the title). `first` is optional for S cards (they get "just do it"), expected for everything
else. `due`, `why`, `link`, `tag`, `added` are optional. `title`, `day`, `anchor`, `tagline`,
`bundle`, `rounds` are optional at the top level; see `scripts/build.py --help`.

Order the cards the way you want them dealt. The build script applies the default sequence
(texts, then quick emails, then other smalls, mediums, larges, bosses, anchor last) as a stable
sort, so your order within each group survives. Pass `--keep-order` if you've sequenced by hand
for a reason (e.g. one boss deliberately on top because the day is short).

### 4. Build it

```bash
python3 <skill-dir>/scripts/build.py deck.json --out ticket-run.html
```

It validates the deck, prints the dealt sequence as plain text, and writes the page. Read the
warnings: a missing first move on a BOSS is the kind of thing that makes the card unswipeable.

### 5. Ship it

- **If the Artifact tool is available**, publish the HTML with favicon 🎟️. Load the
  `artifact-design` skill first as the tool requires, but don't redesign the page; the look is
  deliberate. If the `artifact-capabilities` skill says a `db` capability exists for this user,
  declare it: the page then saves completions to `days/<day>` and you can read them back with
  `read_db` at the end of the day. Without it, the page saves in the browser only and the
  cash-out screen has a "copy recap" button they paste to you.
- **Otherwise**, write the file somewhere that won't vanish and open it: `open ticket-run.html`
  on macOS. Say where it is.

### 6. Hand it over in under ten lines

Give them the link, the goal pills you set (the build script picks three based on deck size),
the anchor if there is one, and the sequence in groups, not card by card. Then one line of
coaching that matches the top of the deck ("Three texts, thirty seconds each. Swipe the first
one."). No explanation of the mechanics; the app has a "hacks in play" button for the curious.
No pep talk. The point is to get them to the first swipe.

### 7. Cash out

When they come back with a recap, a pasted list, or "done": celebrate first, specifically.
Name the hardest thing they cleared. Notice a streak or a boss. Only after that, offer to close
the matching items in whatever task system they use. Never total up the skips or shelved cards;
"not today" was a real answer and the app told them so. If you have `db` access, read
`days/<day>` before they say anything and lead with what you found.

A new day is a new deck and a new `day` value. Don't reuse yesterday's order; the fresh-start
effect is one of the hacks.

## Voice for card copy

Short, imperative, concrete. "Open the draft, read it once, send." Not "You should consider
reviewing the draft." Contractions are fine. No exclamation points on cards; the app supplies
the excitement. Keep titles under ~80 characters and in the user's own words where possible.
If they said "deal with the Sam thing," the card says "Deal with the Sam thing" and the first
move is where you get specific.

## Things that go wrong

- Cards that are really three tasks. Split them; a combo needs clears.
- Every card sized M because you didn't want to guess. Guess. The user can shrink or shelve.
- Two anchors, or an anchor with no deadline. The banner loses meaning.
- A deck of 40. Above ~25 cards, ask which ten they'd be glad to have done by tonight and
  shelve the rest into a "later" list you hand back in text.
- Re-serving the same deck the next day. Rebuild from a fresh dump.
