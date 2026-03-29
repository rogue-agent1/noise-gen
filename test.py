from noise_gen import PerlinNoise, generate_map, to_ascii
n = PerlinNoise(42)
v = n.noise2d(0.5, 0.5)
assert -1 <= v <= 1
m = generate_map(10, 10, 0.1, 42)
assert len(m) == 10 and len(m[0]) == 10
a = to_ascii(m)
assert len(a) > 0
print("Noise tests passed")