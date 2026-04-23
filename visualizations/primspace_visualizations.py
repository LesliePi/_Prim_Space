#!/usr/bin/env python3
"""
Primspace Model - Visualizations
Creates the three-layer visualization scheme
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches

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

def get_primes(k: int):
    """Get first k primes."""
    primes = []
    n = 2
    while len(primes) < k:
        if is_prime(n):
            primes.append(n)
        n += 1
    return primes

def compute_mod_k(n: int, primes):
    """Compute modality map Mod_k(n)."""
    return tuple(n % p for p in primes)

def compute_alpha_k(n: int, primes):
    """Compute residual density α_k(n)."""
    k = len(primes)
    residues = [n % p for p in primes]
    normalized = [r / (p - 1) for r, p in zip(residues, primes)]
    return sum(normalized) / k

def compute_kapv_greedy(n: int, max_prime: int = 200):
    """Compute K-APV using greedy algorithm."""
    if n == 1:
        return [1]
    
    primes = [p for p in range(2, max_prime + 1) if is_prime(p)]
    
    result = []
    remaining = n
    
    while remaining > 0:
        found = False
        for p in reversed(primes):
            if p <= remaining:
                result.append(p)
                remaining -= p
                found = True
                break
        
        if not found:
            result.append(1)
            remaining -= 1
    
    result.sort()
    return result

def create_three_layer_visualization(n_max=100, k=4, output_file='primspace_viz'):
    """Create the complete three-layer Primspace visualization."""
    
    primes = get_primes(k)
    n_vals = list(range(1, n_max + 1))
    
    # Compute all states
    mod_vals = [compute_mod_k(n, primes) for n in n_vals]
    alpha_vals = [compute_alpha_k(n, primes) for n in n_vals]
    kapv_vals = [compute_kapv_greedy(n) for n in n_vals]
    kapv_cards = [len(kv) for kv in kapv_vals]
    
    # Identify primes
    prime_flags = [is_prime(n) for n in n_vals]
    prime_indices = [n for n in n_vals if is_prime(n)]
    prime_alphas = [alpha_vals[n-1] for n in prime_indices]
    
    # Create figure with three subplots
    fig, axes = plt.subplots(3, 1, figsize=(16, 12), sharex=True)
    fig.suptitle(f'Primspace Three-Layer Visualization (n=1..{n_max}, k={k})', 
                 fontsize=16, fontweight='bold')
    
    # === LAYER 1: Modular Braid (DVFM) ===
    ax1 = axes[0]
    
    colors = plt.cm.tab10(np.linspace(0, 1, k))
    for i, p in enumerate(primes):
        residues = [m[i] for m in mod_vals]
        ax1.plot(n_vals, residues, label=f'mod {p}', 
                color=colors[i], linewidth=1.5, alpha=0.7)
        
        # Mark primes with larger dots
        prime_residues = [m[i] for n, m in zip(n_vals, mod_vals) if is_prime(n)]
        prime_ns = [n for n in n_vals if is_prime(n)]
        ax1.scatter(prime_ns, prime_residues, color=colors[i], 
                   s=30, zorder=5, edgecolors='black', linewidth=0.5)
    
    ax1.set_ylabel('Residue', fontsize=12, fontweight='bold')
    ax1.set_title('Layer 1: Modular Braid (DVFM) - Multiplicative Coordinates', 
                  fontsize=13, fontweight='bold', pad=10)
    ax1.legend(loc='upper right', framealpha=0.9)
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(-0.5, max(primes) - 0.5)
    
    # === LAYER 2: Residual Density (Diffusion) ===
    ax2 = axes[1]
    
    # Color code by alpha value
    segments = []
    colors_alpha = []
    for i in range(len(n_vals) - 1):
        segments.append([(n_vals[i], alpha_vals[i]), (n_vals[i+1], alpha_vals[i+1])])
        colors_alpha.append(plt.cm.RdYlBu_r(alpha_vals[i]))
    
    # Plot line with gradient coloring
    ax2.plot(n_vals, alpha_vals, color='steelblue', linewidth=2, alpha=0.8)
    
    # Highlight primes with red dots
    ax2.scatter(prime_indices, prime_alphas, color='red', s=50, 
               label='Primes', zorder=5, edgecolors='darkred', linewidth=1)
    
    # Add threshold line
    threshold = 0.6
    ax2.axhline(y=threshold, color='green', linestyle='--', 
               linewidth=1.5, alpha=0.7, label=f'Threshold α={threshold}')
    
    ax2.set_ylabel('α_k(n)', fontsize=12, fontweight='bold')
    ax2.set_title('Layer 2: Residual Density - Diffusion-like Observable', 
                  fontsize=13, fontweight='bold', pad=10)
    ax2.legend(loc='upper right', framealpha=0.9)
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(-0.05, 1.05)
    
    # === LAYER 3: K-APV Structure (Additive) ===
    ax3 = axes[2]
    
    # Bar chart of cardinality
    bar_colors = ['green' if is_prime(n) else 'lightblue' for n in n_vals]
    ax3.bar(n_vals, kapv_cards, color=bar_colors, alpha=0.7, width=0.8)
    
    # Add horizontal line at cardinality = 1 (primes)
    ax3.axhline(y=1, color='red', linestyle='--', linewidth=1.5, 
               alpha=0.5, label='|K-APV|=1 (primes)')
    
    ax3.set_xlabel('n (Natural Number)', fontsize=12, fontweight='bold')
    ax3.set_ylabel('|K-APV(n)|', fontsize=12, fontweight='bold')
    ax3.set_title('Layer 3: K-APV Cardinality - Additive Complexity', 
                  fontsize=13, fontweight='bold', pad=10)
    ax3.legend(loc='upper right', framealpha=0.9)
    ax3.grid(True, alpha=0.3, axis='y')
    ax3.set_ylim(0, max(kapv_cards) + 0.5)
    
    # Custom legend for Layer 3
    prime_patch = mpatches.Patch(color='green', alpha=0.7, label='Prime numbers')
    composite_patch = mpatches.Patch(color='lightblue', alpha=0.7, label='Composite numbers')
    ax3.legend(handles=[prime_patch, composite_patch], loc='upper right', framealpha=0.9)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Saved: {output_file}")
    
    return fig

def create_alpha_histogram(n_max=100, k=4, output_file='alpha_histogram'):
    """Create histogram comparing α_k for primes vs composites."""
    
    primes = get_primes(k)
    
    prime_alphas = []
    composite_alphas = []
    
    for n in range(2, n_max + 1):
        alpha = compute_alpha_k(n, primes)
        if is_prime(n):
            prime_alphas.append(alpha)
        else:
            composite_alphas.append(alpha)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bins = np.linspace(0, 1, 30)
    ax.hist(composite_alphas, bins=bins, alpha=0.6, color='blue', 
            label=f'Composites (n={len(composite_alphas)})', density=True)
    ax.hist(prime_alphas, bins=bins, alpha=0.7, color='red', 
            label=f'Primes (n={len(prime_alphas)})', density=True)
    
    ax.axvline(x=0.6, color='green', linestyle='--', linewidth=2, 
              label='Threshold = 0.6')
    
    ax.set_xlabel('Residual Density α_k(n)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Probability Density', fontsize=12, fontweight='bold')
    ax.set_title(f'Distribution of α_k: Primes vs Composites (k={k}, n≤{n_max})', 
                fontsize=13, fontweight='bold')
    ax.legend(fontsize=11, framealpha=0.9)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Saved: {output_file}")
    
    return fig

def create_state_space_2d(n_max=100, k=2, output_file='state_space_2d'):
    """Create 2D projection of state space (when k=2)."""
    
    if k != 2:
        print("Warning: 2D state space visualization only works for k=2")
        return None
    
    primes = get_primes(k)
    p1, p2 = primes[0], primes[1]
    
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Create grid
    for n in range(1, n_max + 1):
        mod_k = compute_mod_k(n, primes)
        x, y = mod_k[0], mod_k[1]
        alpha = compute_alpha_k(n, primes)
        
        if is_prime(n):
            ax.scatter(x, y, s=200, c='red', marker='o', 
                      edgecolors='darkred', linewidth=2, 
                      alpha=0.8, zorder=5)
            ax.text(x, y, str(n), ha='center', va='center', 
                   fontsize=8, fontweight='bold', color='white')
        else:
            color = plt.cm.Blues(alpha)
            ax.scatter(x, y, s=150, c=[color], marker='s', 
                      edgecolors='black', linewidth=0.5, 
                      alpha=0.6, zorder=3)
            ax.text(x, y, str(n), ha='center', va='center', 
                   fontsize=7, color='black')
    
    ax.set_xlabel(f'Residue mod {p1}', fontsize=12, fontweight='bold')
    ax.set_ylabel(f'Residue mod {p2}', fontsize=12, fontweight='bold')
    ax.set_title(f'State Space Projection: Mod({p1}) × Mod({p2})', 
                fontsize=13, fontweight='bold')
    ax.set_xticks(range(p1))
    ax.set_yticks(range(p2))
    ax.grid(True, alpha=0.3)
    ax.set_xlim(-0.5, p1 - 0.5)
    ax.set_ylim(-0.5, p2 - 0.5)
    
    # Legend
    red_patch = mpatches.Patch(color='red', alpha=0.8, label='Prime numbers')
    blue_patch = mpatches.Patch(color='lightblue', alpha=0.6, label='Composites (darkness = α_k)')
    ax.legend(handles=[red_patch, blue_patch], loc='upper right', 
             fontsize=11, framealpha=0.9)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Saved: {output_file}")
    
    return fig

def create_twin_prime_analysis(n_max=100, k=4, output_file='twin_primes'):
    """Analyze twin primes in state space."""
    
    primes = get_primes(k)
    
    # Find twin primes
    twin_primes = []
    for n in range(2, n_max):
        if is_prime(n) and is_prime(n + 2):
            twin_primes.append((n, n + 2))
    
    if not twin_primes:
        print("No twin primes found in range")
        return None
    
    fig, axes = plt.subplots(len(twin_primes), 1, 
                            figsize=(12, 3 * len(twin_primes)),
                            squeeze=False)
    
    for idx, (p1, p2) in enumerate(twin_primes):
        ax = axes[idx, 0]
        
        # Plot α_k in neighborhood
        neighborhood = range(max(1, p1 - 5), min(n_max, p2 + 6))
        alphas = [compute_alpha_k(n, primes) for n in neighborhood]
        
        ax.plot(list(neighborhood), alphas, 'o-', linewidth=2, 
               markersize=6, color='steelblue', alpha=0.7)
        
        # Highlight the twin primes
        ax.scatter([p1, p2], 
                  [compute_alpha_k(p1, primes), compute_alpha_k(p2, primes)],
                  s=200, color='red', marker='*', 
                  edgecolors='darkred', linewidth=2, zorder=5,
                  label=f'Twin primes: ({p1}, {p2})')
        
        # Highlight the gap
        gap_n = p1 + 1
        ax.scatter([gap_n], [compute_alpha_k(gap_n, primes)],
                  s=150, color='orange', marker='X', 
                  edgecolors='darkorange', linewidth=2, zorder=4,
                  label=f'Gap at n={gap_n}')
        
        ax.set_xlabel('n', fontsize=11, fontweight='bold')
        ax.set_ylabel('α_k(n)', fontsize=11, fontweight='bold')
        ax.set_title(f'Twin Prime Pair: ({p1}, {p2})', 
                    fontsize=12, fontweight='bold')
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 1)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Saved: {output_file}")
    
    return fig

if __name__ == "__main__":
    print("Creating Primspace visualizations...")
    print()
    
    # Main three-layer visualization
    print("1. Three-layer visualization (n=1..100, k=4)...")
    create_three_layer_visualization(n_max=100, k=4, 
                                    output_file='primspace_threelayer.png')
    print()
    
    # Alpha histogram
    print("2. Alpha distribution histogram...")
    create_alpha_histogram(n_max=100, k=4, 
                          output_file='primspace_alpha_hist.png')
    print()
    
    # 2D state space
    print("3. 2D state space projection (k=2)...")
    create_state_space_2d(n_max=30, k=2, 
                         output_file='primspace_2d_statespace.png')
    print()
    
    # Twin prime analysis
    print("4. Twin prime analysis...")
    create_twin_prime_analysis(n_max=100, k=4, 
                              output_file='primspace_twin_primes.png')
    print()
    
    print("=" * 80)
    print("All visualizations completed!")
    print("=" * 80)