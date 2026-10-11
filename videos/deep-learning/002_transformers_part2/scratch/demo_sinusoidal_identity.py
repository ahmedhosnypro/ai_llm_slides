import numpy as np

def sinusoidal_position_encoding(pos, d):
    """Compute sinusoidal position encoding for position pos and dimension d."""
    pe = np.zeros(d)
    for i in range(d // 2):
        omega = 1.0 / (10000 ** (2 * i / d))
        pe[2 * i] = np.sin(pos * omega)
        pe[2 * i + 1] = np.cos(pos * omega)
    return pe

def expand_using_identity(t, delta, d):
    """Compute PE(t+delta) using angle addition identity from PE(t) and PE(delta)."""
    pe_t = sinusoidal_position_encoding(t, d)
    pe_delta = sinusoidal_position_encoding(delta, d)
    pe_t_delta = np.zeros(d)
    for i in range(d // 2):
        omega = 1.0 / (10000 ** (2 * i / d))
        sin_t = np.sin(t * omega)
        cos_t = np.cos(t * omega)
        sin_delta = np.sin(delta * omega)
        cos_delta = np.cos(delta * omega)
        # sin((t+delta)*omega) = sin(t)*cos(delta) + cos(t)*sin(delta)
        pe_t_delta[2 * i] = sin_t * cos_delta + cos_t * sin_delta
        # cos((t+delta)*omega) = cos(t)*cos(delta) - sin(t)*sin(delta)
        pe_t_delta[2 * i + 1] = cos_t * cos_delta - sin_t * sin_delta
    return pe_t_delta

# Example usage
d = 512
t = 10
delta = 5

pe_direct = sinusoidal_position_encoding(t + delta, d)
pe_via_identity = expand_using_identity(t, delta, d)

print("Direct PE(t+delta):")
print(pe_direct[:10])  # show first 10 dimensions
print("\nPE via identity:")
print(pe_via_identity[:10])
print("\nDifference (should be near zero):")
print(np.max(np.abs(pe_direct - pe_via_identity)))

# Also show the identity for a single dimension
i = 0
omega = 1.0 / (10000 ** (2 * i / d))
print(f"\nFor dimension pair {i}:")
print(f"omega = {omega}")
print(f"sin((t+delta)*omega) = {np.sin((t+delta)*omega)}")
print(f"sin(t*omega)*cos(delta*omega) + cos(t*omega)*sin(delta*omega) = {np.sin(t*omega)*np.cos(delta*omega) + np.cos(t*omega)*np.sin(delta*omega)}")
print(f"cos((t+delta)*omega) = {np.cos((t+delta)*omega)}")
print(f"cos(t*omega)*cos(delta*omega) - sin(t*omega)*sin(delta*omega) = {np.cos(t*omega)*np.cos(delta*omega) - np.sin(t*omega)*np.sin(delta*omega)}")
