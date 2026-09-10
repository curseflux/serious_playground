"""Worked solutions. Don't read these until you've had a real attempt.

Each one is annotated with the control pattern it uses, because the patterns
are what transfer -- the specific environments won't be on your test.
"""

# ---------------------------------------------------------------------------
# LANDER -- predictive bang-bang on a switching surface
#
# The pattern: don't control on the current error, control on whether the
# FUTURE is still recoverable. Compute the distance you need in order to bleed
# off your speed at maximum authority. Coast while you have more room than
# that; burn when you don't. This is the fuel-optimal shape (freefall, then one
# hard burn) and it generalises to anything with a terminal constraint.
#
# The trap: a naive "if falling too fast, thrust" controller also lands 100% of
# the time -- but burns ~109 fuel where this one burns ~41, scoring 83.7 vs 93.8.
# It succeeds and still loses most of the available points.
#
# It is also the clearest case in this harness of actions shaping future options:
# fuel spent early is control authority you no longer have at the moment you
# most need it. Coasting is not passivity, it is keeping your options open.
# ---------------------------------------------------------------------------

def act_lander(obs, mem):
    y = obs["altitude"]
    vy = obs["velocity"]
    g = obs["gravity"]
    hi = obs["thrust_levels"][2]
    target = obs["safe_speed"] * 0.55        # aim comfortably inside the limit

    speed = -vy                              # falling is negative
    if speed <= 0.0:                         # rising: never waste fuel
        return 0

    net = hi - g                             # best available deceleration
    # distance needed to go from `speed` down to `target` at full thrust
    need = max(0.0, (speed * speed - target * target) / (2.0 * net))

    if y <= need + speed:                    # one frame of lead, for discreteness
        return 2
    return 0


# ---------------------------------------------------------------------------
# CARTPOLE -- PD control with a slow secondary objective
#
# The pattern: a weighted sum of (error, error rate) for the fast unstable
# variable, plus a much smaller weight on the slow variable you also care
# about. The pole must be corrected now; the cart position can be corrected
# over hundreds of frames, so it gets a small coefficient and rides along.
#
# The trap: reacting to angle alone. By the time theta is large the pole is
# already falling; the derivative term is what makes it stable. And if you
# weight x too heavily you'll fight the pole to save the cart and lose both.
# ---------------------------------------------------------------------------

def act_cartpole(obs, mem):
    th = obs["theta"]
    thd = obs["theta_dot"]
    x = obs["x"]
    xd = obs["x_dot"]

    # pole term dominates; cart term is deliberately an order of magnitude smaller
    signal = (th * 1.0) + (thd * 0.35) + (x * 0.06) + (xd * 0.14)
    return 1 if signal > 0.0 else 0


# ---------------------------------------------------------------------------
# INTERCEPT -- forward simulation, then track the prediction
#
# The pattern: when you know the dynamics of the thing you're chasing and it
# is not affected by your actions, simulate it forward to its terminal state
# and control toward THAT, not toward where it is now. Recompute every frame,
# so the prediction stays honest and you never need it to be exactly right.
#
# The trap: chasing ball_x. A ball moving sideways faster than the paddle can
# never be caught by following it, and wall bounces mean the ball's current
# direction may be the opposite of where it will end up.
# ---------------------------------------------------------------------------

def _predict_landing(obs):
    """Roll the ball forward to y <= 0 and return its x there."""
    x, y = obs["ball_x"], obs["ball_y"]
    vx, vy = obs["ball_vx"], obs["ball_vy"]
    g, w = obs["gravity"], obs["width"]

    for _ in range(2000):                    # bounded: never loop forever
        if y <= 0.0:
            break
        vy -= g
        x += vx
        y += vy
        if x < 0.0:
            x = -x
            vx = -vx
        elif x > w:
            x = 2.0 * w - x
            vx = -vx
    return x


def act_intercept(obs, mem):
    # recompute each frame; cheap, and self-correcting
    target = _predict_landing(obs)
    err = target - obs["paddle_x"]

    # deadband sized to the paddle's per-frame step, so it stops instead of
    # oscillating around the target
    if abs(err) >= obs["paddle_speed"]:
        return 1 if err > 0 else -1

    return 0


# ---------------------------------------------------------------------------
# MOUNTAIN CAR -- reason about the conserved quantity, not the goal direction
#
# The pattern: the greedy action is wrong. The engine is weaker than gravity
# on the slope, so pushing toward the goal stalls. What you can control is
# total energy: push in the direction you're already moving and every frame
# adds energy, whichever way you happen to be pointing.
#
# The trap: "the goal is to the right, so push right." It never arrives. This
# is the environment that punishes optimising the visible objective directly
# instead of asking what the system actually conserves.
# ---------------------------------------------------------------------------

def act_mountaincar(obs, mem):
    v = obs["velocity"]
    if v == 0.0:                             # at rest: pick a direction and commit
        return 2
    return 2 if v > 0.0 else 0
