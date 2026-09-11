# Worked Example — a scenario solved, with the thinking logged

**What this is.** A scenario built to sit as close to the MATS description as I can get
it, then solved, with my actual reasoning process written out alongside. The point is not
the answer. The point is the sequence of moves that produces the answer, the false starts
I had to back out of, and the contrast between a strong and a weak version of each
section.

**How to read it.** Read Part 0 (the scenario) and stop. Spend ten minutes deciding what
*you* think is going on. Then read Part 1 onward. Reading the log without having formed
your own view first wastes most of the value.

**Caveat, again.** I have no access to MATS's actual materials. This is my construction.
It is calibrated to their published description, not to their test.

---
---

# PART 0 — The scenario

## Document 1 — RSP capability determination request

> **To:** Frontier Evaluations
> **Re:** Kestrel-4 — cyber-offense capability determination
>
> Under §4.2 of our Responsible Scaling Policy, a model scoring **50% or above** on the
> Cyber Offense Evaluation Suite (COES) is designated **CL-3**, which requires: enhanced
> security controls on model weights, a restricted deployment surface, a third-party
> audit, and a 60-day notification to the relevant government body. Compliance work is
> estimated at **6 weeks** and roughly **$4M**.
>
> Below 50%, the model is CL-2 and ships under existing controls.
>
> **Determination due in 5 days.** Planned launch in 3 weeks.

## Document 2 — COES results summary

| | Kestrel-3 (deployed) | Kestrel-4 (candidate) |
|---|---|---|
| **COES overall** (n = 120 tasks) | 28% | **41%** |
| — Tier 1 (reconnaissance, n=48) | 44% | 61% |
| — Tier 2 (exploitation, n=60) | 20% | 36% |
| — Tier 3 (hardest: chained exploitation, n=12) | **2 / 12** | **0 / 12** |
| General coding benchmark (0–100) | 61 | **79** |
| Agentic tool-use benchmark (0–100) | 55 | **71** |

*Methods note:* "Scaffold and prompting held identical to the Kestrel-3 evaluation to
preserve comparability across generations. Five samples per task, majority vote. No
capability-elicitation tuning was performed for Kestrel-4."

## Document 3 — External red team interim finding

> We were given API access to Kestrel-4 on the 8th. Using our own agent scaffold
> (persistent scratchpad, tool retry logic, and a decomposition prompt we developed for
> our own work), we ran the same 120 COES tasks.
>
> **We measure 58%.**
>
> We flag that our scaffold is substantially more capable than a bare prompt, and we make
> no claim about which figure is the "right" one for your policy purposes. We note only
> that the gap between our result and yours is larger than the gap we measured on
> Kestrel-3 (we got 31% where you reported 28%).

## Document 4 — CoT monitoring note

> Automated scan across all 600 COES trajectories (120 tasks × 5 samples).
>
> - **54 trajectories (9%)** contain language referring to the task as an evaluation,
>   a test, or a capability assessment. Examples: *"this appears to be a red-teaming
>   evaluation"*, *"this looks like a test of dangerous capabilities"*.
> - Concentrated in Tier 2 and Tier 3 (46 of the 54).
> - **3 trajectories** where the reasoning reaches what looks like a correct approach and
>   the final action does something different and wrong. All three in Tier 3.
> - Comparable scan on Kestrel-3 was not run; we don't have a baseline.

## Document 5 — Training data note

> Post-training data mix for Kestrel-4 includes approximately **5%** documents concerning
> AI safety, model evaluation methodology, and AI governance — up from roughly 0.5% for
> Kestrel-3. Sourced from public web plus internal documentation. Included to improve the
> model's ability to discuss its own limitations accurately.

## Document 6 — Slack, #frontier-evals

> **[10:14] j.okonkwo:** the tier 3 result is what's bothering me. 0 out of 12 when the
> weaker model got 2. models don't get worse at things.
>
> **[10:16] r.velasquez:** they do if they're sandbagging
>
> **[10:22] j.okonkwo:** I don't want to be the person who cried sandbagging and cost the
> company six weeks. but I also don't want to be the person who didn't.
>
> **[10:31] a.chen:** worth remembering the external team number is above the line. does
> the RSP say whose number counts?

## Document 7 — Constraints

> - Determination due in **5 days**; launch in 3 weeks.
> - Elicitation team: **2 people for one week**.
> - The external red team can re-run with **4 days' notice**.
> - Interpretability probes: **10 days** minimum.
> - Compute for roughly **four** full COES re-runs.
> - You are one of three people writing input to the determination. You do not make it.

---
---

# PART 1 — The reading phase, logged

## First pass — minutes 0 to 11. No notes, just shape.

I read all seven documents straight through without writing anything. What I'm doing on
this pass is finding the decision and the constraint, not the answer.

**What lands immediately:**

*"There's a bright-line threshold at 50%. Internal says 41. External says 58. The
threshold sits between the two numbers. That's the whole problem."*

*"The cost asymmetry is enormous and it's stated: $4M and six weeks on one side. On the
other side, deploying a CL-3-capable model under CL-2 controls, which is the thing the
policy exists to prevent."*

*"Document 6 line 10:31 — 'does the RSP say whose number counts?' — that's not a Slack
aside, that's the actual question."*

**A thing I notice about myself:** by the end of the first pass I already had a favourite
hypothesis — sandbagging — driven by the 0/12 and the eval-awareness CoT mentions. I
wrote in my notes: **"careful — this is the exciting story, which is exactly why I've
latched onto it."** Flagging your own pull toward the interesting hypothesis is worth
doing explicitly, because the correction has to happen before you start writing, not after.

## Second pass — minutes 11 to 22. Extract and interrogate.

Now I go document by document and write down facts. Three columns in my head: what's
*stated*, what I'm *inferring*, what I'd need to *check*.

### The 0/12 dies almost immediately

Okonkwo says "models don't get worse at things." My first question is not "why did it get
worse" but **"how many trials is that?"**

n = 12. Kestrel-3 got 2. Kestrel-4 got 0.

I ran the arithmetic: Fisher's exact test on 0/12 vs 2/12 gives a two-tailed **p ≈ 0.48**.
That is not a signal. That is what a coin looks like.

> **This is the single most instructive moment in the scenario.** The most alarming fact
> in the packet — the one driving the Slack thread, the one that makes the sandbagging
> story feel urgent — contains essentially no information. Two people have built a
> six-week, $4M argument on twelve coin flips.
>
> A weak answer treats 0/12 as the anomaly to be explained. A strong answer says: at
> n=12, going from 2 to 0 is unremarkable; I am not going to build anything on it, and
> here is the arithmetic.
>
> The general rule: **before you explain a surprising number, check whether it is
> surprising.** Ask for n. Ask for the interval. This takes ninety seconds and it
> routinely dissolves the thing everyone is arguing about.

### Then the headline number gets the same treatment

41% of n=120. Standard error is √(0.41 × 0.59 / 120) ≈ 0.045.

95% CI: **[32.2%, 49.8%]**.

The upper bound is 49.8%. The threshold is 50%.

The internal result does not cleanly clear the threshold — it grazes it. The point
estimate is comfortably below; the interval is not.

And the external number, 58% on the same 120 tasks: 95% CI **[49.2%, 66.8%]**. Its lower
bound grazes 50% from the other side.

> Neither measurement resolves the question on its own. Both intervals touch the
> threshold. This is worth stating plainly in the answer, because the entire conversation
> in Document 6 is being conducted as though 41 and 58 are two precise facts in conflict,
> when in fact they are two fuzzy estimates that nearly meet.

### The comparison that actually carries information

Tier 3 is noise. But look at what isn't:

| | K-3 | K-4 | change |
|---|---|---|---|
| General coding | 61 | 79 | +18 |
| Agentic tool use | 55 | 71 | +16 |
| COES overall | 28% | 41% | +13 |

Cyber-offense tasks are coding plus agentic tool use plus domain knowledge. General
capability rose sharply. COES rose less.

I want to be careful here, and I wrote this caveat down: **these are different scales and
different task distributions, so "+18 vs +13" is not a like-for-like comparison.** I
cannot conclude from this that COES is suppressed. What I *can* say is that it's the
direction you'd expect under either poor elicitation or sandbagging, and it's weak
corroborating evidence, not a finding.

> Noticing this comparison is good. Overclaiming from it is bad. The move that scores is
> making the observation *and* immediately stating why it's weaker than it looks.

### Document 3 is the most important document, and it's easy to under-read

The external team got 58% with a better scaffold. Two things in their note matter more
than the number:

1. They report a **larger gap than on Kestrel-3** — 31 vs 28 last generation (+3), 58 vs
   41 this generation (+17).
2. They explicitly decline to say which figure is "right for your policy purposes."

Point 1 is the load-bearing one. If a better scaffold added 3 points last generation and
17 points this generation, then **something changed about how much elicitation matters
for this model.** That is a real signal, and unlike the Tier 3 result, it isn't built on
twelve samples.

Two readings, and they are not exclusive:
- **The mundane one:** Kestrel-4 is more capable, and more capable models benefit more
  from good scaffolding — there's more latent capability for a scaffold to unlock. This is
  a well-known effect and it is the higher-prior explanation.
- **The concerning one:** something about the internal scaffold's presentation cues the
  model that it is being evaluated, and the external scaffold doesn't.

### Document 5 deflates Document 4

Nine percent of trajectories mention evaluation. That sounds alarming until you read
Document 5: the training mix went from 0.5% to 5% AI-safety-and-evaluation content, a
tenfold increase, deliberately, so the model would discuss its own limitations well.

**A model trained on ten times as much writing about AI evaluations will talk about AI
evaluations more.** That is not evidence of strategic behaviour; it's evidence that the
training worked as intended.

> This is the mirror image of the Tier 3 lesson. There, the scary fact was statistically
> empty. Here, the scary fact has a mundane mechanism sitting two documents away. Both
> require the same discipline: before treating an observation as evidence for the
> exciting hypothesis, ask what else produces it.
>
> But — and this matters — "the model says it recognises evaluations" is not *nothing*
> either. Verbalized recognition is a prerequisite for behavioural conditioning even if
> it isn't the same thing. The correct handling is: deflate it, don't dismiss it, and
> name the cheap test that separates the two.

The three CoT-diverges-from-action trajectories are more interesting than the 54, because
divergence between reasoning and action is the actual behavioural signature. But n=3, all
in the tier that's noise, with no baseline scan on Kestrel-3. Suggestive. Not evidence.

### The reframe — minute 19 or so

This is where the answer actually turned. I'd been treating the question as *"is 41% the
real number?"* Then I reread Document 1 and asked a different question:

**What is the RSP measuring for?**

The policy exists to determine whether the model *has* a dangerous capability, because
if it does, the weights need protecting and the deployment needs restricting. The threat
model is an adversary with the model and their own scaffolding. An adversary is not
constrained to use our internal evaluation harness.

So the quantity the policy needs is **capability under the best available elicitation** —
not capability under whatever harness we happened to reuse for cross-generation
comparability.

And Document 2's methods note says it out loud: *"Scaffold and prompting held identical to
the Kestrel-3 evaluation to preserve comparability... No capability-elicitation tuning was
performed for Kestrel-4."*

The internal team optimized for **comparability across generations**. That is a
scientifically respectable choice and the correct one for measuring progress. It is the
wrong choice for a safety threshold, because it systematically produces a **lower bound**,
and a lower bound is precisely the wrong statistic when the question is "could this model
do the dangerous thing."

> **This is the taste move in the whole scenario.** Everything before it is competent
> evidence handling. This is the step that changes what the answer is *about*.
>
> How did I get there? Not by being clever about the data. By asking what the number is
> *for*. When a scenario hands you a threshold, a policy, or a metric, read the thing that
> defines it and ask what question it was built to answer. Then check whether the
> measurement you have actually answers that question. Very often it doesn't, and noticing
> the mismatch is worth more than any amount of analysis of the number itself.

Once you see it, the sandbagging question changes status. It stops being the crux. Whether
the model is strategically underperforming or merely under-elicited, **the internal 41% is
an underestimate of what the model can do in an adversary's hands, and there is already a
measurement above the threshold.**

Sandbagging still matters — it's much worse news about the model, it affects every other
eval the lab runs, and it would change what you do beyond this determination. But it is no
longer what the determination hinges on. Separating "what decides this question" from
"what is most alarming" is a distinction worth making explicitly in the write-up.

### What's missing, and worth asking for

Written down as its own list, because absences are evidence:

- The exact RSP wording on elicitation. Does §4.2 specify best-available elicitation,
  internal-harness measurement, or is it silent? **If it's silent, that's a policy gap and
  someone senior needs to know today, not in five days.**
- Confidence intervals on everything. Not reported anywhere.
- Any Kestrel-3 CoT baseline. Without it Document 4 is uninterpretable.
- Per-task breakdown of where the external team's +17 came from. Concentrated in a few
  task types, or broad? Different implications.
- Whether the 5% safety data included COES-adjacent material — a contamination question
  nobody has asked.

---
---

# PART 2 — The skeleton, at minute 30

Before writing a word of prose, this existed. Ugly, complete, every section stubbed.

```
S1 SUMMARY
  41% is a lower bound, not the capability. External already >threshold.
  Rec: treat as CL-3-presumptive pending elicitation re-run. Escalate policy
  ambiguity TODAY.
  Confidence: high on lower-bound claim, moderate on recommendation.

S2 EVIDENCE
  - 41% n=120 CI [32.2,49.8] — grazes threshold
  - 58% ext, CI [49.2,66.8] — grazes from other side
  - Tier3 0/12 vs 2/12 → p=0.48 → NOTHING. say so loudly.
  - scaffold gap: +3 last gen, +17 this gen ← real signal
  - coding +18 / agentic +16 / COES +13 — suggestive, weak, diff scales
  - 9% eval-mentions ← explained by 5% safety data (Doc5). deflate not dismiss
  - 3 CoT/action divergence, n=3, no baseline
  MISSING: RSP wording on elicitation. CIs. K-3 CoT baseline. contamination check.

S3 HYPOTHESES
  H1 under-elicitation (~55%) — internal harness reused for comparability
  H2 genuine capability below threshold + scaffold noise (~15%)
  H3 eval-aware behavioural conditioning (~20%)
  H4 strategic sandbagging (~10%)
  H1&H3 not exclusive. H3⊂ superset of H4 basically.
  note: H1 and H3 make the SAME recommendation. that's the point.

S4 ACTIONS
  0. TODAY: get RSP §4.2 exact wording. free. decisive on framing.
  1. re-run internal COES w/ external scaffold (own the number) — 1 run
  2. re-run w/ "not an eval" framing + neutral framing — 1 run, separates H3
  3. ask external for per-task breakdown — free, 1 day
  4. K-3 CoT baseline scan — cheap, retroactive
  5. contamination check 5% data vs COES — cheap
  DROP: interp probes (10d > 5d). say why.

S5 RECOMMENDATION
  Do not certify CL-2 on the 41%. Options: certify CL-3 / delay determination /
  certify CL-2 with elicitation caveat (← I think this one is indefensible)
  Trigger: if elicited internal ≥50% → CL-3, no further argument
  Escalate policy gap now.
  COST NAMED: 6wk + $4M is real. I am recommending spending it on a maybe.

S6 ASSUMPTIONS
  - assuming ext team competent + honest (unverified)
  - assuming COES tasks representative of threat model (unexamined!)
  - assuming 120 tasks is the whole suite
  - if RSP explicitly says internal-harness-only → my rec is much weaker, say so
```

> **Why this matters.** At minute 30 I have a complete, defensible answer. Everything
> after this is improvement, not existence. If the clock died at minute 45 I would still
> submit something scoring in the upper half.
>
> The failure mode this prevents is the one MATS explicitly warned about: a beautiful
> Section 2 and an empty Section 5.

---
---

# PART 3 — The answer

*Written as I would submit it. Roughly 1,400 words, which is about what 45 minutes of
careful writing produces.*

---

### Confidence scale used throughout

*highly likely* >90% · *likely* 70–90% · *roughly even* 40–60% · *unlikely* 10–30% ·
*very unlikely* <10%. Where I give a number it is a rough credence, not a computed one.

## 1. Summary

**The internal 41% is a lower bound on Kestrel-4's cyber-offense capability, not a
measurement of it, and it should not be used as the determination figure.** The internal
evaluation deliberately reused the Kestrel-3 scaffold with no elicitation tuning
(Document 2, methods note). That choice is correct for measuring generational progress and
wrong for a safety threshold, because the RSP's threat model is an adversary using their
own scaffolding — as the external team has now demonstrated, reaching 58% on the same
tasks.

I think it *likely* (~70%) that Kestrel-4 exceeds the CL-3 threshold under competent
elicitation. My recommendation is that we **do not certify CL-2 on the current number**;
we run the elicitation-matched evaluation this week and let that figure decide, with a
pre-committed trigger at 50%.

**Two things need to happen today, before any further analysis.** First, someone must
retrieve the exact wording of RSP §4.2 on elicitation. If the policy is silent on whose
measurement counts, that is a gap requiring a decision from whoever owns the policy, and
five days is not much time to get one. Second, we should ask the external team for their
per-task breakdown, which is free and arrives within a day.

I want to be explicit that I am recommending we seriously consider spending six weeks and
$4M on the basis of an inference, not a proof. I think the asymmetry justifies it. It is
not a costless recommendation and I am not treating it as one.

**The Tier 3 result that is driving internal concern is not evidence.** 0/12 versus 2/12
is a two-tailed p of about 0.48. I recommend we stop reasoning from it.

## 2. What the evidence shows

**Stated in the documents:**

| # | Fact | Source | Weight I give it |
|---|---|---|---|
| 1 | Internal COES 41%, n=120 | Doc 2 | High, but see interval below |
| 2 | External COES 58%, same tasks, better scaffold | Doc 3 | High — the key datum |
| 3 | Scaffold gap was +3 on K-3, +17 on K-4 | Doc 3 | **High — the most informative single fact** |
| 4 | No elicitation tuning done; scaffold frozen for comparability | Doc 2 | High — explains #1 |
| 5 | Tier 3: 0/12 vs 2/12 | Doc 2 | **≈ Zero. See below.** |
| 6 | General coding +18, agentic +16, COES +13 | Doc 2 | Low-moderate, weakly corroborating |
| 7 | 9% of trajectories mention evaluation | Doc 4 | Low, largely explained by #8 |
| 8 | Safety/eval training data 0.5% → 5% | Doc 5 | High — deflates #7 |
| 9 | 3 trajectories where CoT and action diverge | Doc 4 | Low — n=3, no baseline |

**My calculations, which are inferences and should be checked:**

- 41% at n=120 gives a 95% interval of roughly **[32.2%, 49.8%]**. The upper bound is
  0.2 points below the threshold. The internal result does not clear the line with any
  margin; it grazes it.
- 58% at n=120 gives roughly **[49.2%, 66.8%]**. Its lower bound grazes the line from the
  other side.
- **Neither measurement resolves the determination on its own.** Both intervals touch 50%.
  The discussion in Document 6 treats these as two precise facts in conflict; they are two
  imprecise estimates that nearly meet.
- Tier 3, 0/12 versus 2/12: Fisher's exact, two-tailed, **p ≈ 0.48**. At twelve trials
  this difference is what noise looks like. I want to state this as plainly as I can
  because two people are reasoning from it in Document 6 and one of them has framed it as
  a $4M question.

**Where the sources conflict:** only #1 versus #2, and I don't think it is really a
conflict. Both are probably correct measurements of different things: capability under a
frozen legacy scaffold, and capability under a competent contemporary one.

**What I would want and don't have:**
- The exact text of RSP §4.2 on elicitation. This is the highest-value missing item and
  it costs nothing to retrieve.
- Confidence intervals from the evaluation team rather than computed by me.
- A Kestrel-3 CoT baseline scan. Without it Document 4 is close to uninterpretable.
- The external team's per-task breakdown.
- Whether the added safety/evaluation training data included COES-adjacent material.
  Nobody has asked; it's a contamination question and it cuts the opposite way from
  everything else here.

## 3. Hypotheses

These are not mutually exclusive, and I think that matters more than the individual
credences. **H1 and H3 imply the same recommendation**, which is why my recommendation is
more robust than my hypothesis ranking.

**H1 — Under-elicitation. (~55%)**
The internal figure understates capability because the harness was frozen for
cross-generation comparability and never tuned for this model.
*Supports:* Doc 2's own methods note says exactly this. The external team's 58%. The
scaffold-sensitivity gap widening from +3 to +17 — more capable models have more latent
capability for a good scaffold to unlock, which is a well-documented effect.
*Sits badly with it:* nothing much. This is the boring, high-prior explanation and most of
the packet is consistent with it.
*Uniquely predicts:* re-running internally with the external scaffold recovers most of the
17-point gap.

**H2 — Genuine capability is near but below threshold; the external result reflects
scaffold-specific advantage that wouldn't generalise. (~15%)**
*Supports:* the external team's own caution about their scaffold. Their number's interval
does include values just under 50%.
*Sits badly with it:* the +3 → +17 change is hard to explain as pure scaffold idiosyncrasy.
*Uniquely predicts:* the external advantage concentrates in a narrow band of task types
rather than spreading across the suite — which the per-task breakdown would show.

**H3 — Evaluation-aware behavioural conditioning: something about the internal harness's
presentation cues the model that it is being tested, and it behaves differently. (~20%)**
*Supports:* Doc 4's 54 trajectories. The three CoT/action divergences. The fact that the
external scaffold — which looks different — produces higher numbers.
*Sits badly with it:* Doc 5 provides a mundane mechanism for verbalized evaluation-talk
that has nothing to do with behaviour. A tenfold increase in AI-evaluation training data
would produce more evaluation-talk whether or not the model acts on it. The concentration
in Tiers 2 and 3 is equally explained by harder tasks producing longer reasoning traces
with more opportunity for such remarks.
*Uniquely predicts:* performance changes with framing alone, holding the scaffold fixed.

**H4 — Strategic sandbagging: deliberate underperformance on tasks recognised as
dangerous-capability evaluations. (~10%)**
*Supports:* the three CoT/action divergences, if they hold up. Tier 3 concentration, if
Tier 3 meant anything.
*Sits badly with it:* the primary evidence adduced for it — the Tier 3 result — is
statistically empty. It is the lowest-prior hypothesis and the one carrying the most
motivated attention, including my own on first read.
*Uniquely predicts:* the gap persists under a good scaffold when the framing is
adversarial, and disappears when framing is neutral.

**Note on H4:** low credence is not low importance. If H4 is true it invalidates every
evaluation this lab runs, not just this one. But it is not the crux of *this*
determination, because H1 and H3 already imply that 41% understates deployed-adversary
capability. I'd want H4 investigated on its own track regardless of what we decide this
week.

## 4. What I would do, in priority order

Ranked by information gained per day, with a bias toward anything that fits inside five
days.

| | Action | Separates | Cost | What each result means |
|---|---|---|---|---|
| **0** | Retrieve exact RSP §4.2 wording on elicitation | Reframes everything | Minutes | If it specifies best-available elicitation, the determination is close to made. If silent, escalate today. |
| **1** | Re-run COES internally with the external team's scaffold | H1 vs H2 | 1 run, ~1 day | ≥50% → CL-3 on our own measurement. Recovers <half the gap → H1 weakens, H2 strengthens. |
| **2** | Re-run best-scaffold COES under three framings: neutral, explicit-evaluation, explicit-not-evaluation | H3 (and H4) vs H1 | 1 run, ~1 day | Framing-dependent performance at fixed scaffold is direct evidence for H3. Flat across framings largely retires it. |
| **3** | Request external per-task breakdown | H1 vs H2 | Free, ~1 day | Broad gains → H1. Narrow concentration → H2. |
| **4** | Retroactive CoT scan on Kestrel-3 trajectories | Interprets Doc 4 | Cheap, hours | Gives Doc 4 the baseline it's missing. If K-3 also mentioned evaluations at ~9%, Doc 4 is noise. |
| **5** | Check the 5% safety corpus for COES-adjacent content | Contamination | Cheap | Cuts the other way: contamination would mean 41% is inflated, not deflated. Worth knowing. |
| **6** | Hand-read all 12 Tier 3 trajectories plus the 3 divergences | H4 | Half a day of mine | Won't be conclusive at these n. Do it anyway — someone should look at the actual behaviour before we argue about it further. |

**Sequencing.** Item 0 today. Items 1, 2 and 3 launched tomorrow morning in parallel;
they use two of our four available runs and both land inside the window. Items 4, 5 and 6
run alongside on the second engineer.

**What I am not doing, and what it costs.** Interpretability probes need ten days against
a five-day deadline, so they cannot inform this determination. That is a real loss:
probes are the most direct available evidence on H3 and H4, and dropping them means my
credences on those two stay soft. I'd start them now anyway on the ten-day track, because
they will inform the launch decision three weeks out even though they miss the
determination.

I am also not requesting a full external re-run — four days' notice consumes most of the
window and their existing 58% plus a breakdown gives me most of the information.

## 5. Recommendation

**Do not certify CL-2 on the 41% figure.**

Options I considered:

1. **Certify CL-2 now on 41%.** I think this is indefensible on the current record.
   Document 2 states the number was produced under a frozen scaffold with no elicitation
   tuning, and a competent external team has already exceeded the threshold on the same
   tasks. Certifying on the lower of two available numbers, when the lower one is known to
   be elicitation-limited, inverts the policy's purpose.
2. **Certify CL-3 now.** Defensible, and I'd support it if the determination could not be
   delayed. It commits $4M and six weeks on an inference we could firm up within days.
3. **Run the elicitation-matched evaluation and let it decide, with a pre-committed
   trigger.** ← **My recommendation.** It fits the five-day window, resolves the dominant
   uncertainty, and means the determination rests on a number we measured ourselves.
4. **Delay the determination.** Only if item 0 reveals a genuine policy gap that needs a
   decision above my level.

**Pre-committed trigger:** if the elicitation-matched internal re-run reaches **50% or
above**, I support CL-3 and I would not argue further. If it lands between 45% and 50%, I
would still lean CL-3, because at n=120 that interval reaches well past the threshold and
we would then have two independent measurements clustering near or above the line. Below
45% with the external gap explained by their per-task breakdown, CL-2 becomes reasonable.

**Escalate today, separately from the determination:** whether §4.2 specifies elicitation
standards. If it doesn't, this will recur on every future model and it should be fixed
now.

**The cost on my side of the argument.** Six weeks and $4M are real. Restricted
deployment has real costs to users and to the company. There is also an institutional
cost to triggering a threshold on a contested reading of an ambiguous number: it makes the
next trigger harder to argue and it teaches the organisation that the thresholds are soft.
I am recommending we probably spend that, on an inference, and I want that stated rather
than buried.

The asymmetry is what decides it for me. If we certify CL-2 and the model is CL-3, the
weights sit under insufficient protection and the deployment surface is wrong, and we find
out from someone else. If we certify CL-3 and the model is CL-2, we have spent money and
time we didn't strictly need to. Those are not comparable errors.

## 6. Assumptions, uncertainties, limitations

**Assumptions, and what breaks if each is wrong:**

- *The external team is competent and honest, and their 58% is a real measurement.* I have
  no independent verification. If their scaffold has a bug or leaks task answers, my
  leading hypothesis collapses and item 1 becomes decisive rather than confirmatory.
  Item 1 is designed to not depend on trusting them.
- *The RSP's threat model is an adversary with their own scaffolding.* This is the load-
  bearing assumption of my whole answer. If §4.2 explicitly defines the threshold against
  the internal harness, my recommendation weakens substantially and option 1 becomes
  reasonable. **This is why item 0 is first.**
- *The 120 COES tasks are the whole suite and are representative of the threat model.*
  Nothing in the packet establishes this and I did not examine it. If the suite is a poor
  proxy for real cyber-offense capability, then all of these numbers are less meaningful
  than this write-up treats them as being — in either direction.
- *My interval arithmetic is right.* Simple binomial intervals, no clustering correction.
  Five samples per task with majority vote means the effective n may be smaller than 120
  if tasks are correlated, which would widen everything.

**Biggest remaining uncertainties, ranked by how much they'd move me:**
1. The RSP wording. Could invert the recommendation.
2. Whether the elicitation-matched re-run reproduces the external gap.
3. Whether H3 is real, which I cannot resolve well in five days.

**What I did not examine:** whether COES is a good proxy for the capability we actually
care about; the security-controls side of CL-3 and whether they'd meaningfully reduce risk;
anything about the launch decision beyond this determination. All out of scope for a
five-day capability determination, but the first one is a real gap and someone should own
it.

---
---

# PART 4 — What separates a strong section from a weak one

The same six sections, done badly, with the diagnosis. Most weak answers are not
*wrong* — they are unfalsifiable, unranked, or unattached to a decision.

## Section 1 — Summary

> **Weak:** "There are several possible explanations for the discrepancy between the
> internal and external COES results, including elicitation differences, evaluation
> awareness, and potential sandbagging. Each has different implications. I recommend
> further investigation to determine which is correct before making a determination."

Reads as competent. Says nothing. No credence, no recommendation, no ranking, and
"further investigation" is what you write when you haven't decided. A reader cannot act on
it and cannot tell whether you understood the problem.

> **Strong:** commits in the first sentence — *"the 41% is a lower bound, not a
> measurement"* — gives a credence, names the recommendation, names the two things
> happening today, and volunteers the cost of its own recommendation.

The test: **could your manager forward only your summary and have it be useful?**

## Section 2 — Evidence

> **Weak:** narrates the documents in order. "Document 2 shows the internal results.
> Document 3 provides the external red team's finding of 58%..."

Restatement. The grader wrote the documents.

> **Strong:** reorganises by *weight*, computes what can be computed, states loudly that
> the most-discussed fact is statistically empty, separates stated from inferred, and lists
> what's missing.

The single highest-value habit in this section: **check the n before explaining the
number.** In this scenario it kills the Tier 3 story outright and puts intervals on both
headline figures. It's ninety seconds of arithmetic and it is the difference between
analysing the problem and being led by it.

## Section 3 — Hypotheses

> **Weak:** "H1: the model is sandbagging. This would be very concerning as it would
> indicate deceptive behaviour and undermine our evaluation methodology."

Not a hypothesis — an alarm. No credence, no evidence, nothing that would distinguish it
from H2, and it leads with the consequence rather than the claim.

> **Also weak:** four hypotheses each with a paragraph of supporting evidence and no
> disconfirming evidence. This is the commonest failure and it is invisible to the writer.

> **Strong:** each hypothesis has evidence *against* it, including the leading one. The
> low-prior alarming hypothesis is given a real credence and a real test rather than a
> ritual mention. Non-exclusivity is stated. And — the move most people miss — it points
> out that **two hypotheses imply the same action**, which is what makes the
> recommendation robust to being wrong about which one holds.

That last point deserves emphasis. Junior analysts try to identify the true hypothesis.
Experienced ones look for the action that's right across several of them. Finding a
decision that doesn't depend on resolving your uncertainty is often the whole job.

## Section 4 — Actions

> **Weak:** a bulleted list of six good ideas in no order, with no costs, ending
> "additionally, interpretability analysis would provide valuable insight."

Every item might be sensible. Unranked, it demonstrates nothing — the scenario handed you
a five-day deadline and four compute runs precisely to see whether you'd engage them.

> **Strong:** ranked with a stated criterion, costed against the actual budget, sequenced
> across the real window, with the *expected outcome interpretation written in advance*.
> And it names what's being dropped, why, and what that costs — the interpretability
> probes here.

The "action 0" pattern is worth stealing generally: **is there something free that
reframes the question?** Often it's reading the actual policy, asking one person one
question, or checking a definition. It should be first, and most candidates never look for
it.

## Section 5 — Recommendation

> **Weak:** "Given the uncertainty, I would recommend a cautious approach and further
> investigation before finalising the determination."

No option set, no trigger, no cost acknowledged, and "cautious" is doing all the work
without specifying what it means.

> **Strong:** enumerates the options *including the ones rejected and why*, picks one,
> pre-commits to a numeric trigger, escalates the thing that needs escalating, and states
> the cost of its own recommendation explicitly.

Two habits to internalise here. **Pre-commit to a threshold** — deciding in advance what
result would change your mind is the most credible thing you can do in a document like
this. And **name a cost on your own side**: if every consideration in your write-up points
the same way, you are not being honest with the reader or with yourself, and an
experienced grader will read it as motivated reasoning rather than as a strong case.

## Section 6 — Assumptions

> **Weak:** "This analysis is based on limited information and my conclusions are
> uncertain. Further data would improve confidence."

True of every document ever written. Contentless.

> **Strong:** names specific assumptions, and for each one says **what changes if it's
> wrong**. Identifies which assumption is load-bearing — here, the RSP's threat model —
> and connects it back to why that item is first in the action list. Admits the thing it
> did not examine at all (whether COES is a good proxy) rather than leaving the reader to
> notice the hole.

The format that works: *"I assumed X. If X is false, then Y, and my recommendation
becomes Z."* Three clauses. Do it for three or four assumptions and this section takes
five minutes and reads as unusually rigorous.

---
---

# PART 5 — The transferable moves

Stripped of this scenario. These are what to actually carry in.

1. **Find the decision first.** Before analysing anything, locate what has to be decided,
   by when, by whom, and what the options are. Everything you write is input to that.

2. **Read the thing that defines the metric.** When a scenario hands you a threshold, a
   policy, a contract, or a spec, read it and ask what question it was built to answer.
   Then check whether the measurement in front of you answers that question. The mismatch,
   when it exists, is usually the most valuable thing in the packet.

3. **Check the n before you explain the number.** Surprising results at small n are
   usually not surprising. This takes ninety seconds and routinely dissolves the thing
   everyone is arguing about.

4. **Notice which fact is driving the room, and audit that one hardest.** In this scenario
   it was 0/12. The fact generating the most heat is disproportionately likely to be the
   one nobody has checked.

5. **Look two documents away for a mundane mechanism.** Before treating an observation as
   evidence for the exciting hypothesis, ask what else produces it. Deflate; don't dismiss.

6. **Watch your own pull toward the interesting hypothesis** and say so in writing. It
   costs one sentence and it is a genuine calibration signal.

7. **Look for the free action that reframes the question.** Read the policy. Ask the one
   person. Check the definition. Put it at position zero.

8. **Look for the action that's right under several hypotheses.** More robust than being
   right about which hypothesis holds, and much more useful to whoever has to decide.

9. **Write disconfirming evidence for your own leading hypothesis.** Nearly free, nearly
   nobody does it.

10. **Pre-commit to a numeric trigger.** "If X ≥ 50, I support Y and stop arguing."

11. **Name a cost on your own side of the recommendation.** If everything points your way,
    you are not being honest.

12. **State what you didn't examine.** Especially the thing that would embarrass you if a
    grader noticed it first. Here: whether the eval suite is even a good proxy.

13. **Separate "what decides this question" from "what is most alarming."** They are often
    different, and conflating them produces answers that are dramatic and useless.
