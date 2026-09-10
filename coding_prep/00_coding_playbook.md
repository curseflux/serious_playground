# AI-Assisted Advanced Coding Assessment — Playbook

**Epistemic status.** I don't know what the actual task is. What follows is decoded from
the assessment description plus what "control policy for a physics simulation, called once
per frame, returns a single decision" almost certainly means. The *patterns* are what
transfer; treat any specific environment as illustrative.

---

## 1. Decoding the brief

> *"You will write a control policy for a simple physics simulation: a function that is
> called once per frame and returns a single decision about what to do next."*

Unpacked:

- **Discrete action space.** "A single decision" means picking from a small set, not
  emitting a continuous vector. Expect something like `{left, right}`, `{off, low, high}`,
  `{-1, 0, +1}`.
- **Frame-by-frame, stateless by default.** Your function gets called with the state and
  returns an action. If you need history — a phase label, a previous reading, a counter —
  **you have to store it yourself**, in a closure, a module-level variable, or a mutable
  argument. This trips people up in the first five minutes.
- **Not machine learning.** Sixty minutes, no training loop, automated tests. This is
  hand-written classical control: proportional/derivative feedback, switching surfaces,
  small state machines, forward prediction.
- **"How you reason about a system that unfolds over time"** is the graded dimension.
  Meaning: they want to see that you control on where the system *will be*, not only on
  where it is.

The plausible task families: a lander or rocket descent, cart-pole or a balancing problem,
an intercept/catch task, a car on a track, a mountain-car-style underpowered system, a
Flappy-Bird-shaped timing problem. The harness in this folder covers four of those shapes.

## 2. Read the simulator before you write anything

The single highest-value five minutes: **open the provided simulator source and read the
step function.** It is the actual spec. It tells you:

- exact physics constants (gravity, thrust, drag, timestep)
- the sign convention (is down negative? is action 0 left or right?)
- the terminal conditions — what counts as success, exactly
- **how scoring works**, which is often not what you'd assume (a fuel penalty, a time
  bonus, partial credit per sub-goal)
- whether actions are clamped, and what happens on an illegal action

People lose points guessing at things that are written down twenty lines away. In this
practice harness, `sim.py` is that file — read it before touching `policies.py`.

## 3. The control patterns worth having loaded

This is the coding equivalent of the hypothesis library. Know these cold.

### P and PD control — the workhorse
```python
error = target - current
signal = Kp * error + Kd * (-current_rate)     # Kd damps; it is what stops overshoot
action = HIGH if signal > 0 else LOW
```
Proportional alone oscillates or overshoots. The derivative term is what makes it settle.
For an unstable system (a pole falling), **the derivative term is doing most of the work**
— by the time the error is large you have already lost.

### Deadband and hysteresis — the fix for chattering
A bang-bang controller flipping every frame around the switching point burns fuel, looks
bad, and can be unstable. Give it a dead zone:
```python
if abs(error) < DEADBAND:
    return NEUTRAL
```
Or two thresholds (turn on at 1.0, off at 0.6) so it can't flip on a single frame's noise.
Chattering is the commonest visible defect in a first-draft policy.

### Switching surface / predictive braking
Instead of reacting to the current error, ask: **is the future still recoverable?** For
anything with a terminal constraint (land under a speed, stop before a wall):
```python
stopping_distance = (v**2 - v_target**2) / (2 * max_decel)
if remaining_distance <= stopping_distance + one_frame_of_lead:
    brake_hard()
else:
    coast()
```
This is the fuel-optimal and time-optimal shape, and it is the pattern that most
distinguishes a considered policy from a reactive one. Add a frame of lead, because your
control is discrete and you'll otherwise commit one frame late.

### Forward simulation
When you know the dynamics of something you don't control (a falling ball, an incoming
obstacle), **roll it forward to its terminal state and aim at that**, recomputing each
frame. Do not chase its current position. Bound the loop so a degenerate case can't hang.

### Energy / invariant reasoning
Some systems can't be solved by pushing toward the goal — the actuator is too weak
(mountain car), or the direct path is blocked. Ask what quantity you *can* monotonically
change. Pushing in the direction of your current velocity always adds energy, regardless
of which way you're facing. When greedy fails, look for the conserved quantity.

### Phase / state machine
When behaviour should differ qualitatively across stages — approach, align, descend,
touch down — a small explicit phase variable in your persistent state beats one giant
expression. Keep transitions one-way where you can; two-way transitions near a boundary
reintroduce chattering.

### Saturation and guards
Clamp everything. Check for division by zero, empty history on frame 0, and the state
where the thing you're tracking doesn't exist yet. **A crash scores zero for that
episode**, so a guard is worth more than an optimisation.

### Your action shapes your future options
The subtle one, and the one that most directly matches *"reason about a system that
unfolds over time."* An action that is fine right now can leave you without the authority
you need later. In the harness's `lander`, a reactive policy that thrusts whenever it's
falling too fast lands successfully **every time** — and burns 109 of its 200 fuel doing
it, where a predictive burn uses 41. Fuel spent early is deceleration you no longer have
at the moment it matters. Coasting isn't passivity; it's keeping your options open.

Generalise: before committing an action, ask what it costs you *later* — fuel, position,
time, remaining margin. Reactive policies spend those resources continuously without
noticing.

## 4. The 60 minutes

| Clock | What |
|---|---|
| 0–7 | Read the task **and the simulator source**. Write down: state variables, action set, sign conventions, terminal conditions, scoring function. |
| 7–12 | Get the dumbest possible policy running end to end and see a score. Constant action, or one-line P control. **You now have a submittable artifact.** |
| 12–20 | Watch it fail in the visual simulator. Name the failure mode in words before changing anything. |
| 20–40 | Implement the real policy — usually PD, or a switching surface, or forward prediction. Test after each change. |
| 40–52 | Edge cases and robustness. Extreme initial conditions, the boundaries, resource exhaustion, frame 0. Add guards. |
| 52–58 | Tune constants. Re-run everything. Confirm nothing regressed. |
| 58–60 | Final submit. |

**Non-negotiables:**
- **Always have something submittable.** Partial credit is explicit in the brief. Never be
  in a state where the file doesn't run.
- **Never break a working policy without a way back.** Keep the last passing version in a
  comment or a second function. Sixty minutes is not enough time to recover from
  "it worked ten minutes ago."
- **Hidden tests exist.** The brief says so. So do not tune to the visible cases —
  deliberately test initial conditions the visible cases don't cover, and prefer a policy
  that's principled over one that's fitted.

## 5. Working with the AI assistant

This is graded terrain, not a loophole. The brief says the assessment is *designed around*
using it. What separates good AI-assisted engineering from bad:

**Use it for:**
- Reading the provided simulator and summarising the physics and sign conventions. Then
  *verify* — models get sign conventions confidently wrong.
- Deriving the algebra: "given constant deceleration a, distance to go from v to v_target."
- Enumerating edge cases: "what initial conditions would break this policy?" This is one
  of the highest-value prompts you can send.
- Boilerplate, refactors, and debugging print statements.
- Critique: paste your policy and ask what it misses. Then judge the answer.

**Don't:**
- Ask for the whole controller and paste it in. You will not be able to debug what you
  don't understand, and the hidden tests will find the part you didn't read.
- Accept physics claims without checking them against the simulator's actual behaviour.
- Let it make the core design decision (PD vs. switching surface vs. state machine).
  That decision *is* the thing being assessed.
- Take a large diff you can't explain line by line.

**The rule:** you can use as much of it as you like, but you must be able to explain every
line you submit. The moment you can't, you've traded away your ability to fix the next
failure — and with hidden tests, there will be a next failure.

## 6. Failure modes to recognise on sight

| Symptom | Cause | Fix |
|---|---|---|
| Rapid oscillation / chattering | Bang-bang with no dead zone | Deadband or hysteresis |
| Overshoots the target, then corrects | P-only control | Add a derivative term |
| Stable but scores badly | Optimising survival, not the scoring function | Re-read how score is computed |
| Works from the default start, fails elsewhere | Fitted to the visible cases | Test extreme initial conditions |
| Fine early, fails at the end | No terminal constraint handling | Switching surface, predictive braking |
| Never reaches the goal at all | Greedy action is wrong | Look for the energy / invariant argument |
| Occasional zero scores | Unguarded crash | Guard frame 0, division, empty state |
| Slightly late every time | Discrete control, no lead | Act on predicted next-frame state |

## 7. Using the practice harness

```bash
cd coding_prep
python3 sim.py lander --render              # watch it; obs keys are in sim.py
python3 sim.py lander --episodes 300        # score your policy
python3 sim.py all                          # everything
python3 sim.py cartpole --policy reference  # the worked solution
```

Fill in `policies.py`. Don't open `reference.py` until you've genuinely attempted one.

**Suggested drills, hardest lesson last:**

1. **`cartpole`** — PD control. Get to 100%. Then try to do it with proportional control
   only and watch it fail; that's the derivative term earning its place.
2. **`lander`** — terminal constraint and resource budgeting. A reactive "thrust if
   falling too fast" policy succeeds **100% of the time** and scores 83.7. A predictive
   burn also succeeds 100% and scores 93.8, using 41 fuel instead of 109. Both "work".
   This is the read-the-scoring-function lesson made concrete: your first working policy
   can be leaving most of the points on the table.
3. **`intercept`** — forward prediction. Try chasing `ball_x` first: it scores 68.4 and
   catches every ball in only 2.7% of episodes, because the ball moves sideways faster
   than the paddle can travel. Predicting the landing point scores 100.
4. **`mountaincar`** — the greedy trap. Try "always push toward the goal" first. It never
   arrives. Sit with that before reaching for the answer; recognising that the obvious
   objective-directed action is wrong is exactly the judgment being tested.

**Then do one under real conditions:** 60 minutes, timer on, a task you haven't seen — get
a friend to change the constants in one environment, or invert a sign convention, and
solve it cold.

Reference scores to beat, over 400 episodes:

| env | reference: success | reference: score | a plausible naive policy |
|---|---|---|---|
| `lander` | 100% | **93.8** | reactive thrust: 100% success, **83.7** |
| `cartpole` | 100% | **100.0** | P-only, no damping: 0% success, **8.4** |
| `intercept` | 100% | **100.0** | chase `ball_x`: 2.7% success, **68.4** |
| `mountaincar` | 100% | **85.1** | always push toward goal: 0% success, **0.0** |

All four are solvable to 100% success. The naive column is what you get from the obvious
first idea — note that on `lander` the obvious idea *succeeds every time* and still loses
ten points. Two of these four naive policies score zero, and two look like they work.
Telling those apart is the skill.
