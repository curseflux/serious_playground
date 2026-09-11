# Worked Example — sixty minutes on the lander, thinking logged

**What this is.** One control policy taken from nothing to a finished solution, with the
reasoning at each step and the measured score of every version. You can reproduce every
number in this file: `python3 sim.py lander --episodes 400 --policy <module>`.

**Why the lander.** It contains the trap that best predicts how you'll do on a real
assessment: **the obvious solution works, and the clever solution is much worse until you
fix two specific things.** If you switch to the clever version at minute 35 and don't
measure, you destroy a working answer.

---

## Minute 0–7 — Read the simulator, not just the prompt

Before writing anything I read `Lander.step()` in `sim.py`. Five things I wrote down:

```
state:      altitude (y), velocity (vy), fuel, frame
actions:    0 = off, 1 = low (0.08), 2 = high (0.16); gravity 0.05
SIGN:       vy is NEGATIVE when falling            <- easy to get wrong
success:    y <= 0 AND abs(vy) <= 0.8
score:      70 + 30*(fuel_left/200) on success, else 0
burn:       0 / 1 / 2 fuel per frame; start 200
```

> **The scoring line is the one that pays.** `70 + 30*(fuel/200)` means landing safely is
> only 70% of the available points. A policy can succeed on every single episode and still
> be leaving 30 points on the table. Most people never read this line and spend the hour
> optimising a number that was already maxed at minute 12.

Two things I computed immediately, because they bound everything:

- **Best available deceleration** = thrust(hi) − gravity = 0.16 − 0.05 = **0.11 per frame².**
- **Worst case:** from 120 units up, free-fall arrival speed is √(2 × 0.05 × 120) ≈ 3.5.
  Braking that to zero at 0.11 needs v²/(2a) ≈ **55 units** of altitude and ~32 frames of
  full burn ≈ **64 fuel**. Budget is 200. So the problem is comfortably solvable, and fuel
  is a scoring dimension rather than a feasibility constraint.

That second calculation is worth the ninety seconds. It tells me the task is not "can I
land" but "how cheaply," which changes what I build.

## Minute 7–12 — Something that runs

```python
def act_lander(obs, mem):
    return 0
```

| | success | score |
|---|---|---|
| **v0** — do nothing | 0.0% | 0.0 |

Pointless as a policy, valuable as an artifact: the harness works, the signature is right,
and I now have something submittable. First real attempt:

```python
def act_lander(obs, mem):
    return 2 if obs["velocity"] > 0.6 else 0      # thrust if falling fast
```

| | success | score |
|---|---|---|
| **v1** — reactive | **0.0%** | **0.0** |

Zero. Identical to doing nothing.

> **The sign bug.** `velocity` is *negative* while falling, so `velocity > 0.6` is never
> true and the engine never fires. I had written the sign convention in my notes seven
> minutes earlier and still got it wrong.
>
> What matters is how it *presented*: not a crash, not an error — a policy that ran
> cleanly 400 times and did nothing. **A silent no-op is the most common first bug in
> frame-based control, and the only thing that catches it is having a baseline to compare
> against.** v0 scoring 0.0 is why I knew instantly that v1 wasn't doing anything, rather
> than assuming it was just bad.

```python
    return 2 if -obs["velocity"] > 0.6 else 0
```

| | success | score | fuel used |
|---|---|---|---|
| **v2** — sign fixed | **100.0%** | **83.7** | 109 / 200 |

Lands every time, at minute 14. **This is the decision point the whole exercise is about.**

## Minute 14–20 — Deciding whether to stop

v2 succeeds on 400 of 400 episodes. The temptation is to tidy up and submit.

I didn't, for one reason: **the scoring function.** 83.7 out of a possible ~100 means the
fuel term is where the remaining points are, and v2 burns 109 of 200 — it is clamping
itself to terminal velocity for the entire descent, fighting gravity the whole way down
instead of arriving with the right speed.

> The reasoning I want you to copy: *"It works" and "it scores" are different questions,
> and I only know they're different because I read the scoring function at minute 3.*

What would spend less fuel? Freefall as long as possible, then one hard burn. The physics
is standard:

```
distance needed to go from speed s to target t at deceleration a  =  (s² − t²) / (2a)
```

Coast while altitude exceeds that; burn at full when it doesn't.

## Minute 20–28 — The clever version, and the crater

```python
def act_lander(obs, mem):
    y, vy, g = obs["altitude"], obs["velocity"], obs["gravity"]
    s = -vy
    if s <= 0:
        return 0
    net = obs["thrust_levels"][2] - g
    t = obs["safe_speed"]                       # aim to arrive at exactly the limit
    need = max(0.0, (s*s - t*t) / (2*net))
    return 2 if y <= need else 0
```

| | success | score |
|---|---|---|
| **v3** — predictive | **6.5%** | **6.2** |

The physics is textbook-correct and it is **catastrophically worse than the naive version
it replaced** — from 100% success to 6.5%.

> **If I had swapped v2 for v3 without re-measuring, I would have destroyed a working
> solution at minute 28 and had no idea.** This is why "always keep the last passing
> version" is the non-negotiable rule. It costs one commented-out function.

### Diagnosing it properly

The instinct is to start tuning constants. Don't — find out what's actually happening
first. I measured the impact speeds:

```
v3: impact speed  mean=0.959  median=0.971  max=1.147   limit=0.8   over-limit=282/300
```

It isn't crashing wildly. It is landing at **0.96 when the limit is 0.80** — consistently,
narrowly over. Then the last frames of one episode:

```
alt=   7.17  vy=-1.566  action=2
alt=   5.72  vy=-1.456  action=2
alt=   4.37  vy=-1.346  action=2
alt=   2.01  vy=-1.126  action=2
alt=   1.00  vy=-1.016  action=2
alt=   0.09  vy=-0.906  action=2
alt=   0.00  vy=-0.796  action=2
```

Full thrust the whole way down, bleeding 0.11 per frame, arriving *just* at the boundary.
Two distinct causes, and they compound:

1. **No margin.** It targets arrival at exactly 0.8. Even with perfect execution, that puts
   half your outcomes on the wrong side of the line. You never aim a controller at the
   failure threshold.
2. **Discrete time.** The formula is continuous-time. It assumes thrust starts at the exact
   switching altitude. In reality the decision happens once per frame and the state jumps by
   a whole `vy` each step, so you commit **systematically one frame late** and arrive faster
   than the algebra promises. The 0.96-vs-0.80 gap *is* that lag.

> This is the single most transferable lesson here, and it's exactly the dimension the
> brief says is being graded — *"how you reason about a system that unfolds over time."*
> **Correct continuous-time physics is not a correct discrete-time controller.** Whenever
> you port a formula into a per-frame policy, you owe it a margin and a lead term.

## Minute 28–36 — Two fixes, applied one at a time

Fix the margin first, alone, so I can see what it's worth:

```python
    t = obs["safe_speed"] * 0.55                # aim well inside the limit
```

| | success | score |
|---|---|---|
| **v4** — margin only | 78.8% | 74.4 |

Big improvement, still **worse than the naive v2** (100% / 83.7). Margin alone doesn't fix
the timing lag. Now the lead term — start braking one frame's worth of distance early:

```python
    return 2 if y <= need + s else 0            # s = one frame of travel
```

| | success | score | fuel used |
|---|---|---|---|
| **v5** — margin + lead | **100.0%** | **93.8** | **41 / 200** |

```
v5: impact speed  mean=0.400  median=0.408  max=0.490   limit=0.8   over-limit=0/300
```

Landing at 0.40 against a 0.8 limit — a factor of two of headroom on the worst episode —
while using **41 fuel instead of v2's 109.**

> Note that applying the fixes **one at a time** is what told me the margin alone was
> insufficient. Had I applied both together and seen 93.8, I'd have learned nothing about
> which one mattered, and I'd have no idea which constant to touch if a hidden test failed.

## The whole run

| | policy | success | score |
|---|---|---|---|
| v0 | do nothing | 0.0% | 0.0 |
| v1 | reactive, **sign bug** | 0.0% | 0.0 |
| v2 | reactive, sign fixed | **100.0%** | 83.7 |
| v3 | predictive, no margin, no lead | 6.5% | 6.2 |
| v4 | + margin on target | 78.8% | 74.4 |
| v5 | + one frame of lead | **100.0%** | **93.8** |

The shape to notice: **success rate is not monotonic.** It goes 0 → 0 → 100 → 6.5 → 79 →
100. A candidate who measures only at the start and the end sees a clean improvement and
learns nothing. A candidate who never measures ships v3.

## Minute 36–48 — Edge cases, before tuning

Tuning constants is the most tempting and least valuable thing to do with the remaining
time. Hidden tests are more likely to hit a case I haven't considered than a case where my
gain is 5% off. So I went looking for states the policy has never seen:

| Case | What I checked | Outcome |
|---|---|---|
| Rising (`vy > 0`) | `if s <= 0: return 0` — already guarded | Never wastes fuel thrusting upward |
| Fuel exhausted | `step()` silently downgrades to action 0 | Policy can't tell; v5 uses 41/200, so unreachable here — but it would degrade quietly, which is worth *knowing* |
| Frame 0 | No history used, `mem` never read | Safe by construction |
| Already at `y ≈ 0` | `need` ≥ 0 always; returns 2; lands | Safe |
| Extreme altitude | Tested by widening the spawn range | Held up |
| Division | `2*net` — constant, nonzero | Safe |

The `mem` observation is worth stating: **this policy needs no persistent state at all.**
Altitude and velocity are sufficient. I checked that deliberately rather than reaching for a
state machine out of habit — a phase machine here would add transitions that can chatter,
for no benefit.

> The general move: **before adding machinery, ask whether the current observation is
> already sufficient.** Complexity you don't need is complexity that can break under a
> hidden test.

## Minute 48–56 — Tuning, and the trap inside it

Only now, constants. The margin coefficient `0.55` and the lead coefficient `1.0` were both
guesses. Sweeping the margin alone, 1000 episodes each:

| margin `c` | success | score |
|---|---|---|
| 0.55 | 100.00% | 93.77 |
| 0.80 | 100.00% | 94.30 |
| 0.85 | 100.00% | 94.40 |
| 0.90 | 100.00% | 94.50 |
| **0.92** | **100.00%** | **94.55** |
| 0.94 | 99.60% | 94.21 |
| 1.00 | 72.20% | 68.40 |

There's the cliff, located: it holds to `c = 0.92` and falls off a ledge by `0.94`. My
initial 0.55 was leaving about 0.8 points on the table.

Then I swept the lead term, and found the thing worth the whole section:

| config | success | score |
|---|---|---|
| `c=0.55, lead=1.0` | 100.00% | 93.77 |
| `c=0.55, lead=0.5` | 100.00% | 94.19 |
| `c=0.85, lead=1.0` | 100.00% | 94.40 |
| **`c=0.85, lead=0.5`** | **65.40%** | **61.88** |

**Each change helps on its own. Together they collapse the policy to 65%.**

> **You cannot tune coupled constants independently.** Margin and lead are two ways of
> buying the same safety, and reducing both at once spends it twice. A sweep of one
> variable at a time will confidently tell you that each is an improvement, and a sweep of
> one variable at a time is exactly what everybody does under time pressure.
>
> I only caught this because I tested the combination rather than assuming the gains added.

### Choosing what to actually submit

`c=0.85, lead=1.0` measures better than my `c=0.55, lead=1.0` — 94.40 vs 93.77. So I
checked whether the advantage survives conditions the policy has never seen, by widening
the spawn range far past what the visible tests use (altitude 40–200 instead of 80–120,
initial speed up to 2.5 instead of 1.0):

| config | success on wide range | score |
|---|---|---|
| `c=0.55, lead=1.0` | 100.00% | 92.61 |
| `c=0.85, lead=1.0` | 100.00% | 93.26 |
| `c=0.85, lead=0.5` | 57.80% | 54.21 |

Both survive; the more aggressive one is still ahead. **So the honest statement is that the
reference solution in `reference.py` is not optimal — `c=0.85` beats it by about 0.6 points
on both the standard and the widened range.**

I left the reference at `0.55` anyway, and that is a judgment rather than an optimum: 0.85
sits about 0.08 from a cliff I can see, against hidden tests whose initial conditions I
can't. Six tenths of a point is not worth most of my margin. **What matters for your exam
is not which choice I made — it's that the choice was made explicitly, with the cliff
located and the robustness measured, instead of by stopping wherever the sweep happened to
end.**

I had also written, before running any of this, that the fuel floor was "around 32."
That was wrong — an arithmetic guess I hadn't checked. The measured optimum is nearer 37.
Which is the lesson in miniature: **the estimate you didn't measure is the one that's
wrong.**

## Where the AI assistant fits

The brief says you're expected to use it. Concretely, across this hour:

| Minute | What I'd delegate | What I'd keep |
|---|---|---|
| 0–7 | "Summarise the state variables, action effects and scoring in this `step()` function" | **Verifying the sign convention myself.** It got mine wrong once already and that's the bug that cost v1. |
| 20 | "Give me the distance to decelerate from v to v_target at constant a" | Deciding *that a switching surface is the right structure*. That decision is what's being graded. |
| 28 | "Here's my policy and the failing trace — what would make it land systematically fast?" | Reading the trace myself first. I already knew it was 0.96-vs-0.80 before asking anything. |
| 36–48 | **"What initial conditions would break this policy?"** — highest-value prompt of the hour | Judging which of its suggestions are real. |

The rule that held throughout: **I could explain every line I submitted.** When v3 cratered,
I fixed it in eight minutes because I'd written it and knew which assumption was load-bearing.
Had it been pasted in, I'd have been tuning constants blind against a hidden test suite.

## What to take into the room

1. **Read the scoring function before writing a policy.** It decides what problem you're solving.
2. **Compute the bounds early.** Best deceleration, worst-case requirement, budget. Ninety seconds, and it reframes the task.
3. **Get a running artifact by minute 12**, however bad. It's your baseline *and* your insurance.
4. **A silent no-op looks exactly like a bad policy.** Keep a do-nothing baseline so you can tell them apart.
5. **"It works" and "it scores" are different questions.**
6. **Measure after every change.** Success rate is not monotonic in cleverness.
7. **Never replace a working policy without keeping it.** One commented-out function.
8. **Diagnose before tuning.** Look at the failing trace; find the mechanism.
9. **Continuous-time physics needs a margin and a lead term** to survive discrete control.
10. **Apply fixes one at a time** so you know which one mattered — **then test the
    combination.** Two changes that each help can collapse the policy together.
11. **Edge cases before constants.** Hidden tests probe unseen states, not suboptimal gains.
12. **Ask whether you need persistent state at all** before building a state machine.
13. **Locate the cliff, don't just find the peak.** Knowing where the policy breaks is
    worth more than the last half-point before it.
14. **Test on conditions the visible cases don't cover** before choosing final constants.
15. **The estimate you didn't measure is the one that's wrong.**
