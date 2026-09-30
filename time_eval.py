"""Runs run_eval.py unchanged and also measures criteria 2, 4 and 5."""
import sys
import time

import config
import run_eval
import store

N = 3  # runs per question, same as run_eval's default
log = []  # one (seconds, names_source) per call, in order q1 r1, q1 r2, q1 r3, q2 r1...
original = run_eval.run_once


def timed_run_once(question, *args):
    start = time.perf_counter()
    answer, results, decision = original(question, *args)
    seconds = time.perf_counter() - start
    log.append((seconds, any(r.source in answer for r in results)))
    return answer, results, decision


def chunk_check(variant):
    name = config.collection_name(None, variant)
    lengths = [len(d) for d in store._client().get_collection(name).get()["documents"]]
    bad = sorted(n for n in lengths if n < 150 or n > 400)
    return (f"Chunks: {len(lengths)} total, shortest {min(lengths)}, "
            f"longest {max(lengths)}, outside 150-400: {len(bad)} {bad}")


def arg(flag, default):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default


run_eval.run_once = timed_run_once
run_eval.main()

label = arg("--label", "run")
lines = [f"# Extra checks - {label}", "",
         "Criteria 2 and 5 produced by `timed_eval.py::timed_run_once`, "
         "criterion 4 by `timed_eval.py::chunk_check`.", ""]
for run in range(N):
    calls = log[run::N]
    lines.append(f"- Run {run + 1}: names a source {sum(s for _, s in calls)}/{len(calls)}, "
                 f"under 5s {sum(t < 5 for t, _ in calls)}/{len(calls)}, "
                 f"seconds: {', '.join(f'{t:.2f}' for t, _ in calls)}")
lines.append("- " + chunk_check(arg("--variant", "default")))
path = config.RESULTS_DIR / f"extra_{label}.md"
path.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n" + "\n".join(lines) + f"\n\nWrote {path}")