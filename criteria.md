# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
Three of my questions have an answer in only one document, and two questions 
have answers in two documents. However, there are topics that are discussed in several
documents. Therefore, there is a possibility that for at least one question the right
document does not reach the top 5 retrieved chunks.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
<!-- Why all five and not four? What about your setup makes that achievable —
     or what would have to go wrong for it not to be? -->
If the system does not produce at least one source document, then it is not 
possible to verify the answer. For that reason, unlike the other criteria, 
100% compliance is required here.

Also, the GROUNDING_INSTRUCTIONS in generate.py specifically indicates: 
"Name the document your answer came from, using the filename given in each 
excerpt." Therefore, 100% success should be achievable.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**
Even if the questions asked in this part are out of scope, some of them, 
such as the question about ibuprofen for headaches, could be related to
documents from the health center. For that reason, 4 out of 5 correct answers
are accepted.

---

## 4. Something about your chunks

No chunk is shorter than 150 characters or longer than 400 characters.

**Why this target:**
Most of the documents are below 400 characters, so most of the documents 
will have one chunk per document, allowing us to have all the required context
to answer the questions. The ones that exceed 400 characters are the general 
overviews of the houses (for example, housing_calder_annexe is 430 characters,
while housing_old_brewhouse is about 549 characters). They contain different 
types of information (the good, the bad, laundry, noise), so in those cases, 
it could be beneficial to split the document into two chunks. 

The 150-character floor avoids small fragments, such as a paragraph that only covers laundry 
information. If a split would produce a chunk under 150 characters, then it is 
merged with its neighboring chunk within the same document.

---

## 5. Your choice

For all the test questions, the answer is completed in under 5 seconds.


**Why this target:**
A tool that takes too long to answer can cause users to lose interest. This target is
realistic because the corpus only has 88 short chunks, with a maximum of 550 characters 
each. Therefore, retrieval should be almost instantaneous, and most of the time will be 
spent generating the answer.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
