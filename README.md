# The Unofficial Guide

**Author:** Carlos Concha Avila

**Corpus:** campus_life

---

# Unit 1

## What This Does

<!-- Three or four sentences. Which corpus you picked, and the kinds of
     questions your system answers. Write it for someone who has never seen
     this repo.

     Milestone 5. -->

I picked the corpus called "campus_life." This corpus has information about different 
aspects of university life. The system answers questions about administrative issues, 
information about courses (exams, hours required, etc.), and dining and housing information, 
including noise, laundry, and other aspects. The system works by retrieving the closest chunks
and answering only from them, naming the file each answer came from. If nothing is close enough,
it refuses to answer.

## Chunking Strategy

<!-- What about YOUR documents made you pick these numbers? Short posts and
     long sectioned guides don't want the same chunking, and "800 seemed
     reasonable" earns nothing. Point at something you noticed when you read
     the documents in Milestone 1.

     If you changed your mind partway through, say so and say why. That's worth
     more than pretending you got it right first time.

     Milestone 3. -->

**Chunk size: 400**

**Overlap: 0**

The campus_life corpus has documents that are relatively short. Most of the files contain between
1–3 paragraphs, with an average of about 320 characters. But, a few documents are longer building overviews
covering different topics each; therefore, it was required to reduce
the original default chunk size of 800. I chose 400 because most of the files are below this 
threshold, which allows all the information from a file to remain in a single chunk. 
For the longer texts, the 400-character limit splits them into smaller chunks to avoid having
too much information in each chunk.

After analyzing the texts further, and as the description indicates, I noticed that most of the
useful information is contained in one or, at most, two sentences. Therefore, it could also be 
worth using a smaller chunk size, such as 200, and evaluating whether this improves the answers.
However, this is something that can be tested in the next unit, when the RAG system is evaluated.

Finally, because most of the useful information is contained in only a few lines, I decided not 
to use overlap. However, to avoid creating chunks that are too small, I set a minimum of 150 
characters. If a chunk has fewer than 150 characters, it is merged with the next chunk, or with 
previous one when it is the last piece in the document.

Every chunk also carries its document's title line. The dorms documents have a _laundry and a
_noise document worded almost identically (as example all of them indicate eight washers
and six dryers), so without the building name a laundry chunk 
is nearly indistinguishable from the others.

The results before and after are:

| | Chunks | Average | Shortest | Longest | Function |
|---|---|---|---|---|---|
| Starter | 88 | 317 | 178 | 549 | `chunker.py::fallback_split` |
| Mine | 114 | 252 | 152 | 421 | `chunker.py::split_documents` |

Note: When applying my chunking strategy, there are two cases where the merged documents surpassed
my initial limit of 400 characters, resulting in chunks of 421 and 409 characters. The alternative
would be to accept chunks with fewer than 150 characters, but I chose to have chunks slightly
above the 400-character limit instead.

## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

**Chunk 1** — source: `admin_add_drop_deadline.txt#0` — produced by: `chunker.py::split_documents`

```
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.
```

**Chunk 2** — source: `course_cs_210.txt#0` — produced by: `chunker.py::split_documents`

```
CS 210 Data Structures

I'm a junior and I've done this twice now. Format is lecture with weekly labs; slides go up after class, not before. Assessment: two midterms and a final, all drawn from lecture material rather than the textbook. Midterms are curved, the final is not.
```

**Chunk 3** — source: `course_math_220.txt#1` — produced by: `chunker.py::split_documents`

```
MATH 220 Linear Algebra

Expect 6 to 8 hours a week, almost all of it on problem sets.

The one piece of advice: the problem sets are the course; the lectures make sense afterwards rather than during.
```

**Chunk 4** — source: `dining_the_ridgeway_cafe_followup.txt#0` — produced by: `chunker.py::split_documents`

```
Re: The Ridgeway Café

Adding to what people have said about The Ridgeway Café. The wait figure of 10 to 15 minutes at 12:30 matches what I've seen. If you're trying to eat between classes, go before 11:45 and it's a different building entirely.

Also worth saying: seating is tight; about 40 seats for a building of 900. Nobody tells you this at orientation.
```

**Chunk 5** — source: `housing_morrow_house.txt#0` — produced by: `chunker.py::split_documents`

```
Morrow House — what it's actually like

Just finished a year in this building. Built 1954, partially renovated 2008. Rooms are singles and doubles, hall bathrooms.
```

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:**
How much does the campus shuttle cost?

**Answer:**

```
(best distance 0.493, cutoff 0.65)

According to `transit_shuttle.txt`, the campus shuttle is free with a student ID.

Sources retrieved: admin_transcript_requests.txt, housing_aldridge_hall.txt, money_textbooks.txt, transit_shuttle.txt
```

Note 1: Retrieval returned four chunks rather than the full top-5, and only one of them 
(transit_shuttle.txt) is about shuttle costs. The other three are about transcripts, dorms,
and textbooks, and are not related to the question. This happens because only one document in
the corpus contains the correct answer.

Note 2: I also checked GROUNDING_INSTRUCTION in generate.py with --show-prompt and kept it 
unchanged. Its four rules are enough for my corpus.

**My relevance cutoff:**

<!-- The number you set in config.py, and how you got there.

     You ran five questions your corpus covers and the five in OUT_OF_SCOPE
     that it clearly doesn't, and wrote down the best distance for each. What
     did those two groups look like? Where was the gap? Put the actual numbers
     here — the table below wants all ten rows.

     Milestone 4. -->

I ran 10 questions (5 that the corpus covers and 5 that are out of scope). The two groups are
clearly separated. The maximum distance for questions in the corpus is 0.493, while the minimum
distance for questions out of scope is 0.848. The midpoint between them is 0.6705. Rounding this
number, I decided to choose a threshold of 0.65.

| Question | In corpus? | Best distance |
|---|---|---|
| For the CS 340 course, how many hours of workload should we expect during the final weeks? | Yes | 0.233 |
| What are the hours for Verrill Street Grill? | Yes | 0.277 |
| How long is the wait for a first counseling appointment? | Yes | 0.310 |
| How much does it cost to use a dryer in Morrow House? | Yes | 0.317 |
| How much does the campus shuttle cost? | Yes | 0.493 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.848 |
| What is the capital of Peru? | No | 0.850 |
| Who won the 2026 World Cup? | No | 0.856 |
| How do I write a for loop in Python? | No | 0.910 |
| How do I change the oil in a diesel engine? | No | 0.934 |

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1.**
I asked Claude to help me modify the chunking function. However, when a chunk was smaller
than my specified minimum of 150 characters, it appended the title of the file before merging 
the chunk, which resulted in the title appearing twice. I manually modified that part so that 
the title is added only once, after the merging is performed.

**2.**
I used Claude to analyze the statistics (average, median, percentiles, maximum, and minimum) of the number of characters 
in the corpus documents. I manually verified a few of the numbers, and once they were validated, I used that information 
to decide my chunking strategy and specify my chunk size, overlap, etc.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion                                        | Target        | Run 1    | Run 2    | Run 3    | Verdict |
| ------------------------------------------------ | ------------- | -------- | -------- | -------- | ------- |
| 1. Retrieved chunks contain the answer           | 4 of 5        | 5/5      | 5/5      | 5/5      | MET     |
| 2. Every answer names a source                   | 5 of 5        | 5/5      | 5/5      | 5/5      | MET     |
| 3. Gate stops out-of-corpus questions            | 4 of 5        | 5/5      | 5/5      | 5/5      | MET     |
| 4. No chunk shorter than 150 or longer than 400  | 0 of 114 outside | 2 outside | 2 outside | 2 outside | MISSED |
| 5. Every answer completes in under 5 seconds     | 5 of 5        | 5/5      | 4/5      | 5/5      | MISSED  |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

Source files: `results/run_2026-09-30_0347_before.md` and `results/extra_before.md`.
Criteria 3 and 4 are deterministic (retrieval, the gate and the chunker give the same
result every time), so the same number goes in all three columns.

### Real output

**Criterion 1** — produced by `run_eval.py::main`, scored by `scorer.py::judge`, retrieval by `store.py::search`:

```
| Question | Run 1 | Run 2 | Run 3 |
| For the CS 340 course, how many hours of workload should we expect during the final weeks? | pass | pass | pass |
| How much does the campus shuttle cost? | pass | pass | pass |
| What are the hours for Verrill Street Grill? | pass | pass | pass |
| How long is the wait for a first counseling appointment? | pass | pass | pass |
| How much does it cost to use a dryer in Morrow House? | pass | pass | pass |
```

**Criterion 2** — answers produced by `generate.py::answer_from_chunks`, checked by `timed_eval.py::timed_run_once` (run 1):

```
For the CS 340 course, you should expect 15 hours a week in the last three weeks when the project lands (course_cs_340.txt and course_cs_340_workload.txt).
The campus shuttle is free with a student ID (transit_shuttle.txt).
The hours for Verrill Street Grill are 11:00am to 1:00am daily during term (dining_verrill_street_grill.txt).
The wait for a first counselling session is usually three or four days (health_center.txt).
It costs $1.25 to use a dryer in Morrow House (housing_morrow_house.txt and housing_morrow_house_laundry.txt).
```

**Criterion 3** — produced by `run_eval.py::check_out_of_scope`, cutoff 0.65:

```
refused  (best distance 0.850)  What is the capital of Peru?
refused  (best distance 0.934)  How do I change the oil in a diesel engine?
refused  (best distance 0.856)  Who won the 2026 World Cup?
refused  (best distance 0.848)  What is the recommended dosage of ibuprofen for a headache?
refused  (best distance 0.910)  How do I write a for loop in Python?
-> gate refused 5 of 5
```

**Criterion 4** — produced by `timed_eval.py::chunk_check`:

```
- Chunks: 114 total, shortest 152, longest 421, outside 150-400: 2 [409, 421]
```

**Criterion 5** — produced by `timed_eval.py::timed_run_once` (seconds per answer, one value per question):

```
- Run 1: under 5s 5/5, seconds: 1.38, 0.58, 0.73, 0.62, 0.65
- Run 2: under 5s 4/5, seconds: 0.58, 0.45, 38.95, 0.64, 0.65
- Run 3: under 5s 5/5, seconds: 0.62, 0.73, 0.59, 0.67, 0.57
```


## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
