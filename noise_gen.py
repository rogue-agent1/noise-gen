#!/usr/bin/env python3
"""noise_gen - Perlin and simplex noise generators."""
import math, sys, random

class PerlinNoise:
    def __init__(self, seed=0):
        random.seed(seed)
        self.perm = list(range(256))
        random.shuffle(self.perm)
        self.perm *= 2
        self.grad = [(math.cos(2*math.pi*i/8), math.sin(2*math.pi*i/8)) for i in range(8)]
    
    def _fade(self, t):
        return t * t * t * (t * (t * 6 - 15) + 10)
    
    def _lerp(self, a, b, t):
        return a + t * (b - a)
    
    def _dot_grad(self, ix, iy, x, y):
        g = self.grad[self.perm[self.perm[ix & 255] + (iy & 255)] % 8]
        return g[0] * (x - ix) + g[1] * (y - iy)
    
    def noise2d(self, x, y):
        x0 = int(math.floor(x))
        y0 = int(math.floor(y))
        x1, y1 = x0 + 1, y0 + 1
        sx = self._fade(x - x0)
        sy = self._fade(y - y0)
        n00 = self._dot_grad(x0, y0, x, y)
        n10 = self._dot_grad(x1, y0, x, y)
        n01 = self._dot_grad(x0, y1, x, y)
        n11 = self._dot_grad(x1, y1, x, y)
        ix0 = self._lerp(n00, n10, sx)
        ix1 = self._lerp(n01, n11, sx)
        return self._lerp(ix0, ix1, sy)
    
    def octave(self, x, y, octaves=4, persistence=0.5, lacunarity=2):
        total = 0
        amplitude = 1
        frequency = 1
        max_val = 0
        for _ in range(octaves):
            total += self.noise2d(x * frequency, y * frequency) * amplitude
            max_val += amplitude
            amplitude *= persistence
            frequency *= lacunarity
        return total / max_val

def fractal_noise(width, height, scale=0.05, octaves=4, seed=42):
    pn = PerlinNoise(seed)
    grid = []
    for y in range(height):
        row = []
        for x in range(width):
            v = pn.octave(x * scale, y * scale, octaves)
            row.append(v)
        grid.append(row)
    return grid

def normalize(grid):
    flat = [v for row in grid for v in row]
    mn, mx = min(flat), max(flat)
    rng = mx - mn or 1
    return [[(v - mn) / rng for v in row] for row in grid]

def to_ascii(grid, chars=" .:-=+*#%@"):
    return "\n".join("".join(chars[min(len(chars)-1, int(v * (len(chars)-1)))] for v in row) for row in grid)

def test():
    pn = PerlinNoise(seed=42)
    v = pn.noise2d(0.5, 0.5)
    assert -1 <= v <= 1
    
    v2 = pn.octave(0.5, 0.5, octaves=4)
    assert -1 <= v2 <= 1
    
    # Deterministic
    assert pn.noise2d(1.5, 2.5) == pn.noise2d(1.5, 2.5)
    
    # Different seeds differ
    pn2 = PerlinNoise(seed=99)
    assert pn.noise2d(0.5, 0.5) != pn2.noise2d(0.5, 0.5)
    
    # Fractal noise
    grid = fractal_noise(20, 10, scale=0.1, seed=42)
    assert len(grid) == 10
    assert len(grid[0]) == 20
    
    norm = normalize(grid)
    flat = [v for row in norm for v in row]
    assert min(flat) >= 0 and max(flat) <= 1
    
    ascii_art = to_ascii(norm)
    assert len(ascii_art.split("\n")) == 10
    
    print(ascii_art)
    print("All tests passed!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test()
    elif len(sys.argv) > 1:
        w = int(sys.argv[1]) if len(sys.argv) > 1 else 80
        h = int(sys.argv[2]) if len(sys.argv) > 2 else 40
        grid = normalize(fractal_noise(w, h))
        print(to_ascii(grid))
    else:
        print("Usage: noise_gen.py [width] [height] | test")
