"""scorer.py: decides whether one answer was right.

Does the answer contain the `expects` phrase?
Note: It catches a missing fact, but not an added (made-up) one.
"""


def judge(question, expects, answer, results) -> bool:
    if not expects:
        return False
    return expects.lower().strip() in answer.lower()