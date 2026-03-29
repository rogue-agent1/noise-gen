#!/usr/bin/env python3
"""noise_gen - Noise generators (white, pink, Perlin, simplex)."""
import sys, math, random

def white_noise(n, seed=None):
    if seed is not None:
        random.seed(seed)
    return [random.gauss(0, 1) for _ in range(n)]

def pink_noise(n, seed=None):
    if seed is not None:
        random.seed(seed)
    b = [0.0] * 7
    result = []
    for _ in range(n):
        white = random.gauss(0, 1)
        b[0] = 0.99886 * b[0] + white * 0.0555179
        b[1] = 0.99332 * b[1] + white * 0.0750759
        b[2] = 0.96900 * b[2] + white * 0.1538520
        b[3] = 0.86650 * b[3] + white * 0.3104856
        b[4] = 0.55000 * b[4] + white * 0.5329522
        b[5] = -0.7616 * b[5] - white * 0.0168980
        result.append(sum(b[:6]) + white * 0.5362)
        b[6] = white * 0.115926
    return result

def _fade(t):
    return t * t * t * (t * (t * 6 - 15) + 10)

def _lerp(a, b, t):
    return a + t * (b - a)

def perlin_1d(x, perm):
    xi = int(x) & 255
    xf = x - int(x)
    u = _fade(xf)
    g0 = (1 if perm[xi] % 2 == 0 else -1) * xf
    g1 = (1 if perm[(xi+1) & 255] % 2 == 0 else -1) * (xf - 1)
    return _lerp(g0, g1, u)

def perlin_noise(n, scale=0.1, seed=None):
    if seed is not None:
        random.seed(seed)
    perm = list(range(256))
    random.shuffle(perm)
    perm = perm + perm
    return [perlin_1d(i * scale, perm) for i in range(n)]

def test():
    # white noise: mean ~0, std ~1
    wn = white_noise(10000, seed=42)
    assert abs(sum(wn)/len(wn)) < 0.05
    assert 0.9 < (sum(x**2 for x in wn)/len(wn))**0.5 < 1.1
    # pink noise
    pn = pink_noise(1000, seed=42)
    assert len(pn) == 1000
    # perlin noise is smooth
    prl = perlin_noise(100, scale=0.05, seed=42)
    assert len(prl) == 100
    diffs = [abs(prl[i+1] - prl[i]) for i in range(99)]
    assert max(diffs) < 0.5  # smooth
    print("OK: noise_gen")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test()
    else:
        print("Usage: noise_gen.py test")
