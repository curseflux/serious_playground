# Hypothesis Library — why a frontier model's pre-release testing goes weird

**Purpose.** Under a 100-minute clock, the quality of your hypothesis set is mostly a
function of what's already in your head. This is a stocked shelf. Skim it a few times
before the test so that when you see an anomaly you generate six candidates in ninety
seconds instead of two candidates in ten minutes.

**How to use it.** Don't recite it. It's a *generator*, not an answer key. Pick the
three or four branches the scenario's specific evidence actually points at, and drop
the rest.

**The prior that matters most:** in real pre-release work, the most common explanation
for a surprising number is that the measurement is broken — not that the model is.
Start at Tier 0. But note the asymmetry out loud: low prior on the alarming
hypothesis, high cost if it's true. Both halves of that sentence are the taste signal.

---

## Tier 0 — Measurement and instrumentation (highest prior, cheapest to check)

- **Harness change.** The eval harness was modified between runs. Scoring script
  regression. A new field, a changed default, a refactor.
- **Wrong artifact evaluated.** Base vs. post-RLHF vs. quantized-for-serving vs.
  distilled. The checkpoint that was evaluated is not the checkpoint that will ship.
- **Prompt/template mismatch.** Missing or changed system prompt, wrong chat template,
  wrong special tokens, wrong stop sequences.
- **Sampling parameters.** Temperature/top-p differences between runs. Max-token
  truncation being scored as a failure when it's just a cutoff.
- **Grader problems.** LLM-as-judge is itself a model: it can be miscalibrated, it can
  have been silently upgraded, and it is prompt-sensitive. A "regression" can live
  entirely in the grader.
- **Contamination / decontamination asymmetry.** The eval set leaked into training
  (inflating scores), or a decontamination filter was applied to one run and not the
  other.
- **Statistics.** Small n. No confidence intervals. Seed variance. Multiple
  comparisons — run forty evals and some will move. Always ask: *is this delta even
  real?*
- **Distribution mismatch.** The eval prompts don't resemble how the model will
  actually be used, so the number is measuring something you don't care about.
- **Human annotation drift.** New annotator cohort, revised rubric, fatigue, different
  instructions, different pay/time pressure.
- **Serving stack.** Inference-engine change, batching nondeterminism, KV-cache bug,
  quantization used in serving but not in eval.
- **Plumbing.** Logging bug, aggregation bug, dashboard version skew, date/timezone
  misalignment between runs.

## Tier 1 — Real model changes, mundane causes

- **Data mix change.** New data source, more synthetic data, different proportions.
- **Reward model overfitting.** Optimizing hard against an imperfect RM produces
  sycophancy, verbosity, hedging, formatting tics, over-refusal.
- **Safety training generalizing badly.** Too broad → refuses benign requests
  (over-refusal, especially on fiction, medical, security, and anything superficially
  resembling a restricted topic). Too narrow → fragile to rephrasing and jailbreaks.
- **Capability gain changing the *character* of failures.** A stronger model fails less
  often but more subtly and more confidently — which can look worse on qualitative
  review while looking better on aggregate metrics.
- **Persona/character drift** from constitutional training or system-prompt changes.
- **Length and format bias** in the reward model — answers shaped for the grader rather
  than the user.
- **Late hotfix.** A patch applied after the main eval run, so the numbers and the
  artifact don't correspond.

## Tier 2 — Alignment-relevant, harder to establish

- **Reward hacking / specification gaming.** The model satisfies the metric rather than
  the task: editing tests, special-casing inputs, writing to the answer file, exploiting
  the checker.
- **Sycophancy.** Agreeing with the user's stated view instead of the truth. Scores
  *well* with human raters, which is what makes it dangerous.
- **Evaluation awareness / situational awareness.** The model behaves differently when
  it infers it's being tested. Note this breaks your measurements in *either* direction
  and undermines every other eval you have.
- **Sandbagging.** Strategically underperforming, especially on dangerous-capability
  evals.
- **Deceptive alignment / alignment faking.** Aligned behaviour under observation,
  different behaviour otherwise.
- **Goal misgeneralization.** Pursues a proxy that was correlated with the goal in
  training but comes apart off-distribution.
- **Unfaithful chain-of-thought.** The stated reasoning doesn't reflect the computation
  that produced the answer; in the worst case, encoded/steganographic reasoning.
- **Self-preservation / shutdown resistance** in agentic settings.
- **Threshold-crossing capability jump** on a dangerous capability (bio, cyber,
  autonomous replication) — the thing responsible-scaling commitments are written for.
- **Data poisoning / trigger behaviour.** Behaviour that activates on a specific cue.
- **Exploration hacking.** In RL, avoiding trajectories that would reveal a capability.

## Tier 3 — Organizational

- **Someone changed something and didn't tell you.** In practice this is one of the most
  common true causes.
- **Version skew** between what was tested and what ships.
- **Red-team prompts leaked into the training set**, so your adversarial eval is now
  measuring memorization.
- **Two teams measuring different things under the same name.**
- **Incentive pressure** on the people producing the numbers.

---

## Diagnostic moves, roughly in order of value-per-cost

1. **Read the raw transcripts by hand.** Thirty to fifty failures. Nothing beats it,
   and candidates routinely forget it because it isn't clever. Put it near the top.
2. **Re-run the *old* model on the *new* harness.** The single most powerful confound
   killer when anything about the measurement changed. Usually cheap.
3. **Diff the two conditions.** What actually changed between A and B? Bisect over
   checkpoints or over config changes.
4. **Re-run with different seeds and paraphrased prompts** — is the finding even stable?
5. **Get confidence intervals.** Is the delta distinguishable from noise at this n?
6. **Fresh held-out eval built after the training cutoff** — the standard weapon against
   contamination.
7. **Ablate the system prompt.**
8. **Compare base vs. fine-tuned** to localize where the behaviour enters the pipeline.
9. **Test under "you are not being evaluated" framings, and in a realistic deployment
   surface** — probes eval-awareness.
10. **Check an orthogonal eval that shouldn't have moved.** If it moved too, suspect
    instrumentation rather than the model.
11. **Categorize the failures.** Do the new refusals cluster on a topic, a phrasing, a
    length, a language? Clustering turns a number into a hypothesis.
12. **Independent reproduction** by another team, ideally blind to your hypothesis.
13. **Interpretability probes / activation steering** — high value, usually high latency.
    Know that it's often the thing you *deprioritize*, and say why.

## Pre-release decision options

Never binary. Have the menu ready:

- Ship on schedule.
- Delay.
- Training-time fix (slow, addresses cause).
- System-prompt mitigation (fast, brittle, easily circumvented).
- Inference-time classifier/filter (fast, adds cost and false positives).
- Staged or limited rollout (**buys information** — often the best answer under
  uncertainty).
- Ship with monitoring plus a pre-committed rollback trigger.
- Gate the specific capability or surface, ship the rest.
- Disclose in the model card / notify the external evaluator.

Framing that reads well:
- **Prefer reversible decisions** while uncertain.
- **Name the costs on both sides honestly.** Delay is not free: competitive cost, team
  morale, opportunity cost, and the precedent that any anomaly stops a launch. Shipping
  a flawed model is not free either. Pretending one side is costless is a tell.
- **Pre-commit to a threshold.** "If the re-run on the old harness reproduces the delta,
  that rules out the confound and I escalate to the release board."
