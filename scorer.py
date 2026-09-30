"""scorer.py: decides whether one answer was right.

Does the answer contain the `expects` phrase?
Note: It catches a missing fact, but not an added (made-up) one.
"""


def judge(question, expects, answer, results) -> bool:
    words = expects.lower().split()
    return any(all(w in r.text.lower() for w in words) for r in results)