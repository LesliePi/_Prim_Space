# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 22:08:47 2026

@author: Laszlo
"""

#!/usr/bin/env python3
"""
Ulam Spiral in DVFM / Fonat-Taometria Framework
Unified representation of prime patterns in spiral coordinates
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Optional
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
        self.prime_set = set()
        self.max_prime = 0
        self._load_from_csv()
        
    def _load_from_csv(self):
        if not self.csv_path.exists():
            print(f"Warning: Prime file not found at {self.csv_path}")
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
    
    def is_prime(self, n: int) -> bool:
        return n in self.prime_set if n <= self.max_prime else False


# ============================================================================
# 2. ULAM SPIRAL IMPLEMENTATION (DVFM compatible)
# ============================================================================

class UlamSpiral:
    """
    Ulam spiral implementation with DVFM/Fonat-Taometria interpretation.
    
    The spiral is a 2D projection of the modular state space:
    - Each natural number n maps to a unique (x,y) coordinate
    - The mapping follows a square spiral pattern
    - Primes appear as singularities in this projection
    """
    
    def __init__(self, prime_db: PrimeDatabase):
        self.prime_db = prime_db
        
    def get_coordinates(self, n: int) -> Tuple[int, int]:
        """
        Convert number n to (x,y) coordinates in Ulam spiral.
        
        Algorithm: Square spiral starting at (0,0) for n=1
        Pattern: right, up, left, left, down, down, right, right, right, ...
        """
        if n == 1:
            return (0, 0)
        
        # Find which ring (layer) the number is in
        # Ring k contains numbers from (2k-1)^2+1 to (2k+1)^2
        k = int(np.ceil((np.sqrt(n) - 1) / 2))
        
        # Bottom-right corner of ring k
        corner = (2 * k + 1) ** 2
        
        # Side length of ring
        side = 2 * k
        
        # Distance from corner
        dist = corner - n
        
        # Determine which side
        if dist < side:
            # Bottom side: moving left
            x = k - dist
            y = -k
        elif dist < 2 * side:
            # Left side: moving up
            x = -k
            y = -k + (dist - side)
        elif dist < 3 * side:
            # Top side: moving right
            x = -k + (dist - 2 * side)
            y = k
        else:
            # Right side: moving down
            x = k
            y = k - (dist - 3 * side)
        
        return (x, y)
    
    def generate_spiral(self, n_max: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Generate Ulam spiral coordinates for numbers 1..n_max.
        
        Returns:
            x: array of x-coordinates
            y: array of y-coordinates
            is_prime: boolean array indicating primality
        """
        n_values = np.arange(1, n_max + 1)
        coords = [self.get_coordinates(n) for n in n_values]
        x = np.array([c[0] for c in coords])
        y = np.array([c[1] for c in coords])
        is_prime = np.array([self.prime_db.is_prime(n) for n in n_values])
        
        return x, y, is_prime
    
    def get_prime_positions(self, n_max: int) -> Tuple[List[int], List[int], List[int]]:
        """Get coordinates of primes only"""
        x, y, is_prime = self.generate_spiral(n_max)
        prime_indices = np.where(is_prime)[0]
        return prime_indices + 1, x[is_prime], y[is_prime]


# ============================================================================
# 3. DVFM INTERPRETATION OF ULAM SPIRAL
# ============================================================================

class DVFMUlamInterpreter:
    """
    Interprets Ulam spiral patterns in terms of DVFM (Discrete Vector Field Method).
    
    In DVFM terms:
    - The Ulam spiral is a 2D projection of the modular embedding Phi_k(n)
    - Primes are singularities where the vector field vanishes
    - Diagonals correspond to arithmetic progressions modulo certain numbers
    """
    
    def __init__(self, prime_db: PrimeDatabase):
        self.prime_db = prime_db
        self.spiral = UlamSpiral(prime_db)
    
    def analyze_diagonals(self, n_max: int = 10000):
        """
        Analyze prime density on diagonals of Ulam spiral.
        
        In DVFM: Diagonals correspond to n mod m = constant for certain m.
        """
        x, y, is_prime = self.spiral.generate_spiral(n_max)
        primes = np.where(is_prime)[0] + 1
        
        # Analyze diagonals (lines with slope ±1)
        # Main diagonal: x = y
        # Anti-diagonal: x = -y
        
        main_diag_mask = (x == y)
        anti_diag_mask = (x == -y)
        
        main_diag_primes = np.sum(is_prime & main_diag_mask)
        anti_diag_primes = np.sum(is_prime & anti_diag_mask)
        total_main_diag = np.sum(main_diag_mask)
        total_anti_diag = np.sum(anti_diag_mask)
        
        print("=" * 70)
        print("DVFM ANALYSIS: Ulam Spiral Diagonals")
        print("=" * 70)
        print(f"Main diagonal (x = y):")
        print(f"  Total numbers: {total_main_diag}")
        print(f"  Primes: {main_diag_primes}")
        print(f"  Prime density: {main_diag_primes/total_main_diag:.4f}")
        print()
        print(f"Anti-diagonal (x = -y):")
        print(f"  Total numbers: {total_anti_diag}")
        print(f"  Primes: {anti_diag_primes}")
        print(f"  Prime density: {anti_diag_primes/total_anti_diag:.4f}")
        
        # Compare with overall density
        overall_density = np.sum(is_prime) / n_max
        print(f"\nOverall prime density: {overall_density:.4f}")
        
        return {
            'main_diag': main_diag_primes / total_main_diag if total_main_diag > 0 else 0,
            'anti_diag': anti_diag_primes / total_anti_diag if total_anti_diag > 0 else 0,
            'overall': overall_density
        }
    
    def analyze_modular_patterns(self, n_max: int = 10000, moduli: List[int] = [2, 3, 5, 7]):
        """
        Analyze how modular residues correlate with Ulam spiral positions.
        
        This connects Ulam spiral to DVFM's modular embedding Phi_k(n).
        """
        from sympy import prime as nth_prime
        
        x, y, is_prime = self.spiral.generate_spiral(n_max)
        
        print("=" * 70)
        print("DVFM MODULAR ANALYSIS: Ulam Spiral vs Phi_k(n)")
        print("=" * 70)
        
        for modulus in moduli:
            # Group positions by residue modulo modulus
            residues = np.arange(1, n_max + 1) % modulus
            
            print(f"\nModulus {modulus}:")
            for r in range(modulus):
                mask = (residues == r)
                if np.sum(mask) == 0:
                    continue
                prime_count = np.sum(is_prime & mask)
                total_count = np.sum(mask)
                density = prime_count / total_count if total_count > 0 else 0
                # Highlight residues with high prime density
                marker = " ***" if density > 0.2 and r != 0 else ""
                print(f"  n mod {modulus} = {r}: {prime_count:5d} / {total_count:5d} = {density:.4f}{marker}")
        
        return residues, is_prime


# ============================================================================
# 4. VISUALIZATIONS
# ============================================================================

def create_ulam_spiral_visualization(
    prime_db: PrimeDatabase,
    n_max: int = 10000,
    output_file: str = None
) -> plt.Figure:
    """
    Create Ulam spiral visualization with DVFM interpretation.
    
    The spiral shows:
    - Black dots: composite numbers
    - Colored dots: primes (color indicates modular residue)
    - Patterns: diagonals (arithmetic progressions) visible
    """
    
    spiral = UlamSpiral(prime_db)
    x, y, is_prime = spiral.generate_spiral(n_max)
    
    # Create figure
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    
    # Plot 1: Traditional Ulam spiral (primes vs composites)
    ax1 = axes[0]
    
    # Plot composites in light gray (background)
    composite_mask = ~is_prime
    ax1.scatter(x[composite_mask], y[composite_mask], 
                c='lightgray', s=1, alpha=0.5)
    
    # Plot primes in red
    ax1.scatter(x[is_prime], y[is_prime], 
                c='red', s=2, alpha=0.8)
    
    ax1.set_title(f'Ulam Spiral (DVFM Projection)\nn = 1 to {n_max:,}\nRed = Primes, Gray = Composites', 
                  fontsize=12, fontweight='bold')
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.set_aspect('equal')
    ax1.grid(True, alpha=0.2)
    
    # Plot 2: Color-coded by modular residue (DVFM Phi_k)
    ax2 = axes[1]
    
    # Use modulus 3 for coloring (shows the 3-fold symmetry)
    residues = np.arange(1, n_max + 1) % 3
    colors = ['blue', 'green', 'orange']
    labels = ['n mod 3 = 0', 'n mod 3 = 1', 'n mod 3 = 2']
    
    for r in range(3):
        mask = (residues == r) & is_prime
        ax2.scatter(x[mask], y[mask], 
                    c=colors[r], s=2, alpha=0.8, label=labels[r])
    
    # Also show composites faintly
    ax2.scatter(x[composite_mask], y[composite_mask], 
                c='lightgray', s=0.5, alpha=0.3)
    
    ax2.set_title(f'DVFM Interpretation: Primes colored by n mod 3\nShows 3-fold spiral arms', 
                  fontsize=12, fontweight='bold')
    ax2.set_xlabel('x')
    ax2.set_ylabel('y')
    ax2.set_aspect('equal')
    ax2.legend(loc='upper right', fontsize=9, markerscale=3)
    ax2.grid(True, alpha=0.2)
    
    plt.suptitle(f'Ulam Spiral in DVFM/Fonat-Taometria Framework\n{len(prime_db.primes):,} primes loaded', 
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Saved: {output_file}")
    
    return fig


def create_dvfm_vector_field_on_spiral(
    prime_db: PrimeDatabase,
    n_max: int = 5000,
    output_file: str = None
) -> plt.Figure:
    """
    Visualize the discrete vector field on the Ulam spiral.
    
    In DVFM: V(n) = Phi(n+1) - Phi(n)
    On the spiral, this shows how the flow moves between numbers.
    """
    
    spiral = UlamSpiral(prime_db)
    x, y, is_prime = spiral.generate_spiral(n_max)
    
    # Compute vector field directions
    # V(n) points from n to n+1 in the spiral
    directions = []
    
    for n in range(1, n_max):
        x1, y1 = spiral.get_coordinates(n)
        x2, y2 = spiral.get_coordinates(n + 1)
        dx = x2 - x1
        dy = y2 - y1
        directions.append((dx, dy, n))
    
    fig, ax = plt.subplots(figsize=(12, 12))
    
    # Plot the spiral path
    ax.plot(x, y, 'k-', alpha=0.3, linewidth=0.5)
    
    # Plot primes
    ax.scatter(x[is_prime], y[is_prime], c='red', s=5, alpha=0.8, label='Primes')
    
    # Plot vector field arrows (sample every N points for clarity)
    sample_step = 50
    for i in range(0, len(directions), sample_step):
        dx, dy, n = directions[i]
        if n < n_max:
            x_n, y_n = spiral.get_coordinates(n)
            ax.arrow(x_n, y_n, dx * 0.3, dy * 0.3, 
                    head_width=0.1, head_length=0.1, 
                    fc='blue', ec='blue', alpha=0.5)
    
    ax.set_title(f'DVFM Discrete Vector Field on Ulam Spiral\nV(n) = Phi(n+1) - Phi(n) (blue arrows)', 
                 fontsize=12, fontweight='bold')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_aspect('equal')
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(True, alpha=0.2)
    
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Saved: {output_file}")
    
    return fig


def create_taometry_spiral_analysis(
    prime_db: PrimeDatabase,
    n_max: int = 50000,
    output_file: str = None
) -> plt.Figure:
    """
    Fonat-Taometria analysis: Show how spiral arms correspond to residue classes.
    
    This demonstrates the connection between Ulam spiral and modular braids.
    """
    
    spiral = UlamSpiral(prime_db)
    x, y, is_prime = spiral.generate_spiral(n_max)
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    # Different moduli to show different spiral arm patterns
    moduli_analysis = [(2, 'blue', 'red'), (3, 'green', 'orange'), (4, 'purple', 'yellow'), (5, 'brown', 'pink')]
    
    for idx, (mod, color1, color2) in enumerate(moduli_analysis):
        ax = axes[idx // 2, idx % 2]
        residues = np.arange(1, n_max + 1) % mod
        
        # Show only primes with specific residues
        for r in range(mod):
            if r == 0:
                continue  # Skip multiples
            mask = (residues == r) & is_prime
            if np.sum(mask) > 0:
                # Color intensity based on residue
                intensity = r / mod
                color = plt.cm.viridis(intensity)
                ax.scatter(x[mask], y[mask], c=[color], s=1, alpha=0.6)
        
        ax.set_title(f'Fonat-Taometria: Primes with n mod {mod} != 0\n{mod}-fold spiral arms visible', 
                     fontsize=10, fontweight='bold')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.1)
    
    plt.suptitle(f'Fonat-Taometria Analysis: Ulam Spiral Decomposition by Modulus\nShows how spiral arms = residue classes', 
                 fontsize=13, fontweight='bold')
    plt.tight_layout()
    
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Saved: {output_file}")
    
    return fig


# ============================================================================
# 5. MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("ULAM SPIRAL in DVFM / FONAT-TAOMETRIA Framework")
    print("=" * 70)
    
    # Load prime database
    prime_db = PrimeDatabase()
    
    # Create Ulam spiral interpreter
    interpreter = DVFMUlamInterpreter(prime_db)
    
    # Analyze diagonal patterns
    print("\n")
    interpreter.analyze_diagonals(n_max=50000)
    
    # Analyze modular patterns
    print("\n")
    interpreter.analyze_modular_patterns(n_max=50000, moduli=[2, 3, 4, 5])
    
    # Create visualizations
    print("\n" + "=" * 70)
    print("CREATING VISUALIZATIONS")
    print("=" * 70)
    
    # 1. Basic Ulam spiral
    fig1 = create_ulam_spiral_visualization(prime_db, n_max=20000, 
                                              output_file="ulam_spiral_basic.png")
    
    # 2. DVFM vector field on spiral
    fig2 = create_dvfm_vector_field_on_spiral(prime_db, n_max=5000,
                                                output_file="ulam_spiral_vector_field.png")
    
    # 3. Fonat-Taometria analysis
    fig3 = create_taometry_spiral_analysis(prime_db, n_max=30000,
                                             output_file="ulam_spiral_taometry.png")
    
    print("\n" + "=" * 70)
    print("ALL VISUALIZATIONS COMPLETED!")
    print("Files saved:")
    print("  - ulam_spiral_basic.png")
    print("  - ulam_spiral_vector_field.png")
    print("  - ulam_spiral_taometry.png")
    print("=" * 70)
    
    plt.show()