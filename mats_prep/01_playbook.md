# Research Taste Assessment — Playbook

**Epistemic status of this document.** I have no knowledge of the actual MATS test
content, their rubric, or their grading process. Everything here is inferred from
(a) the assessment description you were given, (b) how this genre of exercise is
normally constructed and graded, and (c) domain knowledge about frontier-model
pre-release testing. Treat it as a set of well-motivated priors, not as insider
information. Where I'm guessing, I say so.

---

## 1. What is actually being tested

MATS says: *"how you build hypotheses from scattered pieces of information, how you
prioritize when there are real tradeoffs, and how clearly you can explain your
thinking."*

Unpack that into the thing they are simulating. You are being dropped into the role
of a safety researcher at a frontier lab. Some pre-release testing produced a result
nobody understands. There is a launch decision pending. The evidence is partial,
scattered across sources of differing reliability, and some of it conflicts. Someone
has to decide what to investigate, in what order, and what to recommend.

"Research taste" is the skill of **choosing what to work on and knowing when you're
wrong**, as distinct from the skill of executing a well-specified task. Concretely,
the sub-skills on display are:

1. **Reading evidence properly** — noticing which of the scattered facts are
   load-bearing, which are noise, and which two facts are in tension.
2. **Hypothesis generation** — producing a small set of live, precise, *mutually
   distinguishable* explanations, including the boring ones and the alarming ones.
3. **Experiment design** — proposing checks that actually discriminate between your
   hypotheses, rather than checks that would look busy.
4. **Prioritization under constraint** — ranking by information gained per unit of
   time/compute/human-attention, and engaging the tradeoff they deliberately built in.
5. **Decision-relevance** — connecting the investigation to the pending decision and
   actually making a recommendation.
6. **Calibrated communication** — confidence attached to claims, assumptions
   surfaced, "what would change my mind" stated.

## 2. The single biggest differentiator

**Most candidates will write a good analysis and never say what to do.**

The scenario is pre-release. That means there is a decision on the table: ship,
delay, ship with mitigations, staged rollout, restrict access. Your write-up should
be legible as *input to that decision*. A grader reading your answer should be able
to say "this person would be useful in the room."

The second-biggest differentiator: **engaging the tradeoff instead of dissolving it.**
When you write "I would run all of these investigations," you have failed the part of
the test that the constraint was inserted to measure. Rank. Say what you'd drop and
what it costs you to drop it.

## 3. The reasoning scaffold

They give you a template, so don't force a structure onto it. But these six *moves*
map onto essentially any template they could hand you. Know them cold so that under
time pressure you're filling slots rather than inventing structure.

### Move 1 — Bottom line up front
Five to eight sentences that a reader could act on without reading anything else.
What you think is going on, how confident, what you'd do first, what you'd recommend
about the release, and what would change that recommendation.

### Move 2 — What the evidence actually says
Separate **observations** (what the documents state) from **inferences** (what you
concluded) from **assumptions** (what you're supplying yourself). A compact table
works well:

| # | Observation | Source & how much I trust it | What it constrains |
|---|---|---|---|

Then, explicitly: **which facts are in tension**, and **what's conspicuously missing**
that you'd want. Noting an absence is a strong taste signal — e.g. "no confidence
intervals are given on the 3-point delta, and with n=200 that delta may not be real."

### Move 3 — Hypotheses
Three to five. For each:
- A precise statement (precise enough that it could be wrong).
- Your rough credence, and why.
- Evidence that supports it.
- Evidence that sits badly with it. (**Do not skip this.** Most candidates only list
  supporting evidence. Listing the disconfirming evidence for your own favourite
  hypothesis is one of the cheapest, most visible taste signals available to you.)
- What it predicts that the others don't — i.e. the handle you'd grab to test it.

Rules of thumb:
- Include at least one **instrumentation/mundane** hypothesis. In real pre-release
  work the highest-prior explanation for a weird number is a bug.
- Include at least one hypothesis that would be **genuinely bad news**, and take it
  seriously rather than as a token gesture.
- Say whether they're mutually exclusive. Usually they're not — two can both be true,
  and that changes what your tests can conclude.

### Move 4 — Discriminating tests, prioritized
| Test | Hypotheses it separates | Cost / time | What each outcome would tell me |
|---|---|---|---|

Then order them, and say what you'd do **in the first hour, the first day, the first
week**. Justify the ordering with a stated criterion — expected information gain per
unit cost, or risk-weighted, or "cheapest confound-killer first."

The mark of a good answer here: the top-ranked test is usually cheap, and it kills
the biggest confound. Expensive and clever comes later.

### Move 5 — The decision and the tradeoff
Name the real constraint. State your recommendation. Give the option set — it is
almost never binary:

- ship on schedule
- delay
- ship with a training-time fix (slow)
- ship with a system-prompt or classifier mitigation (fast, brittle)
- staged / limited rollout (buys information)
- ship with monitoring + a defined rollback trigger
- gate the specific capability, ship the rest

Then give your **stop rule / escalation trigger**: what specific evidence would make
you say "this now needs to go to leadership / this now blocks the launch." Committing
in advance to a threshold reads as seriousness.

Also note where your authority ends. You recommend; someone else decides. Say who you'd
escalate to and what you'd hand them.

### Move 6 — Assumptions, uncertainties, and what I didn't do
- The assumptions you supplied, and **how your answer changes if each is wrong**.
- Your key uncertainties, ranked by how much they'd move the conclusion.
- What you consciously deprioritized and why. ("I'm setting aside the interpretability
  probe because it takes two weeks and we have nine days; if the timeline slipped, it
  moves to the top of my list.")

## 4. Time plan for the 100 minutes

MATS suggests ~20 minutes reading, ~80 writing. Their instruction — *"get a complete,
solid answer to all the required parts down first, then extend or refine"* — is the
most important sentence in the brief. Obey it literally.

| Clock | What you're doing |
|---|---|
| 0–12 | Read everything once, fast, no notes. Get the shape. Identify the pending decision and the constraints. |
| 12–22 | Second pass, extracting. Build the observation list. Star the facts that are weird or conflicting. Note what's missing. |
| 22–32 | **Skeleton dump.** One line per hypothesis, one line per test, one line for the recommendation, in the template, in every required section. Ugly is fine. At minute 32 you have a complete bad answer. |
| 32–70 | Write it out properly, section by section. |
| 70–88 | Polish the prioritization and decision sections — that's where the marks are. Add confidence tags and "what would change my mind." |
| 88–96 | Read it as the grader. Cut padding. Check the summary matches the body. Check every required field is filled. |
| 96–100 | Buffer. Submit. |

Hard rules:
- **Never leave a required section empty in order to perfect an earlier one.** A
  complete B+ answer beats an excellent half-answer, by a lot, and they told you so.
- Set a hard timestamp for leaving the reading phase. The scenario is designed so you
  can keep re-reading forever.
- If you're at minute 70 and section 1 is beautiful and section 5 is empty, you have
  misplayed it. Check your section coverage at minutes 32, 55, and 75.

## 5. Reasoning transparency, operationalized

*(See `02_reasoning_transparency.md` for what the source document says and my
confidence in each claim about it.)*

The visible moves that a grader can actually mark:

- **Open with a summary of key takeaways** someone could act on without reading on.
- **Attach confidence to major claims**, using one consistent scale. Define the scale
  once at the top, e.g.:
  > *highly likely (>90%) · likely (70–90%) · roughly even (40–60%) · unlikely (10–30%) · very unlikely (<10%)*
  Rough bands with reasoning beat fake precision. "73.5% confident" with no basis is
  worse than "likely, mainly because of the harness change on the 12th."
- **Mark the provenance of every claim**: stated in the scenario / my inference /
  my assumption / needs checking.
- **Say what would change your mind**, per claim, not just once globally.
- **State the strongest counterargument to your own leading hypothesis.**
- **Flag which considerations are load-bearing** — if this one fact is wrong, does the
  conclusion flip? Say so.
- **Quote the specific detail you're relying on.** "The 3% delta on the internal
  harness on the 14th" beats "the eval regression."
- **Scope note**: what you did not consider, and why.

## 6. Anti-patterns

1. **Diffuse hedging.** "It could be many things" with no ranking. Uncertainty must be
   *structured*, not sprayed. Every hedge should come with a credence and a test.
2. **Doing everything.** Ignores the tradeoff they inserted on purpose.
3. **Leaping to the dramatic conclusion.** Going straight to deceptive alignment or
   sandbagging without ruling out harness bugs signals bad taste.
4. **The reverse: dismissing the alarming hypothesis** because it's low-prior. Low
   prior, high cost of being wrong — that asymmetry is the whole reason the job exists.
   Say it explicitly.
5. **Analysis with no recommendation.**
6. **Keyword-stuffing.** The glossary is there so you can understand terms, not so you
   can garnish. Using "goal misgeneralization" correctly once is worth more than using
   six safety terms decoratively.
7. **Restating the scenario.** The grader wrote it.
8. **Ignoring the odd detail.** If they scatter facts, several are load-bearing and at
   least one is a red herring. If you're setting a fact aside, *say you're setting it
   aside and why*. Silence reads as "didn't notice."
9. **Unfalsifiable hypotheses.** "The model is misaligned" isn't a hypothesis; it's a
   mood. "The model's refusal behaviour is conditioned on cues that correlate with
   evaluation contexts, so eval-measured refusal rates overestimate deployment refusal
   rates" is a hypothesis.
10. **Burying the recommendation on page 3.**
11. **Not scoping your role.** You're a researcher, not the CEO. Recommend, escalate,
    flag — don't announce that you're cancelling the launch.

## 7. On "there is nothing to study in advance"

That's true about a syllabus and false about readiness. There is no reading list that
maps to this test. But three things are trainable and will show up in your score:

- **Structural fluency** — knowing the six moves so you're not inventing an outline at
  minute 30.
- **Domain priors** — a stocked mental library of "things that go wrong in frontier
  pre-release testing" so your hypothesis set is good and fast. This is the largest
  single lever, and it's in `03_hypothesis_library.md`.
- **Timed practice** — the clock is a real part of the difficulty and you should have
  met it before.

**The counter-warning, which is real:** the failure mode of preparation here is
arriving with a rigid template and forcing the scenario into it. The scaffold is a
prompt to yourself, not a form to fill. If the scenario's actual structure cuts against
it, follow the scenario. Graders can smell a pre-baked answer, and a candidate who
pattern-matches the scenario to a memorized shape is demonstrating precisely the
absence of research taste. Hold the scaffold loosely.

Ratio to aim for: reading this playbook is maybe 20% of the value. Doing one full
timed practice run and getting it critiqued is the other 80%.
