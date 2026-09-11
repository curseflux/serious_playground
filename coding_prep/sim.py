#!/usr/bin/env python3
"""
Practice harness for a frame-by-frame control-policy assessment.

Mirrors the shape of the task: a function is called once per frame with the
current state, and returns one discrete decision. Nothing here depends on
numpy, gym, or anything outside the standard library.

Usage
-----
    python3 sim.py lander                       # run your policy, 200 episodes
    python3 sim.py lander --render --delay 0.02 # watch one episode in ASCII
    python3 sim.py cartpole --episodes 500
    python3 sim.py intercept --policy reference # run the worked solution
    python3 sim.py all                          # score every environment

Your policies live in policies.py. Worked solutions live in reference.py --
don't open that until you've had a real attempt.
"""

import argparse
import importlib
import math
import random
import sys
import time

# --------------------------------------------------------------------------
# Environments
#
# Each env exposes:
#   NAME, ACTIONS (list of legal actions), DESC
#   reset(rng)      -> obs dict
#   step(action)    -> (obs, done, info)   info has 'success' when done
#   render()        -> str
#   MAX_FRAMES
# --------------------------------------------------------------------------


class Lander:
    """Vertical descent under gravity with a throttle and finite fuel.

    Land with |vy| <= SAFE_SPEED to succeed. Fuel spent is scored, so a policy
    that hovers all the way down passes but scores poorly.
    """

    NAME = "lander"
    DESC = "Land softly. 0=off 1=low 2=high. Fuel is finite and scored."
    ACTIONS = [0, 1, 2]
    MAX_FRAMES = 1200

    GRAVITY = 0.05
    THRUST = {0: 0.0, 1: 0.08, 2: 0.16}
    BURN = {0: 0, 1: 1, 2: 2}
    SAFE_SPEED = 0.8
    START_FUEL = 200

    def reset(self, rng):
        self.y = rng.uniform(80.0, 120.0)
        self.vy = rng.uniform(-1.0, 0.0)
        self.fuel = float(self.START_FUEL)
        self.frame = 0
        self.last_action = 0
        return self._obs()

    def _obs(self):
        return {
            "altitude": self.y,
            "velocity": self.vy,
            "fuel": self.fuel,
            "gravity": self.GRAVITY,
            "thrust_levels": dict(self.THRUST),
            "safe_speed": self.SAFE_SPEED,
            "frame": self.frame,
        }

    def step(self, action):
        if action not in self.ACTIONS:
            raise ValueError(f"illegal action {action!r}")
        if self.fuel < self.BURN[action]:
            action = 0
        self.last_action = action
        self.fuel -= self.BURN[action]
        self.vy += self.THRUST[action] - self.GRAVITY
        self.y += self.vy
        self.frame += 1

        if self.y <= 0.0:
            self.y = 0.0
            ok = abs(self.vy) <= self.SAFE_SPEED
            # score: landing is most of it, fuel saved is the tiebreak
            score = (70.0 + 30.0 * (self.fuel / self.START_FUEL)) if ok else 0.0
            return self._obs(), True, {"success": ok, "score": score,
                                       "impact": abs(self.vy)}
        if self.frame >= self.MAX_FRAMES:
            return self._obs(), True, {"success": False, "score": 0.0,
                                       "impact": abs(self.vy), "timeout": True}
        return self._obs(), False, {}

    def render(self):
        h = 22
        row = h - 1 - min(h - 1, int(self.y / 130.0 * (h - 1)))
        flame = {0: "   ", 1: " v ", 2: "vVv"}[self.last_action]
        out = []
        for r in range(h):
            if r == row:
                out.append(f"      [=]{'':2}   vy={self.vy:+6.2f}  alt={self.y:6.1f}  fuel={self.fuel:5.0f}")
            elif r == row + 1:
                out.append(f"      {flame}")
            else:
                out.append("")
        out.append("~" * 46)
        return "\n".join(out)


class CartPole:
    """Balance an inverted pendulum on a cart. 0=push left, 1=push right."""

    NAME = "cartpole"
    DESC = "Keep the pole up and the cart on the track. 0=left 1=right."
    ACTIONS = [0, 1]
    MAX_FRAMES = 500

    G = 9.8
    M_CART = 1.0
    M_POLE = 0.1
    LENGTH = 0.5          # half the pole's length
    FORCE = 10.0
    TAU = 0.02
    THETA_LIMIT = 12 * math.pi / 180
    X_LIMIT = 2.4

    def reset(self, rng):
        self.x = rng.uniform(-0.05, 0.05)
        self.xd = rng.uniform(-0.05, 0.05)
        self.th = rng.uniform(-0.05, 0.05)
        self.thd = rng.uniform(-0.05, 0.05)
        self.frame = 0
        return self._obs()

    def _obs(self):
        return {
            "x": self.x, "x_dot": self.xd,
            "theta": self.th, "theta_dot": self.thd,
            "x_limit": self.X_LIMIT, "theta_limit": self.THETA_LIMIT,
            "frame": self.frame,
        }

    def step(self, action):
        if action not in self.ACTIONS:
            raise ValueError(f"illegal action {action!r}")
        force = self.FORCE if action == 1 else -self.FORCE
        total_m = self.M_CART + self.M_POLE
        pml = self.M_POLE * self.LENGTH
        ct, st = math.cos(self.th), math.sin(self.th)

        temp = (force + pml * self.thd ** 2 * st) / total_m
        thacc = (self.G * st - ct * temp) / (
            self.LENGTH * (4.0 / 3.0 - self.M_POLE * ct ** 2 / total_m))
        xacc = temp - pml * thacc * ct / total_m

        self.x += self.TAU * self.xd
        self.xd += self.TAU * xacc
        self.th += self.TAU * self.thd
        self.thd += self.TAU * thacc
        self.frame += 1

        dead = abs(self.th) > self.THETA_LIMIT or abs(self.x) > self.X_LIMIT
        if dead:
            return self._obs(), True, {"success": False,
                                       "score": 100.0 * self.frame / self.MAX_FRAMES}
        if self.frame >= self.MAX_FRAMES:
            return self._obs(), True, {"success": True, "score": 100.0}
        return self._obs(), False, {}

    def render(self):
        w = 46
        col = int((self.x + self.X_LIMIT) / (2 * self.X_LIMIT) * (w - 1))
        col = max(0, min(w - 1, col))
        track = [" "] * w
        track[col] = "#"
        lean = int(round(self.th / self.THETA_LIMIT * 6))
        top = [" "] * w
        tc = max(0, min(w - 1, col + lean))
        top[tc] = "|"
        return ("\n".join(["".join(top), "".join(track), "-" * w])
                + f"\n x={self.x:+5.2f} th={math.degrees(self.th):+6.2f}deg frame={self.frame}")


class Intercept:
    """Catch falling balls with a paddle. -1=left 0=stay 1=right.

    Balls move sideways FASTER than the paddle can travel, and bounce off the
    side walls. Chasing the ball's current x position cannot work; the landing
    point has to be predicted.
    """

    NAME = "intercept"
    DESC = "Catch the balls. -1=left 0=stay 1=right. Balls bounce off walls."
    ACTIONS = [-1, 0, 1]
    MAX_FRAMES = 3000
    N_BALLS = 12

    WIDTH = 100.0
    HEIGHT = 60.0
    PADDLE_HALF = 5.0
    PADDLE_SPEED = 2.2
    GRAVITY = 0.06

    def reset(self, rng):
        self.rng = rng
        self.px = self.WIDTH / 2
        self.caught = 0
        self.dropped = 0
        self.frame = 0
        self._spawn()
        return self._obs()

    def _spawn(self):
        self.bx = self.rng.uniform(10, self.WIDTH - 10)
        self.by = self.HEIGHT
        self.bvx = self.rng.uniform(-3.6, 3.6)
        self.bvy = 0.0

    def _obs(self):
        return {
            "paddle_x": self.px, "paddle_half_width": self.PADDLE_HALF,
            "paddle_speed": self.PADDLE_SPEED,
            "ball_x": self.bx, "ball_y": self.by,
            "ball_vx": self.bvx, "ball_vy": self.bvy,
            "gravity": self.GRAVITY, "width": self.WIDTH, "height": self.HEIGHT,
            "caught": self.caught, "dropped": self.dropped, "frame": self.frame,
        }

    def step(self, action):
        if action not in self.ACTIONS:
            raise ValueError(f"illegal action {action!r}")
        self.px += action * self.PADDLE_SPEED
        self.px = max(0.0, min(self.WIDTH, self.px))

        self.bvy -= self.GRAVITY
        self.bx += self.bvx
        self.by += self.bvy
        if self.bx < 0:
            self.bx = -self.bx
            self.bvx = -self.bvx
        elif self.bx > self.WIDTH:
            self.bx = 2 * self.WIDTH - self.bx
            self.bvx = -self.bvx

        self.frame += 1
        if self.by <= 0.0:
            if abs(self.bx - self.px) <= self.PADDLE_HALF:
                self.caught += 1
            else:
                self.dropped += 1
            if self.caught + self.dropped >= self.N_BALLS:
                score = 100.0 * self.caught / self.N_BALLS
                return self._obs(), True, {"success": self.caught == self.N_BALLS,
                                           "score": score, "caught": self.caught}
            self._spawn()

        if self.frame >= self.MAX_FRAMES:
            score = 100.0 * self.caught / self.N_BALLS
            return self._obs(), True, {"success": False, "score": score,
                                       "caught": self.caught, "timeout": True}
        return self._obs(), False, {}

    def render(self):
        w, h = 50, 18
        grid = [[" "] * w for _ in range(h)]
        bc = max(0, min(w - 1, int(self.bx / self.WIDTH * (w - 1))))
        br = max(0, min(h - 1, h - 1 - int(self.by / self.HEIGHT * (h - 1))))
        grid[br][bc] = "o"
        pc = int(self.px / self.WIDTH * (w - 1))
        half = max(1, int(self.PADDLE_HALF / self.WIDTH * w))
        for c in range(max(0, pc - half), min(w, pc + half + 1)):
            grid[h - 1][c] = "="
        body = "\n".join("|" + "".join(r) + "|" for r in grid)
        return body + f"\n caught={self.caught} dropped={self.dropped} frame={self.frame}"


class MountainCar:
    """Underpowered car in a valley. 0=push left 1=coast 2=push right.

    The engine cannot climb the hill directly. Pushing toward the goal the
    whole time fails; you have to build energy by driving with your velocity.
    """

    NAME = "mountaincar"
    DESC = "Reach the flag at p >= 0.5. 0=left 1=coast 2=right. Engine is weak."
    ACTIONS = [0, 1, 2]
    MAX_FRAMES = 400

    FORCE = 0.001
    GRAV = 0.0025
    GOAL = 0.5

    def reset(self, rng):
        self.p = rng.uniform(-0.6, -0.4)
        self.v = 0.0
        self.frame = 0
        return self._obs()

    def _obs(self):
        return {"position": self.p, "velocity": self.v, "goal": self.GOAL,
                "force": self.FORCE, "gravity": self.GRAV, "frame": self.frame}

    def step(self, action):
        if action not in self.ACTIONS:
            raise ValueError(f"illegal action {action!r}")
        self.v += (action - 1) * self.FORCE + math.cos(3 * self.p) * (-self.GRAV)
        self.v = max(-0.07, min(0.07, self.v))
        self.p += self.v
        if self.p < -1.2:
            self.p = -1.2
            self.v = 0.0
        self.frame += 1

        if self.p >= self.GOAL:
            score = 100.0 * (1.0 - 0.5 * self.frame / self.MAX_FRAMES)
            return self._obs(), True, {"success": True, "score": score}
        if self.frame >= self.MAX_FRAMES:
            return self._obs(), True, {"success": False, "score": 0.0}
        return self._obs(), False, {}

    def render(self):
        w = 46
        col = int((self.p + 1.2) / 1.8 * (w - 1))
        col = max(0, min(w - 1, col))
        hill = "".join("_" if i < w - 4 else "F" for i in range(w))
        car = [" "] * w
        car[col] = "@"
        return ("".join(car) + "\n" + hill
                + f"\n p={self.p:+5.2f} v={self.v:+6.4f} frame={self.frame}")


ENVS = {e.NAME: e for e in (Lander, CartPole, Intercept, MountainCar)}


# --------------------------------------------------------------------------
# Runner
# --------------------------------------------------------------------------

def run_episode(env, act, seed, render=False, delay=0.05):
    rng = random.Random(seed)
    obs = env.reset(rng)
    mem = {}
    frames = 0
    while True:
        try:
            action = act(obs, mem)
        except Exception as exc:                      # a crash is a failed run
            return {"success": False, "score": 0.0, "error": repr(exc)}, frames
        obs, done, info = env.step(action)
        frames += 1
        if render:
            print("\033[2J\033[H" + env.render())
            time.sleep(delay)
        if done:
            return info, frames


def evaluate(name, act, episodes, seed0=0, render=False, delay=0.05):
    env = ENVS[name]()
    wins = 0
    total = 0.0
    errors = []
    for i in range(episodes):
        info, _ = run_episode(env, act, seed0 + i, render=render, delay=delay)
        wins += bool(info.get("success"))
        total += info.get("score", 0.0)
        if "error" in info and len(errors) < 3:
            errors.append(info["error"])
        if render:
            break
    n = 1 if render else episodes
    return {"env": name, "episodes": n, "success_rate": wins / n,
            "mean_score": total / n, "errors": errors}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("env", choices=list(ENVS) + ["all"])
    ap.add_argument("--episodes", type=int, default=200)
    ap.add_argument("--policy", default="policies",
                    help="module to import policies from (try: reference)")
    ap.add_argument("--render", action="store_true", help="watch one episode")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--delay", type=float, default=0.05,
                    help="seconds per frame when rendering (try 0.01)")
    args = ap.parse_args()

    try:
        mod = importlib.import_module(args.policy)
    except ImportError as exc:
        print(f"could not import {args.policy!r}: {exc}", file=sys.stderr)
        return 1

    names = list(ENVS) if args.env == "all" else [args.env]
    rows = []
    for name in names:
        fn = getattr(mod, f"act_{name}", None)
        if fn is None:
            print(f"  {name:<12} no act_{name} in {args.policy}.py -- skipped")
            continue
        rows.append(evaluate(name, fn, args.episodes, args.seed, args.render,
                             args.delay))

    if args.render:
        return 0
    print(f"\n  policy module: {args.policy}.py")
    print(f"  {'env':<13}{'episodes':>9}{'success':>10}{'mean score':>13}")
    print("  " + "-" * 45)
    for r in rows:
        print(f"  {r['env']:<13}{r['episodes']:>9}{r['success_rate']:>9.1%}"
              f"{r['mean_score']:>13.1f}")
        for e in r["errors"]:
            print(f"      ! {e}")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
