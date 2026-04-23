#!/usr/bin/env python3
"""
Primspace Core Engine v3.0 - Fixed Syntax
Using 1,000,000 prime database from CSV
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Optional, Set
from pathlib import Path

# ============================================================================
# 0. CONFIGURATION
# ============================================================================

PRIME_CSV_PATH = Path(r"C:\Users\Laszlo\Documents\GitHub\Prim_Numb\PrimNumb.csv")

# ============================================================================
# 1. PRIME DATABASE LOADER
# ============================================================================

class PrimeDatabase:
    """Loads and manages prime numbers from CSV file."""
    
    def __init__(self, csv_path: Path = PRIME_CSV_PATH):
        self.csv_path = csv_path
        self.primes = []
        self.prime_set: Set[int] = set()
        self.max_prime = 0
        self._load_from_csv()
        
    def _load_from_csv(self):
        """Load primes from CSV file (one prime per line)"""
        if not self.csv_path.exists():
            print(f"Warning: Prime file not found at {self.csv_path}")
            print("Falling back to sieve generation...")
            self._generate_sieve(1000000)
            return
            
        print(f"Loading primes from {self.csv_path}...")
        with open(self.csv_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and line.isdigit():
                    p = int(line)
                    self.primes.append(p)
                    self.prime_set.add(p)
        
        self.max_prime = max(self.primes) if self.primes else 0
        print(f"Loaded {len(self.primes):,} primes (max: {self.max_prime:,})")
        
    def _generate_sieve(self, limit: int):
        """Fallback: generate primes using sieve"""
        sieve = np.ones(limit + 1, dtype=bool)
        sieve[:2] = False
        for i in range(2, int(limit**0.5) + 1):
            if sieve[i]:
                sieve[i*i:limit+1:i] = False
        self.primes = np.where(sieve)[0].tolist()
        self.prime_set = set(self.primes)
        self.max_prime = limit
        print(f"Generated {len(self.primes):,} primes via sieve (up to {limit:,})")
    
    def is_prime(self, n: int) -> bool:
        """O(1) primality test for n <= max_prime"""
        if n <= self.max_prime:
            return n in self.prime_set
        if n < 2:
            return False
        if n % 2 == 0:
            return n == 2
        limit = int(n**0.5) + 1
        for p in self.primes:
            if p > limit:
                break
            if n % p == 0:
                return False
        return True
    
    def get_primes_up_to(self, limit: int) -> List[int]:
        """Return all primes <= limit"""
        if limit >= self.max_prime:
            return self.primes.copy()
        # Binary search for the cutoff
        lo, hi = 0, len(self.primes)
        while lo < hi:
            mid = (lo + hi) // 2
            if self.primes[mid] <= limit:
                lo = mid + 1
            else:
                hi = mid
        return self.primes[:lo]


# ============================================================================
# 2. CORE CLASSES
# ============================================================================

class ModularSpiral:
    """Φ_k(n) = (n mod p_1, ..., n mod p_k)"""
    
    def __init__(self, moduli: List[int]):
        self.moduli = np.array(moduli)
        self.k = len(moduli)
        self.period = np.prod(moduli)
        
    def map_number(self, n: int) -> np.ndarray:
        return np.array([n % m for m in self.moduli])
    
    def trajectory(self, n_start: int = 0, n_steps: int = None) -> np.ndarray:
        if n_steps is None:
            n_steps = min(self.period * 2, 10000)
        points = []
        for n in range(n_start, n_start + n_steps):
            points.append(self.map_number(n))
        return np.array(points)
    
    def to_2d_projection(self, points: np.ndarray, dim1: int = 0, dim2: int = 1):
        return points[:, dim1], points[:, dim2]


class ResidualDensity:
    """α_k(n) = (1/k) Σ (n mod p_i)/(p_i - 1)"""
    
    def __init__(self, moduli: List[int]):
        self.moduli = np.array(moduli)
        self.k = len(moduli)
        self.max_residues = np.array(moduli) - 1
        
    def compute(self, n: int) -> float:
        residues = np.array([n % m for m in self.moduli])
        normalized = residues / self.max_residues
        return float(np.mean(normalized))
    
    def compute_batch(self, n_values: np.ndarray) -> np.ndarray:
        result = np.zeros(len(n_values))
        for i, n in enumerate(n_values):
            result[i] = self.compute(n)
        return result


class KAPVDecomposer:
    """K-APV: Minimal additive prime decomposition"""
    
    def __init__(self, prime_db: PrimeDatabase):
        self.prime_db = prime_db
        self.primes = prime_db.primes
        self.cache = {}
        
    def compute(self, n: int) -> List[int]:
        if n in self.cache:
            return self.cache[n]
        
        if n == 1:
            return [1]
        if self.prime_db.is_prime(n):
            return [n]
        
        result = []
        remaining = n
        
        while remaining > 0:
            found = False
            for p in reversed(self.primes):
                if p <= remaining:
                    result.append(p)
                    remaining -= p
                    found = True
                    break
            if not found:
                result.append(1)
                remaining -= 1
        
        result.sort()
        self.cache[n] = result
        return result
    
    def cardinality(self, n: int) -> int:
        if n == 1:
            return 1
        if self.prime_db.is_prime(n):
            return 1
        if n > 10000:
            # Approximation for large n
            return n // self.primes[-1] + 2
        return len(self.compute(n))


# ============================================================================
# 3. VISUALIZATIONS
# ============================================================================

def create_multi_layer_visualization(
    moduli: Tuple[int, ...] = (2, 3, 5, 7),
    n_max: int = 500,
    prime_db: PrimeDatabase = None,
    output_file: str = None
) -> plt.Figure:
    """Four-panel Primspace visualization"""
    
    if prime_db is None:
        prime_db = PrimeDatabase()
    
    moduli_list = list(moduli)
    spiral = ModularSpiral(moduli_list)
    density = ResidualDensity(moduli_list)
    kapv = KAPVDecomposer(prime_db)
    
    # Precompute for all n
    n_range = np.arange(1, n_max + 1)
    alpha_vals = np.array([density.compute(n) for n in n_range])
    kapv_cards = np.array([kapv.cardinality(n) for n in n_range])
    is_prime_arr = np.array([prime_db.is_prime(n) for n in n_range])
    
    # Trajectory for 2D projection
    points = spiral.trajectory(n_start=1, n_steps=n_max)
    x, y = spiral.to_2d_projection(points)
    
    # Create figure
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Panel 1: Modular braid
    ax1 = axes[0, 0]
    colors = ['red' if is_prime_arr[i] else 'steelblue' for i in range(n_max)]
    ax1.scatter(x, y, c=colors, s=20, alpha=0.7, edgecolors='black', linewidth=0.2)
    ax1.plot(x, y, 'k-', alpha=0.1, linewidth=0.3)
    ax1.set_title(f'Layer 1: Modular Braid\nM = {moduli}', fontsize=12, fontweight='bold')
    ax1.set_xlabel(f'n mod {moduli[0]}')
    ax1.set_ylabel(f'n mod {moduli[1]}')
    ax1.grid(True, alpha=0.3)
    
    # Panel 2: Residual density
    ax2 = axes[0, 1]
    prime_indices = np.where(is_prime_arr)[0] + 1
    prime_alphas = alpha_vals[is_prime_arr]
    
    ax2.plot(n_range, alpha_vals, 'b-', alpha=0.5, linewidth=1)
    ax2.scatter(prime_indices, prime_alphas, c='red', s=15, alpha=0.8, label='Primes')
    ax2.axhline(y=0.6, color='green', linestyle='--', alpha=0.5, label='Threshold α=0.6')
    ax2.set_title(f'Layer 2: Residual Density α_k(n)\nk={len(moduli)}', fontsize=12, fontweight='bold')
    ax2.set_xlabel('n')
    ax2.set_ylabel('α_k(n)')
    ax2.set_ylim(-0.05, 1.05)
    ax2.legend(loc='upper right', fontsize=9)
    ax2.grid(True, alpha=0.3)
    
    # Panel 3: K-APV cardinality
    ax3 = axes[1, 0]
    bar_colors = ['red' if is_prime_arr[i] else 'steelblue' for i in range(n_max)]
    ax3.bar(n_range, kapv_cards, color=bar_colors, alpha=0.7, width=0.8)
    ax3.axhline(y=1, color='darkred', linestyle='--', alpha=0.7, label='|K-APV| = 1 (prime)')
    ax3.set_title(f'Layer 3: K-APV Cardinality\nAdditive Complexity', fontsize=12, fontweight='bold')
    ax3.set_xlabel('n')
    ax3.set_ylabel('|K-APV(n)|')
    ax3.legend(loc='upper right', fontsize=9)
    ax3.grid(True, alpha=0.3, axis='y')
    
    # Panel 4: Prime density histogram
    ax4 = axes[1, 1]
    bins = np.linspace(0, 1, 21)
    prime_hist, _ = np.histogram(prime_alphas, bins=bins, density=True)
    composite_alphas = alpha_vals[~is_prime_arr]
    comp_hist, _ = np.histogram(composite_alphas, bins=bins, density=True)
    
    x_bins = (bins[:-1] + bins[1:]) / 2
    width = bins[1] - bins[0]
    ax4.bar(x_bins - width/4, prime_hist, width=width/2, alpha=0.7, color='red', label='Primes')
    ax4.bar(x_bins + width/4, comp_hist, width=width/2, alpha=0.7, color='steelblue', label='Composites')
    ax4.set_title(f'Distribution of α_k(n)\nPrimes vs Composites', fontsize=12, fontweight='bold')
    ax4.set_xlabel('α_k(n)')
    ax4.set_ylabel('Density')
    ax4.legend(loc='upper left', fontsize=9)
    ax4.grid(True, alpha=0.3)
    
    plt.suptitle(f'Primspace Unified Framework | n=1..{n_max} | {len(prime_db.primes):,} primes loaded',
                 fontsize=13, fontweight='bold')
    plt.tight_layout()
    
    # Add statistics text
    prime_ratio_high = np.mean(prime_alphas > 0.6) if len(prime_alphas) > 0 else 0
    comp_ratio_high = np.mean(composite_alphas > 0.6) if len(composite_alphas) > 0 else 0
    stats_text = f"Primes with α_k>0.6: {prime_ratio_high:.1%} | Composites with α_k>0.6: {comp_ratio_high:.1%}"
    fig.text(0.5, 0.02, stats_text, ha='center', fontsize=10, style='italic')
    
    if output_file:
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        print(f"Saved: {output_file}")
    
    return fig


def analyze_prime_distribution(prime_db: PrimeDatabase = None, n_max: int = 100000):
    """Statistical analysis of prime distribution"""
    
    if prime_db is None:
        prime_db = PrimeDatabase()
    
    primes = prime_db.get_primes_up_to(n_max)
    n_primes = len(primes)
    
    print("=" * 70)
    print("PRIME DISTRIBUTION ANALYSIS (from CSV database)")
    print("=" * 70)
    print(f"Total primes in database: {len(prime_db.primes):,}")
    print(f"Max prime in database: {prime_db.max_prime:,}")
    print(f"Analyzing up to n={n_max:,}")
    print(f"Primes in range: {n_primes:,}")
    print()
    
    # Prime gaps
    gaps = [primes[i] - primes[i-1] for i in range(1, len(primes))]
    
    print("Prime Gap Statistics:")
    print(f"  Mean gap: {np.mean(gaps):.2f}")
    print(f"  Median gap: {np.median(gaps):.2f}")
    print(f"  Max gap: {max(gaps)}")
    print(f"  Min gap: {min(gaps)}")
    print()
    
    # Twin primes count - FIXED SYNTAX
    twin_count = 0
    for i in range(len(primes) - 1):
        if primes[i+1] == primes[i] + 2:
            twin_count += 1
    print(f"Twin primes (p, p+2) up to {n_max}: {twin_count:,}")
    
    # Prime number theorem approximation
    expected = n_max / np.log(n_max)
    print(f"\nPrime Number Theorem comparison:")
    print(f"  Actual π({n_max}): {n_primes:,}")
    print(f"  Expected n/log(n): {expected:.0f}")
    print(f"  Ratio (actual/expected): {n_primes/expected:.4f}")
    
    return primes, gaps


def create_twin_prime_visualization(
    moduli: Tuple[int, ...] = (2, 3, 5, 7),
    n_max: int = 1000,
    prime_db: PrimeDatabase = None,
    output_file: str = None
) -> plt.Figure:
    """Enhanced twin prime visualization"""
    
    if prime_db is None:
        prime_db = PrimeDatabase()
    
    density = ResidualDensity(list(moduli))
    
    # Find twin primes up to n_max
    primes = prime_db.get_primes_up_to(n_max)
    twin_pairs = []
    for i in range(len(primes) - 1):
        if primes[i+1] == primes[i] + 2:
            twin_pairs.append((primes[i], primes[i+1]))
    
    print(f"Found {len(twin_pairs)} twin prime pairs up to n={n_max}")
    
    if not twin_pairs:
        print("No twin primes found")
        return None
    
    # Show first 6 twin pairs
    n_plots = min(len(twin_pairs), 6)
    fig, axes = plt.subplots(n_plots, 1, figsize=(12, 3 * n_plots))
    if n_plots == 1:
        axes = [axes]
    
    for idx, (p1, p2) in enumerate(twin_pairs[:n_plots]):
        ax = axes[idx]
        n_range = range(max(1, p1 - 10), min(n_max, p2 + 10))
        alpha_vals = [density.compute(n) for n in n_range]
        
        ax.plot(list(n_range), alpha_vals, 'b-o', markersize=3, linewidth=1, alpha=0.7)
        
        # Highlight twin primes
        ax.scatter([p1, p2], [density.compute(p1), density.compute(p2)], 
                  c='red', s=100, marker='*', zorder=5, label=f'Twin primes ({p1}, {p2})')
        
        # Highlight gap
        gap = p1 + 1
        alpha_gap = density.compute(gap)
        alpha_avg = (density.compute(p1) + density.compute(p2)) / 2
        drop = alpha_avg - alpha_gap
        
        ax.scatter([gap], [alpha_gap], c='orange', s=80, marker='X', zorder=4, label=f'Gap (drop={drop:.3f})')
        
        ax.set_title(f'Twin Prime Pair ({p1}, {p2}) | α_k drop: {drop:.3f}', fontsize=11)
        ax.set_xlabel('n')
        ax.set_ylabel('α_k(n)')
        ax.set_ylim(0, 1)
        ax.legend(loc='upper right', fontsize=8)
        ax.grid(True, alpha=0.3)
    
    plt.suptitle(f'Twin Prime Gap Signature | k={len(moduli)} | n≤{n_max}', 
                 fontsize=13, fontweight='bold')
    plt.tight_layout()
    
    if output_file:
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        print(f"Saved: {output_file}")
    
    return fig


# ============================================================================
# 4. MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("PRIMSPACE CORE ENGINE v3.0")
    print("Using prime database from CSV")
    print("=" * 70)
    
    # Load the prime database
    prime_db = PrimeDatabase()
    
    # Analysis 1: Prime distribution statistics
    print("\n" + "-" * 50)
    analyze_prime_distribution(prime_db, n_max=100000)
    
    # Visualization 1: Multi-layer view
    print("\n" + "-" * 50)
    print("Creating multi-layer visualization...")
    fig1 = create_multi_layer_visualization(
        moduli=(2, 3, 5, 7),
        n_max=500,
        prime_db=prime_db,
        output_file="primspace_multilayer.png"
    )
    
    # Visualization 2: Twin prime analysis
    print("\n" + "-" * 50)
    print("Creating twin prime visualization...")
    fig2 = create_twin_prime_visualization(
        moduli=(2, 3, 5, 7),
        n_max=1000,
        prime_db=prime_db,
        output_file="primspace_twin_primes.png"
    )
    
    print("\n" + "=" * 70)
    print("All visualizations completed!")
    print("Files saved:")
    print("  - primspace_multilayer.png")
    print("  - primspace_twin_primes.png")
    print("=" * 70)
    
    plt.show()