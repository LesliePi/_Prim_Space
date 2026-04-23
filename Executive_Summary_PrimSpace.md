# Executive Summary
## PrimSpace: Prime Numbers as a Field on a Discrete Torus

**Author:** László Tatai / BarefootRealism Labs  
**Date:** April 2026  
**Contact:** ORCID 0009-0007-5153-6306  
**Related:** DVFM v1.1 — Zenodo https://doi.org/10.5281/zenodo.17675025

---

## The Question

Prime numbers have been studied for thousands of years. Their distribution
is described by the Prime Number Theorem, bounded by the Riemann Hypothesis,
and constrained by the sieve of Eratosthenes. Yet one question remains
surprisingly open:

**Within the states the sieve allows, why do some states attract
more primes than others?**

This release provides an empirical answer — and a framework for thinking
about it.

---

## The Key Idea

Every natural number $n$ maps to a point in a modular state space:

$$\Phi_k(n) = (n \bmod p_1,\; n \bmod p_2,\; \ldots,\; n \bmod p_k)$$

This space $\Omega_k$ has the natural topology of a **discrete torus** —
each dimension wraps around with the period of its prime modulus.
The modular trajectories of consecutive integers are geodesic lines
on this torus, braiding around each other with different periods.

The prime distribution in this space decomposes into three independent
components:

$$P(\text{prime at } s) = \mu(s) \cdot S(s) \cdot \rho(s)$$

| Component | What it is | What we knew |
|-----------|-----------|-------------|
| $\mu(s)$ | Occupancy — how often each state is visited | Uniform (CRT) — known |
| $S(s)$ | Sieve mask — which states are forbidden | Binary — known since Eratosthenes |
| $\rho(s)$ | Prime preference field | **Non-constant, structured — this is new** |

---

## What Is New

**1. $\rho(s)$ is not constant.**

Within the states permitted by the sieve, primes are not uniformly
distributed. Some states systematically attract more primes than others.
This is confirmed empirically for $N = 10^8$, across multiple moduli
sets including $\{2,3,5,7,11,13\}$ and $\{41,43\}$.

**2. $\rho(s)$ has Fourier structure.**

The Fourier spectrum of $\rho$ on $\Omega_k$ shows dominant discrete
peaks — not white noise. The prime preference field is compressible:
it can be reconstructed from a small number of harmonic components.
This means the primes carry a hidden periodicity beyond the obvious
sieve structure.

**3. The twin prime gap signature is universal.**

For every twin prime pair $(p, p+2)$ tested, the gap point $g = p+1$
falls in a local minimum of the residual density $\alpha_k(n)$ —
equivalently, a local maximum of the potential $V(g) = -\ln\rho(g)$.
This signature appears to be universal across all twin prime pairs
in the tested range.

**4. The sieve sum is exact.**

$$\sum_{s \in \Omega_k} \mu(s)\, S(s) = \rho_{\text{sieve}}
= \prod_{p \in \mathcal{P}_k}\left(1 - \frac{1}{p}\right)$$

Confirmed to six decimal places at $N = 10^8$. The global density
is exactly the Euler product — but the local structure is not flat.

---

## The Potential Field

The prime preference field defines a natural potential:

$$V(s) = -\ln\rho(s)$$

This potential has a direct physical interpretation:
- Low $V(s)$: prime-friendly state — primes concentrate here
- High $V(s)$: prime-sparse state — primes avoid this region
- $V(s) = \infty$: forbidden state ($S(s) = 0$)

The twin prime gap point $g = p+1$ is always a local maximum of $V$ —
a potential barrier between two prime-rich states.

---

## Connection to the GPM Framework

The potential $V(s) = -\ln\rho(s)$ is formally identical to the
potential used in the Gauss–PowerLaw Module (Tatai, 2026):
$V(x) = -\ln\mu^*(x)$. In both frameworks, critical transitions
occur at potential minima, and the structure of the field encodes
the system's phase behavior.

This is not claimed to be more than a formal analogy at this stage.
Whether the correspondence between prime field theory and dynamical
systems theory runs deeper is an open question — and one worth pursuing.

---

## What Is Included in This Release

- **Mathematical framework** — formal definitions, master equation,
  Fourier decomposition, potential field, open questions
- **Prime number data** — all primes up to 1,000,000 (CSV format)
- **Empirical figures** — modular occupancy, prime density maps,
  Fourier spectra, Ulam spiral decompositions, twin prime signatures
- **Integrity verification** — all documents in both `.md` and `.mdl`
  format (MDL cryptographic authorship proof)

---

## What This Is Not

This release does not prove the Riemann Hypothesis.
It does not prove the Twin Prime Conjecture.
It does not claim to solve any open problem in number theory.

What it does is provide a **new representational framework** — a way
of seeing prime distribution as a field on a geometric space, with
measurable structure, Fourier decomposition, and a potential-theoretic
interpretation. Whether this framework leads to deeper results is a
question for future work.

---

## Citation

```
Tatai, L. (2026). PrimSpace: Prime Numbers as a Field on a Discrete Torus.
BarefootRealism Labs. Zenodo. doi: [assigned on upload]
```

---

## Related Work

Tatai, L. (2025). *Discrete Vector Field Method (DVFM) v1.1.*
Zenodo. https://doi.org/10.5281/zenodo.17675025

Tatai, L. (2026). *The Gauss–PowerLaw Module (GPM): Endogenous
Heavy-Tail Formation as a Bifurcation Phenomenon.*
Zenodo. https://doi.org/10.5281/zenodo.19692647

---

*Integrity verified with MDL (Markdown Logged) —
a tamper-evident document format developed by BarefootRealism Labs.*
