# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 22:37:45 2026

@author: Laszlo
"""

import numpy as np
from collections import Counter
import math
from Ulam_Spiral_in_DVFM import UlamSpiral




def load_primes_from_csv(path):
    primes = set()
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                primes.add(int(line))
    return primes

PRIME_FILE = r"C:\Users\Laszlo\Documents\GitHub\Prim_Numb\PrimNumb.csv"

prime_set = load_primes_from_csv(PRIME_FILE)

def real_prime_density(moduli, N, prime_set):

    occupancy = Counter()
    prime_occ = Counter()

    for n in range(1, N+1):
        state = tuple(n % m for m in moduli)

        occupancy[state] += 1

        if n in prime_set:
            prime_occ[state] += 1

    densities = {}
    for state in occupancy:
        densities[state] = prime_occ[state] / occupancy[state]

    return densities

# -------- PRIME GENERATOR --------
def primes_up_to(n):
    sieve = np.ones(n+1, dtype=bool)
    sieve[:2] = False
    for i in range(2, int(n**0.5)+1):
        if sieve[i]:
            sieve[i*i:n+1:i] = False
    return np.where(sieve)[0]

# -------- SIEVE DENSITY --------
#def sieve_density(primes):
#   mu = 1.0
#   for p in primes:
#       mu *= (1 - 1/p)
#   return mu

# -------- EMPIRICAL MODULAR DENSITY --------
def empirical_density(moduli, N):
    occupancy = Counter()

    for n in range(1, N+1):
        state = tuple(n % m for m in moduli)
        occupancy[state] += 1

    densities = np.array(list(occupancy.values())) / N
    return densities

# -------- PRIME-COMPATIBLE STATES --------
def prime_compatible_density(moduli, N):
    primes = primes_up_to(max(moduli))

    count = 0
    for n in range(1, N+1):
        ok = True
        for p in primes:
            if n % p == 0:
                ok = False
                break
        if ok:
            count += 1

    return count / N

# ============================================================================
# 4. PRIME FIELD EXTENSION (mu, rho, potential)
# ============================================================================

def compute_rho(moduli, N, prime_db):
    total = Counter()
    prime = Counter()

    for n in range(1, N+1):
        state = tuple(n % m for m in moduli)
        total[state] += 1

        if prime_db.is_prime(n):
            prime[state] += 1

    rho = {}
    for s in total:
        rho[s] = prime[s] / total[s] if total[s] > 0 else 0

    return rho

import numpy as np

def compute_fft(rho_dict):
    """
    rho_dict: {state_index: rho_value}
    """
    # állapottér vektor
    states = sorted(rho_dict.keys())
    rho_vec = np.array([rho_dict[s] for s in states])

    fft_vals = np.fft.fft(rho_vec)
    freqs = np.fft.fftfreq(len(rho_vec))

    return freqs, fft_vals

def extract_top_frequencies(freqs, fft_vals, k=10):
    magnitudes = np.abs(fft_vals)

    idx = np.argsort(magnitudes)[-k:]  # top k
    return freqs[idx], fft_vals[idx]

def reconstruct_rho(states, freqs, fft_vals, M):
    reconstructed = []

    for x in range(len(states)):
        val = 0.0 + 0.0j

        for f, a in zip(freqs, fft_vals):
            val += a * np.exp(2j * np.pi * f * x)

        reconstructed.append(val.real)

    return np.array(reconstructed)

def normalize_rho(rho_vec):
    rho_vec = np.maximum(rho_vec, 0)  # negatív zaj levágása
    total = np.sum(rho_vec)

    if total > 0:
        rho_vec /= total

    return rho_vec

def compare_rho(original, reconstructed):
    error = np.mean(np.abs(original - reconstructed))
    print(f"Reconstruction error: {error}")

def sieve_mask(state):
    return 1 if all(r != 0 for r in state) else 0

def compute_potential(rho, eps=1e-12):
    import numpy as np
    return {s: -np.log(rho[s] + eps) for s in rho}

def compute_fourier_spectrum(rho):
    import numpy as np

    values = np.array(list(rho.values()))

    fft = np.fft.fft(values)
    freqs = np.fft.fftfreq(len(values))

    return freqs, np.abs(fft)

def ulam_with_rho(prime_db, moduli, rho, n_max=10000):

    spiral = UlamSpiral(prime_db)
    x, y, _ = spiral.generate_spiral(n_max)

    colors = []

    for n in range(1, n_max+1):
        state = tuple(n % m for m in moduli)
        val = rho.get(state, 0)
        colors.append(val)

    plt.figure(figsize=(8,8))
    plt.scatter(x, y, c=colors, s=2, cmap='inferno')

    plt.title("Ulam spiral colored by rho(x)")
    plt.colorbar(label="rho(x)")
    plt.gca().set_aspect('equal')
    plt.show()
    
    

# -------- MAIN VALIDATION --------
def validate(moduli, N=100000000):

    print(f"\nModuli: {moduli}")

    densities = empirical_density(moduli, N)

    print(f"Empirical mean density: {np.mean(densities)}")

    primes = primes_up_to(max(moduli))
#    mu_sieve = sieve_density(primes)

#    print(f"Sieve density: {mu_sieve}")

    mu_pc = prime_compatible_density(moduli, N)
    print(f"Empirical prime-compatible density: {mu_pc}")

    print("\nDifferences:")
#    print(f"|empirical - sieve| = {abs(mu_pc - mu_sieve)}")

# -------- RUN --------
validate([2,3,5,7,11,13], N=100000000)
validate([17,19], N=100000000)

import matplotlib.pyplot as plt

def plot_validation(moduli, N=100000000):

    densities = empirical_density(moduli, N)

    primes = primes_up_to(max(moduli))
#    mu_sieve = sieve_density(primes)
    mu_pc = prime_compatible_density(moduli, N)

    # Histogram of densities
    plt.figure(figsize=(10,5))

    plt.hist(densities, bins=30, alpha=0.7, label="Empirical μ(x)")

    # Vertical lines
    plt.axvline(mu_pc, color='red', linestyle='--', linewidth=2,
                label=f'Empirical prime-compatible = {mu_pc:.6f}')

#    plt.axvline(mu_sieve, color='green', linestyle='--', linewidth=2,
#                label=f'Sieve = {mu_sieve:.6f}')

    plt.title(f"Density Spectrum vs Sieve Prediction\nModuli={moduli}")
    plt.xlabel("μ(x)")
    plt.ylabel("Frequency")
    plt.legend()
    plt.grid(True)

    plt.show()


# RUN
plot_validation([2,3,5,7,11,13], N=100000000)
plot_validation([17,19], N=100000000)


def plot_prime_state_sum(moduli, N=100000000):

    occupancy = Counter()

    for n in range(1, N+1):
        state = tuple(n % m for m in moduli)
        occupancy[state] += 1

    densities = {s: c/N for s, c in occupancy.items()}

    primes = primes_up_to(max(moduli))

    # prime-compatible states
    pc_states = []
    for state in densities:
        ok = True
        for i, p in enumerate(moduli):
            if state[i] == 0:
                ok = False
                break
        if ok:
            pc_states.append(state)

    pc_sum = sum(densities[s] for s in pc_states)

    print(f"Sum over prime-compatible states: {pc_sum}")
    
def plot_real_prime_density(moduli, N, prime_set):

    densities = real_prime_density(moduli, N, prime_set)

    values = list(densities.values())

    plt.figure(figsize=(10,5))
    plt.hist(values, bins=30, alpha=0.7)

    plt.title(f"Real prime density per state\nModuli={moduli}")
    plt.xlabel("Prime density")
    plt.ylabel("Frequency")
    plt.grid(True)

    plt.show()
    
def plot_mass_comparison(moduli, N=100000):

    from collections import Counter
    import numpy as np
    import matplotlib.pyplot as plt

    occupancy = Counter()

    for n in range(1, N+1):
        state = tuple(n % m for m in moduli)
        occupancy[state] += 1

    densities = {s: c/N for s, c in occupancy.items()}

    # classify states
    allowed = []
    forbidden = []

    for s, mu in densities.items():
        if all(r != 0 for r in s):
            allowed.append(mu)
        else:
            forbidden.append(mu)

    print("Allowed sum:", sum(allowed))
    print("Forbidden sum:", sum(forbidden))

    plt.figure(figsize=(10,5))

    plt.hist(allowed, bins=20, alpha=0.7, label="Allowed states")
    plt.hist(forbidden, bins=20, alpha=0.7, label="Forbidden states")

    plt.title(f"State space partition\nModuli={moduli}")
    plt.xlabel("μ(x)")
    plt.ylabel("Frequency")
    plt.legend()
    plt.grid(True)

    plt.show()
    
def run_prime_field_analysis(moduli, N, prime_db):

    print("\n=== COMPUTING MU ===")
    mu = compute_mu(moduli, N)

    print("=== COMPUTING RHO ===")
    rho = compute_rho(moduli, N, prime_db)

    print("=== COMPUTING POTENTIAL ===")
    V = compute_potential(rho)

    print("=== FOURIER ANALYSIS ===")
    freqs, spec = compute_fourier_spectrum(rho)

    print("=== ULAM VISUALIZATION ===")
    ulam_with_rho(prime_db, moduli, rho, n_max=10000)

    # Fourier plot
    import matplotlib.pyplot as plt
    plt.figure()
    plt.plot(freqs, spec)
    plt.title("Fourier spectrum of rho(x)")
    plt.xlabel("Frequency")
    plt.ylabel("Amplitude")
    plt.show()
    
    # === FOURIER RECONSTRUCTION ===

    states = sorted(rho.keys())
    rho_vec = np.array([rho[s] for s in states])
    
    freqs, fft_vals = compute_fft(rho)
    
    top_freqs, top_vals = extract_top_frequencies(freqs, fft_vals, k=20)
    
    rho_recon = reconstruct_rho(states, top_freqs, top_vals, M=len(states))
    rho_recon = normalize_rho(rho_recon)
    
    compare_rho(rho_vec, rho_recon)

    return mu, rho, V

# ============================================================================
# PRIME FIELD EXTENSION
# ============================================================================

def compute_mu(moduli, N):
    occ = Counter()

    for n in range(1, N+1):
        state = tuple(n % m for m in moduli)
        occ[state] += 1

    return {s: c/N for s, c in occ.items()}


def compute_rho(moduli, N, prime_db):
    total = Counter()
    prime = Counter()

    for n in range(1, N+1):
        state = tuple(n % m for m in moduli)
        total[state] += 1

        if prime_db.is_prime(n):
            prime[state] += 1

    rho = {}
    for s in total:
        rho[s] = prime[s] / total[s] if total[s] > 0 else 0

    return rho


def sieve_mask(state):
    return 1 if all(r != 0 for r in state) else 0


def compute_potential(rho, eps=1e-12):
    return {s: -np.log(rho[s] + eps) for s in rho}


def compute_fourier_spectrum(rho):
    values = np.array(list(rho.values()))
    fft = np.fft.fft(values)
    freqs = np.fft.fftfreq(len(values))
    return freqs, np.abs(fft)


def ulam_with_rho(prime_db, moduli, rho, n_max=10000):

    spiral = UlamSpiral(prime_db)
    x, y, _ = spiral.generate_spiral(n_max)

    colors = []

    for n in range(1, n_max+1):
        state = tuple(n % m for m in moduli)
        val = rho.get(state, 0)
        colors.append(val)

    plt.figure(figsize=(8,8))
    plt.scatter(x, y, c=colors, s=2, cmap='inferno')

    plt.title("Ulam spiral colored by rho(x)")
    plt.colorbar(label="rho(x)")
    plt.gca().set_aspect('equal')
    plt.show()


def run_prime_field_analysis(moduli, N, prime_db):

    print("\n=== COMPUTING MU ===")
    mu = compute_mu(moduli, N)

    print("=== COMPUTING RHO ===")
    rho = compute_rho(moduli, N, prime_db)

    print("=== COMPUTING POTENTIAL ===")
    V = compute_potential(rho)

    print("=== TOP STATES ===")
    sorted_rho = sorted(rho.items(), key=lambda x: x[1], reverse=True)
    for s, v in sorted_rho[:10]:
        print(s, v)

    # === FOURIER RECONSTRUCTION ===

    states = sorted(rho.keys())
    rho_vec = np.array([rho[s] for s in states])
    
    freqs, fft_vals = compute_fft(rho)
    top_freqs, top_vals = extract_top_frequencies(freqs, fft_vals, k=20)
    
    rho_recon = reconstruct_rho(states, top_freqs, top_vals, M=len(states))
    rho_recon = normalize_rho(rho_recon)
    
    compare_rho(rho_vec, rho_recon)
    
    # === VISUALIZATION ===
    import matplotlib.pyplot as plt
    
    plt.figure(figsize=(10,5))
    
    plt.plot(rho_vec, label="Original ρ(x)", linewidth=2)
    plt.plot(rho_recon, label="Reconstructed ρ(x)", linestyle="--")
    
    plt.legend()
    plt.title("ρ(x) vs Fourier Reconstruction")
    plt.xlabel("State index")
    plt.ylabel("Density")
    
    plt.grid(True)
    plt.show()

    print("=== POTENTIAL HIST ===")
    vals = list(V.values())

    plt.figure()
    plt.hist(vals, bins=30)
    plt.title("Potential V(x)")
    plt.show()

    print("=== ULAM ===")
    ulam_with_rho(prime_db, moduli, rho, n_max=10000)
    
    

    return mu, rho, V


    
from primspace_core_engine_v3_1 import PrimeDatabase    
def main():

    prime_db = PrimeDatabase()

    moduli = [2,3,5,7,11,13]

    # EZ AZ ÚJ RÉSZ
    run_prime_field_analysis(moduli, N=100000000, prime_db=prime_db)

    print("=== VALIDATION ===")  
    validate([2,3,5,7,11,13], N=100000000)
    validate([17,19], N=100000000)

    print("\n=== BASIC PLOTS ===")
    plot_validation([2,3,5,7,11,13], N=100000000)
    plot_validation([17,19], N=100000000)

    print("\n=== MASS CHECK ===")
    plot_mass_comparison([2,3,5,7,11,13], N=100000000)
    plot_mass_comparison([17,19], N=100000000)

    print("\n=== REAL PRIME DENSITY ===")
    plot_real_prime_density([2,3,5,7,11,13], 100000000, prime_set)
    plot_real_prime_density([17,19], 100000000, prime_set)
    
    


if __name__ == "__main__":
    main()