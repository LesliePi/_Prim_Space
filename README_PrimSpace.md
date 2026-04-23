# PrimSpace: Prime Numbers as a Field on a Discrete Torus

**Author:** László Tatai / BarefootRealism Labs  
**ORCID:** 0009-0007-5153-6306  
**License:** MIT  
**Zenodo DOI:** https://doi.org/10.5281/zenodo.19705530
**Related:** DVFM v1.1 — https://doi.org/10.5281/zenodo.17675025

---

## Overview

PrimSpace is a mathematical framework that represents prime number
distribution as a **field on a discrete torus**. Every natural number
maps to a point in a modular state space via:

$$\Phi_k(n) = (n \bmod p_1,\; n \bmod p_2,\; \ldots,\; n \bmod p_k)$$

The prime distribution in this space decomposes into three independent
components:

$$P(\text{prime at } s) = \mu(s) \cdot S(s) \cdot \rho(s)$$

where $\mu(s)$ is the uniform occupancy measure, $S(s)$ is the sieve
mask, and $\rho(s)$ is the **prime preference field** — a structured,
non-constant field whose Fourier spectrum shows discrete peaks.

**Central empirical result:** Within the states permitted by the sieve,
primes are not uniformly distributed. The prime preference field
$\rho(s)$ is compressible — it can be reconstructed from a small number
of Fourier components.

---

## Repository Structure

```
_Prime_Space/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── LICENSE
│
│
├── core/                          
│   ├── prim_core_engine.py               # Core modular space engine
│   ├── prime_analysis.py                 # Analysis pipeline
│   ├── Primspace_Core_Engine_v3_0.py     # Extended engine v3.0
│   └── primspace_core_engine_v3_1.py     # Extended engine v3.1
│                      
├── analysis/                      
│   ├── PRIME_001.py                      # Main analysis pipeline
│   ├── primspace_deep_analysis.py
│   └── primspace_examples.py      
│
├── visualizations/      
│   ├── Ulam_Spiral_in_DVFM.py            # Ulam spiral implementation
│   └── primspace_visualizations.py
│
├── paper/
│   └── PrimSpace_Mathematical_Framework.md
│
├── data/
│   ├── README_data.md                 # Data source instructions
│   └── PrimNumb.csv                   # Primes up to 1,000,000
│
└── results/                           # Figures and output data
    ├── modular_occupancy_11x13.png
    ├── prime_density_11x13.png
    ├── primspace_multilayer.png
    ├── primspace_twin_primes.png
    ├── ulam_spiral_basic.png
    ├── ulam_spiral_taometry.png
    ├── ulam_spiral_vector_field.png
    ├── 20260423_072309_torus_2d.png
    ├── 20260423_072314_torus_braid.png
    ├── 20260423_072315_rho_fourier.png
    ├── 220260423_072316_twin_prime_fourierr.png
    ├── 20260423_074103_occupancy_ratio_zoom.png
    ├── 20260423_074104_forbidden_bands_11x13.png
    └── 20260423_075820_envelope_potential


```

---

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the main analysis

```bash
python PRIME_001.py
```

This computes $\mu(s)$, $\rho(s)$, $V(s)$, Fourier spectrum,
and generates all figures.

### 3. Run the core engine

```bash
python prim_core_engine.py
```

Generates modular spiral visualizations and phase diagrams.

---

## Key Results

### The Master Equation

$$P(\text{prime at } s) = \mu(s) \cdot S(s) \cdot \rho(s)$$

| Component | Result |
|-----------|--------|
| $\mu(s)$ | Uniform — confirmed ($N = 10^8$) |
| $S(s)$ | Binary sieve — exact Euler product |
| $\rho(s)$ | **Non-constant, Fourier-structured** |

### Sieve Sum Validation

$$\sum_{s} \mu(s) S(s) = 0.228571\ldots = \prod_{p \in \{2,3,5,7,11,13\}}\left(1-\frac{1}{p}\right)$$

Confirmed to six decimal places at $N = 10^8$.

### Twin Prime Gap Signature

For every twin prime pair $(p, p+2)$ tested, the gap point $g = p+1$
falls in a local minimum of $\alpha_k(n)$ — a local maximum of the
potential $V(g) = -\ln\rho(g)$. This signature appears universal.

### Fourier Structure

The Fourier spectrum of $\rho$ on $\Omega_k$ shows dominant discrete
peaks at the primorial half-period $M/2$ and its harmonics.
The field is compressible — not white noise.

---

## Mathematical Background

The state space $\Omega_k = \prod_{i=1}^k \mathbb{Z}_{p_i}$ is a
**discrete torus**. The modular trajectories of consecutive integers
are geodesic lines on this torus — straight lines that wrap around
each dimension with period $p_i$.

The potential field $V(s) = -\ln\rho(s)$ has local minima at
prime-rich states (field singularities) and barriers at twin prime
gap points.

**Connection to GPM framework:** The potential $V(s) = -\ln\rho(s)$
is formally identical to $V(x) = -\ln\mu^*(x)$ in the Gauss–PowerLaw
Module (Tatai, 2026). Both frameworks share a potential-theoretic
foundation while operating on different domains.

---

## Open Questions

1. What is the analytic form of $\rho(s) = \rho_{\text{sieve}} \cdot w(s)$?
2. Does the Fourier spectrum have a characteristic decay rate?
3. Does the twin prime gap signature persist as $N \to \infty$?
4. What is the homology of the sublevel sets $\{s : V(s) \leq c\}$?
5. Is the correspondence between PrimSpace and GPM deeper than formal analogy?
6. Are quasi-twin pairs (p = q²-2) infinite in number?
7. Does V(m) ~ C/ln(m) hold analytically?
8. Do prime Fourier frequencies correspond to Riemann zeta zeros?

---

## Citation

```bibtex
@techreport{tatai2026primspace,
  author      = {Tatai, László},
  title       = {PrimSpace: Prime Numbers as a Field on a Discrete Torus},
  institution = {BarefootRealism Labs},
  year        = {2026},
  note        = {Preprint. Zenodo. https://doi.org/10.5281/zenodo.19705530}
}
```

---

## Related Work

- Tatai, L. (2025). *Discrete Vector Field Method (DVFM) v1.1.*
  Zenodo. https://doi.org/10.5281/zenodo.17675025
- Tatai, L. (2026). *The Gauss–PowerLaw Module (GPM).*
  Zenodo. https://doi.org/10.5281/zenodo.19692647
- Tatai, L. (2026). *Operator Theory of Distribution Dynamics (OTDD).*
  BarefootRealism Labs. Zenodo.

---

*Integrity verified with [MDL (Markdown Logged)](https://github.com/BarefootRealismLabs/mdl)*
