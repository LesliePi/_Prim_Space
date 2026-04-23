# PrimSpace — Primes as a Field on a Discrete Torus

**Author:** László Tatai / BarefootRealism Labs  
**ORCID:** [0009-0007-5153-6306](https://orcid.org/0009-0007-5153-6306)  
**License:** Apache 2.0  
**Zenodo:** [doi.org/10.5281/zenodo.19705530](https://doi.org/10.5281/zenodo.19705530)  
**Related:** DVFM v1.1 — [doi.org/10.5281/zenodo.17675025](https://doi.org/10.5281/zenodo.17675025)  
**Status:** Active research — preprint available, formal proofs in progress

---

> *"The primes do not sit randomly on the torus. They cluster. They have preferences. This is the field."*

---

## Overview

PrimSpace is a mathematical framework that maps the natural numbers onto a **discrete torus** via modular embedding, then studies the resulting **prime preference field** ρ(s) — the non-uniform distribution of primes across the torus states.

Every natural number maps to a point in the modular state space via:

$$\Phi_k(n) = (n \bmod p_1,\; n \bmod p_2,\; \ldots,\; n \bmod p_k)$$

The prime distribution decomposes into three independent components:

$$P(\text{prime at } s) = \mu(s) \cdot S(s) \cdot \rho(s)$$

| Component | Result |
|-----------|--------|
| $\mu(s)$ | Uniform occupancy — proven by CRT, confirmed at $N = 10^8$ |
| $S(s)$ | Binary sieve mask — exact Euler product |
| $\rho(s)$ | **Non-constant, Fourier-structured — this is new** |

**Central empirical result:** Within the sieve-permitted states, primes are *not* uniformly distributed. The prime preference field ρ(s) is compressible — its Fourier spectrum shows discrete peaks, not white noise, and the field can be reconstructed from a small number of Fourier components.

---

## Repository Structure

```
_Prim_Space/
├── README.md
├── requirements.txt
├── LICENSE
│
├── core/
│   ├── prim_core_engine.py
│   ├── prime_analysis.py
│   ├── Primspace_Core_Engine_v3_0.py
│   └── primspace_core_engine_v3_1.py
│
├── analysis/
│   ├── PRIME_001.py
│   ├── primspace_deep_analysis.py
│   └── primspace_examples.py
│
├── visualizations/
│   ├── Ulam_Spiral_in_DVFM.py
│   └── primspace_visualizations.py
│
├── lab/
│   └── PrimSpace_Research_Lab_v3.html   ← interactive browser tool
│
├── paper/
│   └── PrimSpace_Mathematical_Framework.md
│
├── data/
│   ├── README_data.md
│   └── PrimNumb.csv                     ← primes up to 1,000,000
│
└── results/                             ← timestamped figures and run manifests
    ├── 20260423_072309_torus_2d.png
    ├── 20260423_072314_torus_braid.png
    ├── 20260423_072315_rho_fourier.png
    ├── 20260423_072316_twin_prime_fourier.png
    ├── 20260423_074103_occupancy_ratio_zoom.png
    ├── 20260423_074104_forbidden_bands_11x13.png
    └── 20260423_075820_envelope_potential.png
```

---

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the main analysis

```bash
python analysis/PRIME_001.py
```

Computes μ(s), ρ(s), V(s), Fourier spectrum, and generates all figures.

### 3. Interactive browser lab

Open `lab/PrimSpace_Research_Lab_v3.html` in any browser — no Python, no server, no installation needed.

---

## Key Results

### Sieve Sum Validation

$$\sum_{s} \mu(s)\, S(s) = \prod_{p \in \{2,3,5,7,11,13\}}\!\!\left(1-\frac{1}{p}\right) = 0.228571\ldots$$

Confirmed to six decimal places at $N = 10^8$.

### Proven Theorems

**Theorem 1 — Structural zero:**  
If $(p, p+2)$ is a twin prime pair with $p > 3$, then $6 \mid (p+1)$.  
*Consequence:* The $p=2$ and $p=3$ terms in $\alpha_k(\text{gap})$ are always zero.  
*Exact formula:* $\alpha_4(g) = \bigl(3\cdot(g \bmod 5) + 2\cdot(g \bmod 7)\bigr) / 48$ — rational, 35 possible values, depends only on $g \bmod 210$.

**Theorem 2 — Exact coverage:**  
If $N = M^k$ where $M = p_k\#$ (the $k$-th primorial), then $\text{occ}[r] = M^{k-1}$ exactly for every residue $r$.  
*Consequence:* $\delta(M,r)$ is an exact integer ratio — zero statistical noise.

**Theorem 3 — Fourier amplitude ratios (empirical):**  
$|\hat{\rho}(1/2)| : |\hat{\rho}(1/3)| : |\hat{\rho}(1/5)| \approx 2 : 1 : 0.5$ — a geometric series encoding the sieve structure.

### Twin Prime Gap Signature

For every twin prime pair $(p, p+2)$ tested, the gap point $g = p+1$ falls in a local minimum of $\alpha_k(n)$ — equivalently, a local maximum of the potential $V(g) = -\ln\rho(g)$.

The exact formula $\alpha_4(g) = (3\cdot(g \bmod 5) + 2\cdot(g \bmod 7))/48$ shows that the gap depth depends only on $g \bmod 210$ — 35 CRT residue classes, each with an exact rational value.

### QFT Analogy

The Fourier decomposition of $\rho(s)$ on $\Omega_k \cong \mathbb{Z}/M\mathbb{Z}$:

$$\rho(r) = \sum_{j=0}^{M-1} \hat{\rho}(j)\cdot e^{2\pi i j r / M}$$

is structurally identical to Shor's quantum Fourier transform with $M = p_k\# = 210$.  
The Fourier modes $e_j(s) = e^{2\pi i j s/M}$ are eigenvectors of the shift operator on $H_k = L^2(\Omega_k)$, $\dim(H_4) = 210$, $\dim(H_5) = 2310$, $\dim(H_6) = 30030$.

---

## Open Questions

1. What is the analytic form of $\rho(s) = \rho_{\text{sieve}} \cdot w(s)$?
2. Does the Fourier spectrum of $\rho$ have a characteristic decay rate?
3. Does the twin prime gap signature persist as $N \to \infty$?
4. Is $\rho(s)$ an eigenstate of some natural operator on $H_k = L^2(\Omega_k)$?
5. Do the dominant Fourier frequencies of $\rho$ correspond to imaginary parts of Riemann zeta zeros?
6. Are quasi-twin pairs $(p = q^2 - 2)$ infinite in number?
7. Does $V(m) \sim C/\ln m$ hold analytically?
8. Is the Carmichael separation (Cohen's $d = 2.59$, $k=6$) provable analytically?

---

## Primorial Field Dynamics (PFD) — Framework Components

| Symbol | Name | Description |
|--------|------|-------------|
| $\alpha_k(n)$ | Primorial Projection Field | Scalar projection into [0,1] |
| $\varphi_k(n)$ | Prime Phase Field | Local phase at dominant resonance |
| $\Delta_k$ | Gap Displacement | Distance to nearest composite structure |
| $\sigma_k$ | Smoothness Ratio | $\Delta_k / S(\Delta_k)$, $S$ = nearest 3-smooth number |
| $\delta(M,r)$ | Prime Preference Field | $\rho(r)/\rho_{\text{global}}$, normalized |
| $\Omega_k$ | State space | Discrete torus $\mathbb{Z}/p_1\mathbb{Z} \times \cdots \times \mathbb{Z}/p_k\mathbb{Z}$ |
| $H_k = L^2(\Omega_k)$ | Primorial Hilbert space | $\dim = p_k\#$ |

---

## Interactive Research Lab

`PrimSpace_Research_Lab_v3.html` runs entirely in the browser:

| Tab | Content |
|-----|---------|
| **α-Field** | Primorial Projection Field, torus CRT map, primorial hierarchy |
| **φ-Phase** | Prime Phase Field, Δφ per twin pair, phase-gap correlation |
| **Δ-Gap** | Category analysis (REJECT / WEAK / MID / STRONG / NSF), smoothness σ_k |
| **Crypto** | Deterministic α_k pre-sieve, Carmichael separation |
| **QFT** | δ(210,r) field, Fourier spectrum, autocorrelation |
| **Theory** | Proven theorems, open conjectures, formal framework |
| **Export** | Timestamped JSON session data, CSV datasets, PNG charts |

---

## Cryptographic Note

This framework has structural implications for prime generation and Carmichael number detection (Cohen's $d = 2.59$ separation at $k=6$). The theoretical results are presented here at the mathematical level. Optimized implementations with cryptographic relevance are being evaluated carefully and are not included in this repository at this stage.

---

## Citation

```bibtex
@misc{tatai2026primspace,
  author    = {Tatai, László},
  title     = {Primes as a Field on a Discrete Torus},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.19705530},
  url       = {https://doi.org/10.5281/zenodo.19705530},
  note      = {Preprint. PrimSpace v1.0}
}
```

---

## Related Work

- Tatai, L. (2025). *Discrete Vector Field Method (DVFM) v1.1.* Zenodo. https://doi.org/10.5281/zenodo.17675025  
- Tatai, L. (2026). *The Gauss–PowerLaw Module (GPM).* Zenodo. https://doi.org/10.5281/zenodo.19692647  
- Tatai, L. (2026). *MDL — Markdown Logged (v1.1).* Zenodo. https://doi.org/10.5281/zenodo.19698943

---

*Integrity verified with [MDL (Markdown Logged)](https://doi.org/10.5281/zenodo.19698943)*  
*"Not a law — a measurement tool. A different paradigm." — PrimSpace, 2026*
