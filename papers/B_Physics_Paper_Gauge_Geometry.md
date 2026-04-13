# Gauge-Geometry Coupling Is a Necessary Consequence
# of Self-Referential Dynamics on Graphs

Hyeokjun Kwon — April 2026

---

**Abstract.** We prove that any system in which a field reads itself on a graph necessarily produces an edge operator T = C·S coupling gauge content (C) to geometric structure (S). This Hadamard product follows from three axioms and variational stability (Theorem 1). The discrete gauge-geometry equation of motion follows from δS/δl = 0 (Theorem 2). We verify universality by ab initio Monte Carlo simulation across seven configurations: 2D U(1), 2D SU(2), 3D U(1), 4D U(1), and 4D SU(2) at three lattice sizes (L = 4, 6, 8). The gauge-geometry correlation r(β) is non-zero in all 42 measurements (minimum significance: 13.6σ). The non-monotonic r(β) profile is confirmed across dimensions and gauge groups. Finite-size scaling of 4D SU(2) shows the peak correlation r(β = 1.0) = 0.343 ± 0.002 is stable across L = 4–8, confirming a bulk effect. These results establish that gauge-gravity coupling is forced by the mathematical structure of self-referential field dynamics.

---

## 1. Introduction

The coupling of gauge forces to gravity—encoded in the Einstein equation Gμν = 8πG Tμν—is derived from the Einstein-Hilbert action by variational calculus. No deeper explanation is offered for why matter and geometry interact; the equivalence principle provides operational meaning but not logical necessity.

We prove that this coupling is a theorem, not a postulate. Any system in which a field reads its own values across a graph necessarily produces an operator coupling state comparisons (gauge content) to graph structure (geometry). The proof requires the uniqueness of the inner product, the uniqueness of the self-adjoint normalized adjacency, and variational stability.

We compute the ab initio predictions by Monte Carlo simulation across seven configurations spanning two gauge groups (U(1), SU(2)), three spatial dimensions (2D, 3D, 4D), and three lattice sizes for 4D SU(2) (L = 4, 6, 8). Forty-two independent measurements at six coupling values yield significance ranging from 13.6σ to 326σ. No configuration shows r = 0 at any coupling.

Scope: All results are proved and computed in the weak-field (linearized Regge) regime. The non-perturbative regime is discussed in Section 8.


## 2. The Hadamard Necessity Theorem

**Proposition 1 (Content uniqueness).** The state comparison Cₐₕ = ⟨φₐ, φₕ⟩ is the unique rotationally invariant bilinear form on unit vectors (Schur's lemma). Non-bilinear SO(d)-invariant functions (e.g., RBF kernels) are excluded by variational stability [Kwon 2026a, Proposition 1, Remark]. Physically: C = cosθ = Re(e^{iθ}), the U(1) gauge link variable (Wilson 1974). For SU(2), C = Re(Tr U)/2, the fundamental character. This is not merely a conventional choice; the companion paper [Kwon 2026h, Theorem 7] proves that the fundamental character is the unique content function consistent with faithful self-reference — integer representations are blind at maximal disorder, and higher half-integer representations invert the sign of content.

**Proposition 2 (Structure uniqueness).** With self-adjointness (required for energy conservation and reversible dynamics), the propagation matrix S = D⁻½AD⁻½ is the unique spectrally consistent normalization (Chung 1997). The random walk matrix D⁻¹A has the same eigenvalues but is not self-adjoint.

**Lemma 1 (Hadamard necessity).** Any bilinear, pointwise-dependent operation on the space of edge-supported matrices is a scalar multiple of the Hadamard product. This rules out matrix multiplication (non-local), tensor products (wrong codomain), and direct sums (non-scalar).

**Theorem 1 (Variational necessity).** Under Axioms 1–3 (locality, rotational invariance, self-adjoint spectral consistency) and variational stability, the edge operator is uniquely Tₐₕ = Cₐₕ · Sₐₕ.

*Proof.* Propositions 1–2 determine C and S. Lemma 1 determines the Hadamard composition among bilinear operations. For non-linear alternatives T = CᵅSᵝ: variational stability requires ∂²T/∂C² = α(α−1)Cᵅ⁻²Sᵝ = 0. This gives α = 0 or α = 1. Since α = 0 decouples gauge from geometry, α = 1. By the same argument, β = 1. The full proof — extending to all analytic compositions T = f(C, S) via Taylor expansion and showing that variational stability forces f(C, S) = λCS — is in [Kwon 2026a, Theorem 1, Case 2]. □


## 3. The Discrete Gauge-Geometry Equation of Motion

The Hadamard-coupled lattice action is S = −Nβ Σ_P w_P cos Θ_P + κ Σ_e (w_e − 1)², where w_P = (∏_{e∈∂P} w_e)^{1/2} is the plaquette area measure. The first term is the gauge action weighted by local geometry; the second is the linearized Regge action governing edge-weight fluctuations around flat spacetime (w = 1).

**Theorem 2.** Varying with respect to edge weight w_e yields: 2κ(w_e − 1) = Nβ Σ_{P∋e} (∂w_P/∂w_e) cos Θ_P. Elastic resistance (left) equals gauge-geometry driving force (right). The multiplicative coupling w_P × cos Θ_P ensures δS_{gauge}/δw_e ≠ 0; an additive action would yield δS_{gauge}/δw_e = 0, precluding any gauge-geometry dynamics. □

*Scope note.* Theorem 2 operates in the linearized Regge regime. The full tensorial structure of spin-2 gravity in 3+1D requires non-linearized Regge dynamics, beyond the scope of this paper.


## 4. Path Integral Validation

On a fixed (non-dynamical) 2D lattice, the U(1) Monte Carlo reproduces the exact solution ⟨cos P⟩ = I₁(β)/I₀(β) within statistical error (Table 1). A null test on the fixed lattice yields r = 0.004 ± 0.003 (1.6σ), consistent with zero.

Table 1. Fixed-lattice U(1): MC vs exact I₁(β)/I₀(β).


## 5. Universality across Dimensions and Gauge Groups

We test the central prediction—r(β) > 0 at all couplings—across seven configurations (including 4D U(1)). All simulations use Metropolis with alternating gauge and geometry sweeps, linearized Regge action with κ = 1.0.

### 5.1 Results: 2D, 3D, and 4D U(1)

Table 2. Gauge-geometry correlation r(β) in 2D, 3D, and 4D U(1). All values >13σ significant.

### 5.2 Results: 4D SU(2) with Finite-Size Scaling

The critical test: non-abelian gauge theory in four dimensions with dynamical geometry. We measure r(β) at three lattice sizes to establish that the correlation is a bulk effect.

Table 3. 4D SU(2) finite-size scaling. Peak r(β=1.0) = 0.345, 0.341, 0.342 at L = 4, 6, 8: stable to three significant figures. All 18 measurements >49σ.

Table 4. Statistical significance. Minimum: 49σ (L=4, β=3.0). Maximum: 326σ (L=6, β=5.0).

Figure 1. (a) Gauge-geometry correlation across 2D/3D configurations. (b) 4D SU(2) finite-size scaling: L = 4, 6, 8 profiles overlap. (c) Peak r(β=1.0) vs lattice size: stable at 0.343 ± 0.002. (d) Summary table.

### 5.3 Key Observations

**(i) Universality of non-zero coupling.** r(β) > 0 in all 42 measurements across 7 configurations. Gauge fields and geometry are never statistically independent on a dynamical lattice.

**(ii) Non-monotonic profile.** The competition between gauge disorder (low β) and gauge freezing (high β) produces a peak at intermediate β. The peak position is β ≈ 1.5–2.0 in 2D and β ≈ 1.0 in 3D and 4D. The post-peak decline is sharpest in 4D (r drops by a factor of ~3 from peak to β = 5.0 at L = 8), moderate in 3D, and weakest in 2D SU(2), where r remains elevated at high β (0.395 at β = 5.0 vs peak 0.411 at β = 2.0). This dimensional dependence is consistent with the richer fluctuation spectrum in lower dimensions sustaining gauge-geometry coupling even when the gauge field is strongly ordered.

**(iii) Finite-size convergence.** In 4D SU(2), the peak correlation r(β = 1.0) = 0.345, 0.341, 0.342 at L = 4, 6, 8 respectively. This three-significant-figure stability across a factor-of-8 volume change (256 → 4096 sites) establishes the correlation as a bulk thermodynamic property, not a finite-size artifact.

**(iv) Gauge group dependence.** SU(2) exhibits stronger coupling than U(1) in matched dimensions. In 4D, SU(2) achieves r = 0.34 compared to U(1)'s r = 0.23 at β = 1.0. The three generators of SU(2) provide more degrees of freedom for gauge-geometry coupling.

**(v) High-β secondary rise at small L.** In 4D SU(2) at L = 4, the correlation r increases from 0.088 (β = 3.0) to 0.156 (β = 5.0), creating a secondary rise after the primary peak. This effect weakens with increasing lattice size: at L = 6, the corresponding values are 0.153 → 0.126, and at L = 8, 0.133 → 0.122 (monotonically decreasing). The L-dependence identifies this as a finite-size artifact: at L = 4, the lattice has only 256 sites, and at β = 5.0 the gauge field is nearly frozen (plaquette ≈ 1), reducing the effective number of independent degrees of freedom to the point where geometric fluctuations become correlated with the residual gauge ordering. This effect vanishes in the thermodynamic limit and does not affect the central conclusion (r > 0 at all couplings), which is supported by the L = 8 data where no secondary rise is observed.

**(vi) Magnitude of r and unexplained variance.** The peak Pearson correlation r ≈ 0.34 explains approximately 12% of the plaquette-level variance. The remaining 88% is attributable to local thermal fluctuations: at the plaquette level, individual gauge angles and edge lengths undergo independent Metropolis updates with large per-step noise. The correlation r measures the *systematic* component of gauge-geometry coupling surviving these fluctuations. A global observable — for example, the correlation between the spatially averaged plaquette and the spatially averaged edge length — would yield a higher r by averaging out local noise, but would sacrifice the ability to probe spatial structure. The fact that a systematic r > 0 is detectable above local noise at 13σ–326σ significance is itself evidence of strong underlying coupling.


## 6. Analytical Mean-Field Prediction

For 2D U(1), the mean-field correlation is r_MF(β) = βf′(β)/(2κσ_c), where f(β) = I₁(β)/I₀(β). The MC exceeds mean-field by a factor of 1.2–1.4 across all β, attributable to fluctuation corrections. The constancy of the MC/MF ratio is a falsifiable prediction.


## 7. Implications

**(i) Mathematical necessity.** T = C·S is the unique variationally stable, self-adjoint, local, rotationally invariant edge operator (Theorem 1). No postulates beyond the three axioms and variational stability are required.

**(ii) Physical identification.** C is the standard lattice gauge link variable (Wilson 1974). S converges to the Laplace-Beltrami operator. In Regge calculus, edge lengths encode the metric (Regge 1961). These are established identifications.

**(iii) Variational coupling.** The discrete gauge-geometry equation of motion (Theorem 2) is derived by δS/δlₑ = 0, yielding geometric deformation proportional to gauge energy—the same variational structure as general relativity.

**(iv) Universality.** 42 measurements across 7 configurations, all r > 0, all >13σ. Gauge fields cannot propagate independently of geometry on a dynamical lattice.

**(v) Finite-size stability.** The 4D SU(2) peak correlation is volume-independent (Table 3), confirming a bulk thermodynamic effect.


## 8. Scope and Limitations

All results are in the linearized Regge (weak-field) regime. Extensions: SU(3) in 4D; full non-linearized Regge dynamics; topology-changing moves; causal structure and Lorentzian signature (CDT framework); continuum limit analysis. Each is a well-defined computational program using established lattice methodology.


## 9. Discussion

**On the meaning of "coupling."** Throughout this paper, "gauge-geometry coupling" refers to the Hadamard inseparability of C and S in the product T = C·S. The correlation r(β) > 0 is not evidence that two independent entities interact — it is the manifestation of a single entity T projected onto two measurement channels (plaquette weight and plaquette angle). Just as measuring the x and y projections of a vector always yields a correlation unless the vector is axis-aligned, measuring the C and S projections of T always yields r > 0 unless the Hadamard structure is broken (κ = ∞, the null test). The 42 measurements across 7 configurations confirm that T = C⊙S is one inseparable field.

This paper establishes: (1) T = C·S is the unique variationally stable edge operator (Theorem 1). (2) Variation yields the discrete gauge-geometry equation of motion (Theorem 2). (3) The gauge-geometry correlation is non-zero across two gauge groups, four configurations (2D, 3D, 4D), and three lattice sizes for 4D SU(2) (42 measurements, all >13σ). (4) Finite-size scaling confirms the correlation is a bulk effect.

The central claim is falsifiable: a measurement of r = 0 at any coupling in any gauge group or dimension would refute it. No such measurement has been found across 42 independent tests.

If confirmed with SU(3) and full Regge dynamics, these results would establish that the coupling of gauge forces to gravity is not a contingent feature of our universe but a mathematical necessity inherent in self-referential field dynamics. The companion paper [Kwon 2026h] shows that this coupling produces a two-sector spectral structure: massive, localized excitations (matter) at short wavelengths and unstable, expanding modes (cosmology) at long wavelengths — both from the same Hadamard-coupled action verified here.

**Independent confirmation from CDT.** The Causal Dynamical Triangulations program [Ambjorn, Jurkiewicz, Loll 2004, 2005] is an independent approach to dynamical-geometry lattice field theory. CDT uses simplicial triangulations with topology change (unlike our fixed-topology edge-weight approach), yet produces the same qualitative physics: a 4D de Sitter spacetime emerges dynamically from the path integral over geometries, with Hausdorff dimension converging to 4 and spatial slices exhibiting homogeneity. These are precisely the predictions of the Hadamard framework (Papers G, J). The agreement between two independent dynamical-geometry programs — using different discretizations, different dynamics, and different methodologies — constitutes evidence that the underlying physics (gauge-geometry coupling producing expansion and d = 4) is robust and discretization-independent.


## Methods

**Fixed-lattice validation.** 2D U(1), 8×8 periodic, Metropolis, δθ ~ U(−2, 2), 300 thermalization + 500 measurement sweeps.

**2D dynamical.** U(1): 8×8, same gauge updates, edge weights w initialized at 1, δw ~ N(0, 0.05), w ≥ 0.1, κ = 1.0, 200+200 sweeps. SU(2): 8×8, quaternion representation, near-identity Metropolis (ε = 0.5).

**3D dynamical.** U(1), 5³ periodic, 100+150 sweeps, same update procedures.

**4D U(1) dynamical.** U(1), 3⁴ periodic, 80 thermalization + 100 measurement sweeps, same update procedures as 3D U(1).

**4D SU(2) dynamical.** L = 4, 6, 8 periodic lattices, SU(2) in quaternion representation, Numba JIT-compiled Metropolis. 200 thermalization + 300 measurement sweeps per β. Near-identity gauge updates (ε = 0.5), weight updates δw ~ N(0, 0.05), w ≥ 0.1.

**Correlation.** Pearson r between plaquette weight w_P = (∏_{e∈∂P} w_e)^{1/2} and Re(Tr U_P)/2, computed per configuration across all plaquettes and orientations.

**Null test.** Fixed lattice (no geometry updates): r = 0.004 ± 0.003 (1.6σ), consistent with zero.

**Reproducibility.** All simulations use deterministic seeds. Full source code provided as supplementary material. The 2D U(1) results are generated by `run_2d_u1()` in `hadamard_mc_suite.py`; all other configuration results are provided as JSON data files.

**Ergodicity diagnostics.** For each configuration, we verified that the Metropolis acceptance rate remains in the range 30–70% across all β values. At high β (≥ 5.0), gauge updates approach freezing and acceptance rates drop to ~35%; the geometry updates maintain ~50% acceptance. For the smallest lattice (4D SU(2), L = 4), we performed an additional check with doubled thermalization (400 sweeps) and confirmed that the measured r values agree within statistical error, indicating adequate equilibration. The secondary rise in r at β = 5.0 for L = 4 (see §5.3(v)) persists after extended thermalization, confirming it is a finite-size effect rather than an equilibration artifact.


## Acknowledgments

The author used Claude (Anthropic) as a computational tool for mathematical verification, numerical simulation, and assistance in preparing the manuscripts. All theoretical content — axioms, theorems, proofs, physical interpretations, and strategic decisions — is the author's original work. The author takes full responsibility for all content.

---

## References

- Regge, T. General relativity without coordinates. Nuovo Cim. 19, 558–571 (1961).
- Williams, R.M. & Tuckey, P.A. Regge calculus: a brief review. CQG 9, 1409 (1992).
- Wilson, K.G. Confinement of quarks. Phys. Rev. D 10, 2445 (1974).
- Chung, F.R.K. Spectral Graph Theory. CBMS 92, AMS (1997).
- Ambjorn, J. et al. Reconstructing the universe. Phys. Rev. D 72, 064014 (2005).
- Ambjorn, J. et al. Nonperturbative Lorentzian path integral. PRL 85, 924 (2000).
- Ambjorn, J. et al. Emergence of a 4D world from causal quantum gravity. PRL 93, 131301 (2004).
- Loll, R. Quantum gravity from causal dynamical triangulations: a review. CQG 37, 013002 (2020).
- Belkin, M. & Niyogi, P. Convergence of Laplacian eigenmaps. NIPS 19, 129 (2007).
- García Trillos, N. et al. Spectral convergence. Found. Comput. Math. 20, 827 (2020).
- Weyl, H. Math. Ann. 71, 441 (1912).
- Kato, T. Perturbation Theory for Linear Operators. Springer (1966).
- Jacobson, T. Thermodynamics of spacetime. PRL 75, 1260 (1995).
- Kwon, H. The Hadamard structure of self-referential graphs. arXiv (2026a).
- Kwon, H. The excitation spectrum of self-referential fields. arXiv (2026h).
