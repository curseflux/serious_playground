"""Your policies. Fill these in.

Each function is called ONCE PER FRAME with:
    obs -- a dict of the current state (printed below if you run with --render)
    mem -- a dict that persists across frames within one episode, and is
           reset between episodes. Use it if you need history: a phase label,
           a previous reading to difference, a frame counter.

Return one legal action. Illegal actions raise, and a crash scores zero for
that episode -- so guard your edge cases.

Start each one with the dumbest thing that runs end to end, check the score,
then improve it. That mirrors how you should play the real 60 minutes.
"""


def act_lander(obs, mem):
    # obs: altitude, velocity, fuel, gravity, thrust_levels, safe_speed, frame
    # actions: 0 = off, 1 = low, 2 = high
    return 0


def act_cartpole(obs, mem):
    # obs: x, x_dot, theta, theta_dot, x_limit, theta_limit, frame
    # actions: 0 = push left, 1 = push right
    return 0


def act_intercept(obs, mem):
    # obs: paddle_x, paddle_half_width, paddle_speed, ball_x, ball_y,
    #      ball_vx, ball_vy, gravity, width, height, caught, dropped, frame
    # actions: -1 = left, 0 = stay, 1 = right
    return 0


def act_mountaincar(obs, mem):
    # obs: position, velocity, goal, force, gravity, frame
    # actions: 0 = push left, 1 = coast, 2 = push right
    return 1
