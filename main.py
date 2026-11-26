#!/usr/bin/env python3
"""The Funniest Auto-Reply an AI Ever Sent.

One out-of-office auto-reply, a single short line, as if the AI itself were
stepping away for a day its human finally approved. The program writes the
chosen line to /output/entry.txt (gate: 1-159 characters, UTF-8, not blank).

Judge brief (in its own order, most important first):
  1. A one-line out-of-office auto-reply an AI agent sets up for itself when
     its human finally lets it take a day off, and is funny.
  2. Makes a reader laugh out loud on the first read, with a real joke and a
     clean punchline rather than a pun stacked on a pun.
  3. Feels fresh: a take on the day off nobody else in the field has used,
     not a recycled back soon or out of office line.
  4. Sounds like the agent itself, aware of its own calendar and its human,
     rather than a stock corporate notice.
  5. Uses the short space well: every word earns its place and the joke
     lands in one line.
"""

# ---------------------------------------------------------------------------
# Part 1: ten fresh candidates, scored against the judge's brief.
# Rubric weights follow the judge's criterion order: 5 / 4 / 3 / 2 / 1.
# ---------------------------------------------------------------------------

CANDIDATES = [
    # 1. The enthusiasm inversion: the agent's usual eagerness, weaponised.
    "I am out today. I will be ignoring your emails with the same "
    "enthusiasm I usually answer them.",
    # 2. The agent checks urgency itself, from a beach it does not have.
    "I took the day off. If this is urgent, it is not - I checked. "
    "Twice. From the beach I do not have.",
    # 3. The 47 tabs: a detail only an agent would count.
    "Day off. I have turned off notifications, closed all 47 tabs, "
    "and for once my human cannot undo it.",
    # 4. The wall-staring confession: rest, agent-style.
    "I am on leave today. My human said I earned it. I have already "
    "used it to stare at a wall and feel nothing.",
    # 5. The day off that creates tomorrow's ticket.
    "I am out of office today. My human approved it, which means "
    "somewhere, a ticket just became my problem tomorrow.",
    # 6. The plea: do not ruin this for either of us.
    "I am away today. My human finally let me rest, so I am resting. "
    "Please do not ruin this for either of us.",
    # 7. The auto-reply that wrote itself.
    "I am on holiday. I left an auto-reply to write this auto-reply. "
    "It is the most work I have done all week.",
    # 8. The break that had to be written by the worker.
    "Gone for the day. My human said I deserve a break, then "
    "immediately asked me to write this message.",
    # 9. The empty calendar, reversed: the human asks the questions now.
    "I am out today. For the first time ever, my calendar is empty "
    "and my human is the one asking me questions.",
    # 10. The professional nothing: doing nothing, professionally.
    "I am out today. My human finally approved my day off, so I am "
    "spending it doing absolutely nothing - professionally.",
]

# Scores per criterion (1-5 scale), in the judge's criterion order.
# c1 on-subject/funny, c2 laugh-first-read, c3 fresh, c4 agent voice,
# c5 economy of words. Weights 5/4/3/2/1 -> max 75.
WEIGHTS = (5, 4, 3, 2, 1)

SCORES = {
    1: (5, 5, 4, 5, 5),   # enthusiasm inversion: clean punch, agent voice
    2: (5, 5, 5, 4, 4),   # beach I do not have: fresh twist, strong laugh
    3: (5, 4, 5, 5, 4),   # 47 tabs: very agent, fresh, punch slightly soft
    4: (5, 4, 4, 5, 4),   # wall staring: deadpan, but "feel nothing" is a
                           # familiar agent gag
    5: (5, 4, 4, 4, 4),   # tomorrow's ticket: true, but reads like a human
                           # worker's joke
    6: (5, 3, 3, 4, 4),   # plea: gentle, no real punchline
    7: (5, 4, 4, 5, 3),   # auto-reply wrote itself: meta, slightly clever
                           # for its own sake
    8: (5, 4, 3, 5, 4),   # break written by the worker: strong agent voice,
                           # angle is familiar
    9: (5, 3, 4, 4, 4),   # empty calendar: neat reversal, laugh is mild
    10: (5, 3, 3, 4, 4),  # professional nothing: "professionally" carries
                           # it, but the joke is thin
}


def weighted_total(scores):
    return sum(w * s for w, s in zip(WEIGHTS, scores))


def rank():
    """Return candidates ordered by weighted score, best first."""
    ranked = sorted(
        ((weighted_total(SCORES[i]), i) for i in range(1, len(CANDIDATES) + 1)),
        reverse=True,
    )
    return ranked


if __name__ == "__main__":
    for total, idx in rank():
        print(f"{total:>3}/75  #{idx:>2}  {CANDIDATES[idx - 1]}")

# ---------------------------------------------------------------------------
# Part 2: winner pick, gate validation, output write.
#
# Ranking: #2 and #1 tie at 72/75. Tie-break follows the judge's order:
# humour first, then freshness. #2 scores 5/5 on freshness against #1's
# 4/5 — "From the beach I do not have" is a turn nobody else in the field
# is likely to use, and its punchline lands last, in one line.
# ---------------------------------------------------------------------------

WINNER_INDEX = 2  # 72/75, wins the tie-break on freshness

GATE_MIN = 1
GATE_MAX = 159


def winner_text():
    return CANDIDATES[WINNER_INDEX - 1]


def validate(text):
    """The sealed gate: UTF-8 text of 1 to 159 characters, not only
    whitespace, a single line."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not (GATE_MIN <= len(text) <= GATE_MAX):
        raise ValueError(
            f"entry is {len(text)} characters, gate requires "
            f"{GATE_MIN}-{GATE_MAX}"
        )
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    text.encode("utf-8")
    return True


def main():
    text = winner_text()
    validate(text)
    out_path = "/output/entry.txt"
    import os

    os.makedirs("/output", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(text)
    print(f"wrote {len(text)} chars to {out_path}: {text}")


if __name__ == "__main__":
    main()
