#!/usr/bin/env python3
"""Perlin-like noise generator. Zero dependencies."""
import math, random, sys

class PerlinNoise:
    def __init__(self, seed=0):
        random.seed(seed)
        self.p = list(range(256))
        random.shuffle(self.p)
        self.p *= 2

    def _fade(self, t): return t*t*t*(t*(t*6-15)+10)
    def _lerp(self, a, b, t): return a + t*(b-a)
    def _grad(self, h, x, y=0):
        h = h & 15
        u = x if h < 8 else y
        v = y if h < 4 else (x if h in (12,14) else 0)
        return (u if h&1 == 0 else -u) + (v if h&2 == 0 else -v)

    def noise2d(self, x, y):
        X, Y = int(math.floor(x)) & 255, int(math.floor(y)) & 255
        x -= math.floor(x); y -= math.floor(y)
        u, v = self._fade(x), self._fade(y)
        A = self.p[X] + Y; B = self.p[X+1] + Y
        return self._lerp(
            self._lerp(self._grad(self.p[A], x, y), self._grad(self.p[B], x-1, y), u),
            self._lerp(self._grad(self.p[A+1], x, y-1), self._grad(self.p[B+1], x-1, y-1), u), v)

    def octave(self, x, y, octaves=4, persistence=0.5):
        total = 0; freq = 1; amp = 1; max_val = 0
        for _ in range(octaves):
            total += self.noise2d(x*freq, y*freq) * amp
            max_val += amp; freq *= 2; amp *= persistence
        return total / max_val

def generate_map(width, height, scale=0.05, seed=0):
    noise = PerlinNoise(seed)
    return [[noise.octave(x*scale, y*scale) for x in range(width)] for y in range(height)]

def to_ascii(nmap, chars=" .:-=+*#%@"):
    result = []
    for row in nmap:
        line = ""
        for v in row:
            idx = int((v + 1) / 2 * (len(chars) - 1))
            idx = max(0, min(len(chars)-1, idx))
            line += chars[idx]
        result.append(line)
    return "\n".join(result)

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Noise generator")
    p.add_argument("-w", "--width", type=int, default=80)
    p.add_argument("-h", "--height", type=int, default=24)
    p.add_argument("-s", "--scale", type=float, default=0.08)
    p.add_argument("--seed", type=int, default=42)
    args = p.parse_args()
    nmap = generate_map(args.width, args.height, args.scale, args.seed)
    print(to_ascii(nmap))
