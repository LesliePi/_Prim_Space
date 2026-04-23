#!/usr/bin/env python3
"""
Primspace Model - Computational Examples
Demonstrates DVFM, K-APV, and residual density calculations
"""

import numpy as np
from typing import List, Tuple, Set
from collections import Counter

def is_prime(n: int) -> bool:
    """Standard primality test."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def get_primes(k: int) -> List[int]:
    """Get first k primes."""
    primes = []
    n = 2
    while len(primes) < k:
        if is_prime(n):
            primes.append(n)
        n += 1
    return primes

def compute_mod_k(n: int, primes: List[int]) -> Tuple[int, ...]:
    """Compute modality map Mod_k(n)."""
    return tuple(n % p for p in primes)

def compute_alpha_k(n: int, primes: List[int]) -> float:
    """Compute residual density α_k(n)."""
    k = len(primes)
    residues = [n % p for p in primes]
    normalized = [r / (p - 1) for r, p in zip(residues, primes)]
    return sum(normalized) / k

def compute_kapv_greedy(n: int, max_prime: int = 100) -> List[int]:
    """
    Compute K-APV using greedy algorithm.
    Start with n, repeatedly subtract largest prime ≤ remaining value.
    """
    if n == 1:
        return [1]
    
    primes = [p for p in range(2, max_prime + 1) if is_prime(p)]
    
    result = []
    remaining = n
    
    while remaining > 0:
        # Find largest prime ≤ remaining
        found = False
        for p in reversed(primes):
            if p <= remaining:
                result.append(p)
                remaining -= p
                found = True
                break
        
        if not found:
            # If no prime found, use 1
            result.append(1)
            remaining -= 1
    
    result.sort()
    return result

def format_state(n: int, primes: List[int]) -> str:
    """Format complete state S_k(n)."""
    mod_k = compute_mod_k(n, primes)
    kapv = compute_kapv_greedy(n)
    alpha = compute_alpha_k(n, primes)
    is_p = "PRIME" if is_prime(n) else ""
    
    return f"n={n:3d} | Mod_k={mod_k} | K-APV={kapv} | α_k={alpha:.3f} | {is_p}"

def example_1_small_range():
    """Example 1: Small range n=1..20 with k=3."""
    print("=" * 80)
    print("EXAMPLE 1: Small Range (n=1..20, k=3)")
    print("=" * 80)
    print()
    
    k = 3
    primes = get_primes(k)
    print(f"Using first {k} primes: {primes}")
    print()
    
    print("State evolution:")
    print("-" * 80)
    for n in range(1, 21):
        print(format_state(n, primes))
    print()

def example_2_prime_detection():
    """Example 2: How well does α_k correlate with primality?"""
    print("=" * 80)
    print("EXAMPLE 2: Prime Detection via Residual Density")
    print("=" * 80)
    print()
    
    k = 4
    primes = get_primes(k)
    n_max = 200
    
    prime_alphas = []
    composite_alphas = []
    
    for n in range(2, n_max + 1):
        alpha = compute_alpha_k(n, primes)
        if is_prime(n):
            prime_alphas.append(alpha)
        else:
            composite_alphas.append(alpha)
    
    print(f"Using k={k} primes: {primes}")
    print(f"Range: n=2..{n_max}")
    print()
    
    print("Statistics:")
    print(f"  Primes:")
    print(f"    Count: {len(prime_alphas)}")
    print(f"    Mean α_k: {np.mean(prime_alphas):.4f}")
    print(f"    Std α_k:  {np.std(prime_alphas):.4f}")
    print(f"    Min α_k:  {np.min(prime_alphas):.4f}")
    print(f"    Max α_k:  {np.max(prime_alphas):.4f}")
    print()
    print(f"  Composites:")
    print(f"    Count: {len(composite_alphas)}")
    print(f"    Mean α_k: {np.mean(composite_alphas):.4f}")
    print(f"    Std α_k:  {np.std(composite_alphas):.4f}")
    print(f"    Min α_k:  {np.min(composite_alphas):.4f}")
    print(f"    Max α_k:  {np.max(composite_alphas):.4f}")
    print()
    
    # Threshold analysis
    threshold = 0.6
    primes_above = sum(1 for a in prime_alphas if a > threshold)
    composites_above = sum(1 for a in composite_alphas if a > threshold)
    
    print(f"Threshold α_k > {threshold}:")
    print(f"  Primes:     {primes_above}/{len(prime_alphas)} ({100*primes_above/len(prime_alphas):.1f}%)")
    print(f"  Composites: {composites_above}/{len(composite_alphas)} ({100*composites_above/len(composite_alphas):.1f}%)")
    print()

def example_3_state_transitions():
    """Example 3: Detailed state transition examples."""
    print("=" * 80)
    print("EXAMPLE 3: State Transitions T_k")
    print("=" * 80)
    print()
    
    k = 3
    primes = get_primes(k)
    
    # Interesting transitions
    transitions = [
        (6, 7),   # Composite to prime
        (7, 8),   # Prime to composite
        (10, 11), # Composite to prime
        (12, 13), # Composite to prime
    ]
    
    print(f"Using k={k} primes: {primes}")
    print()
    
    for n1, n2 in transitions:
        print(f"Transition: {n1} → {n2}")
        print(f"  Before: {format_state(n1, primes)}")
        print(f"  After:  {format_state(n2, primes)}")
        
        # Compute gradient
        alpha1 = compute_alpha_k(n1, primes)
        alpha2 = compute_alpha_k(n2, primes)
        gradient = alpha2 - alpha1
        
        print(f"  Δα_k = {gradient:+.3f}")
        print()

def example_4_kapv_growth():
    """Example 4: K-APV cardinality growth."""
    print("=" * 80)
    print("EXAMPLE 4: K-APV Cardinality Growth")
    print("=" * 80)
    print()
    
    n_max = 200
    
    print(f"K-APV evolution (n=1..{n_max}):")
    print("-" * 80)
    
    for n in range(1, n_max + 1):
        kapv = compute_kapv_greedy(n)
        card = len(kapv)
        is_p = "P" if is_prime(n) else " "
        
        # Show full K-APV for primes and some interesting composites
        if is_prime(n) or n % 10 == 0:
            print(f"n={n:3d} [{is_p}] | |K-APV|={card} | K-APV={kapv}")
    
    print()
    
    # Statistics
    cardinalities = [len(compute_kapv_greedy(n)) for n in range(1, n_max + 1)]
    print("Cardinality statistics:")
    print(f"  Mean: {np.mean(cardinalities):.2f}")
    print(f"  Max:  {np.max(cardinalities)}")
    print(f"  Growth rate: ~log(n) [theoretical expectation]")
    print()

def example_5_twin_primes():
    """Example 5: Twin primes in state space."""
    print("=" * 80)
    print("EXAMPLE 5: Twin Primes in State Space")
    print("=" * 80)
    print()
    
    k = 4
    primes = get_primes(k)
    n_max = 200
    
    # Find twin primes
    twin_primes = []
    for n in range(2, n_max):
        if is_prime(n) and is_prime(n + 2):
            twin_primes.append((n, n + 2))
    
    print(f"Using k={k} primes: {primes}")
    print(f"Twin primes in range [2, {n_max}]:")
    print()
    
    for p1, p2 in twin_primes:
        print(f"Twin pair: ({p1}, {p2})")
        print(f"  {format_state(p1, primes)}")
        print(f"  {format_state(p2, primes)}")
        
        # Analyze the gap state (p1 + 1)
        gap_n = p1 + 1
        print(f"  Gap n={gap_n}: {format_state(gap_n, primes)}")
        print()

if __name__ == "__main__":
    example_1_small_range()
    print("\n" * 2)
    
    example_2_prime_detection()
    print("\n" * 2)
    
    example_3_state_transitions()
    print("\n" * 2)
    
    example_4_kapv_growth()
    print("\n" * 2)
    
    example_5_twin_primes()
    
    print("=" * 80)
    print("Examples completed.")
    print("=" * 80)
