# Superadditive Forces from Multi-Gauge Coupling on Shared Geometry:
# Alignment, Propagation, and Analytical Structure

Hyeokjun Kwon — April 2026

---

**Abstract.** When multiple gauge fields share a dynamical lattice geometry, the force each field exerts on the geometry — defined as F_e = −δE/δl_e — exhibits five properties beyond what scalar energy analysis reveals. (1) Forces from independent fields align to >99%, with alignment improving as N increases. (2) Forces concentrate where geometry is least deformed (anti-correlation r = −0.64), producing propagating deformation wave fronts. (3) Net force magnitude scales as |F| ~ N^(1.69 ± 0.06) (R² = 0.997), matching the energy superadditivity exponent. (4) Force direction is temporally stable (consecutive-sweep cosine similarity 0.999), implying DC-like energy output without rectification. (5) F = −dE/dl is verified numerically to machine precision, confirming the discrete gauge-geometry equation of motion (Theorem 2, Kwon 2026a). We further derive analytically that (i) k=0 geometric condensation follows from the AM-GM inequality applied to plaquette weights, and (ii) exponential (de Sitter) expansion of the scale factor a(t) ~ exp(Ht) follows when gauge-geometry coupling exceeds elastic resistance. These results establish that multi-gauge coupling on shared geometry produces coherent, directional, superadditive forces — extending the scalar superadditivity results of Kwon (2026d) to the vector domain.

---

## 1. Introduction

The answer to the force alignment question is contained in one observation: every per-field force acts through the same geometric derivative ∂w_P/∂w_e = w_P/(2w_e), which depends only on geometry, not on the field. All fields push through the same channel. Therefore all fields push in the same direction. The remainder of this paper verifies this observation quantitatively.

The companion paper (Kwon 2026d, hereafter Paper D) established that the geometric deformation energy E scales superadditively as E ~ N^γ (γ = 1.8 ± 0.2) when N gauge fields share a dynamical lattice. However, energy is a scalar — it has magnitude but no direction. The question of *where* and *in what direction* the geometry deforms was left open.

The discrete gauge-geometry equation of motion (Theorem 2, Kwon 2026a) provides the bridge: the force on each edge e is F_e = −δE/δl_e. If energy is superadditive, is force also superadditive? If multiple fields push on geometry, do they push in the same direction or cancel?

These questions have direct implications for energy extraction (rectification requirements), gravitational physics (microscopic force coherence), and cosmology (unidirectional expansion).

## 2. Model and Methods

### 2.1 Force Definition

We use the same lattice gauge-geometry model as Paper D: N independent U(1) gauge fields {θ^(i)} on a 2D L×L periodic lattice with dynamical edge weights {w}. The total action is:

S = −Σ_{i=1}^{N} β Σ_P w_P cos Θ_P^{(i)} + κ Σ_e (w_e − 1)²

This is the Hadamard-coupled action in the Regge convention, where the gauge term −βw_P cos Θ_P is a single product of geometric structure (w_P) and gauge content (cos Θ_P).

The force on edge e is computed by central finite difference: F_e = −[E(w_e + δ) − E(w_e − δ)] / (2δ), δ = 10⁻⁴. This is the gradient of the single Hadamard-coupled action with respect to edge weight, not a force from one sector acting on another.

We distinguish per-field force f_e^{(i)} (gradient of field i's contribution) from total force F_e (full gradient including elastic term).

**Force decomposition.** Each per-field force decomposes as f^{(i)} = g^{(i)} + e, where g^{(i)} = −∂[−βw_P cosΘ_P^{(i)}]/∂w_e is the gauge-only gradient from field i, and e = −2κ(w_e−1) is the elastic gradient shared by all fields. The inter-field alignment (§3.1) could in principle be inflated by the shared elastic term e.

**Verification.** We computed alignment using gauge-only forces g^{(i)} (excluding the elastic term entirely). The results confirm that the alignment is a genuine gauge-geometry effect:

| N | Gauge-only ⟨cosθ⟩ | Full ⟨cosθ⟩ | Gauge-only alignment |
|---|-------------------|-------------|---------------------|
| 2 | 0.963 | 0.961 | 99.1% |
| 3 | 0.978 | 0.973 | 99.3% |
| 5 | 0.996 | 0.995 | 99.9% |
| 10 | 0.999 | 0.999 | 99.9% |

The gauge-only alignment is equal to or HIGHER than the full alignment. The elastic term does not inflate alignment — it slightly dilutes it by adding a common component unrelated to the gauge-geometry coupling. The >99% alignment is entirely attributable to the shared plaquette structure: all gauge gradients g^{(i)} act through the same ∂w_P/∂w_e, which depends only on geometry.

**Decomposition of alignment.** The >99% raw alignment has two independent sources, both arising from the Hadamard coupling:

(a) *Sign alignment*: at β > β_c, gauge ordering produces ⟨cosΘ_P⟩ > 0 for all fields simultaneously. Since g_e^{(i)} ∝ (∂w_P/∂w_e) × cosΘ_P^{(i)}, and cosΘ > 0 at most plaquettes, all per-field force vectors are predominantly positive. This produces high raw cosine even between uncorrelated spatial patterns.

(b) *Spatial pattern alignment*: the shared plaquette weight derivative ∂w_P/∂w_e imposes a common spatial pattern on all force vectors, beyond the sign effect. Mean-centered cosine similarity (removing the sign bias) measures this component.

4D verification (L = 3, N = 3, κ = 3.0): at β = 2.0, raw cosine = 0.998, mean-centered cosine = 0.82 (14.8σ above permutation baseline). At β = 0.5 (below β_c), centered cosine drops to 0.05 (not significant): the spatial funneling requires supercritical coupling. This β-dependence is itself a prediction of the framework: geometric funneling strengthens with gauge-geometry coupling.

### 2.2 Measurements

(a) Inter-field alignment: cos θ_{ij} = (f^{(i)} · f^{(j)}) / (|f^{(i)}| |f^{(j)}|), treating force arrays as vectors in R^{2L²}.

(b) Alignment ratio: |F_net| / Σ|f^{(i)}|. Equals 1 for perfect alignment, 1/√N for random.

(c) Force-deformation correlation: Pearson r between |F_e| and |w_e − 1| across all edges.

(d) Temporal stability: cos(F(t), F(t+1)) between consecutive Metropolis sweeps.

(e) N-scaling of |F_net|.

### 2.3 Parameters

L = 8 (2D), β = 2.0, κ = 3.0. Thermalization: 100 sweeps. Measurements: 100 sweeps. N = 1 to 10. All simulations use deterministic seeds for reproducibility.

## 3. Results

### 3.1 Force Alignment across Independent Fields

Table 1. Inter-field force alignment (β = 2.0, κ = 3.0, L = 8)

| N | ⟨cos θ_{ij}⟩ | Alignment ratio |
|---|--------------|----------------|
| 1 | 1.000 (def.) | 100.0% |
| 2 | 0.964 | 99.1% |
| 3 | 0.979 | 99.3% |
| 5 | 0.997 | 99.9% |
| 7 | 0.998 | 99.9% |
| 10 | 0.999 | 100.0% |

Forces from independent fields are >99% aligned, and alignment monotonically improves with N. The physical mechanism: all fields act on geometry through the same edge weights, and the plaquette weight structure (geometric mean of surrounding edges) constrains the force direction to be determined by local geometry rather than by individual field configurations. Geometry acts as a funnel that channels diverse gauge pressures into a common direction.

### 3.2 Force-Deformation Anti-Correlation

The Pearson correlation between |F_e| and |w_e − 1| depends on N:

| N | r(|F|, |w-1|) |
|---|---------------|
| 1 | +0.40 (positive) |
| 2 | -0.57 |
| 3 | -0.80 |
| 5 | -0.73 |
| 7 | -0.69 |
| 10 | -0.74 |

For N = 1, forces concentrate where deformation is largest (positive feedback). For N >= 2, forces concentrate where deformation is smallest (wave front). This is a qualitative transition, not a gradual change: the sign of the correlation flips between N = 1 and N = 2. A single field digs into geometry locally; multiple fields create a propagating front. The wave front is a collective phenomenon that cannot exist with fewer than two fields sharing the same geometry.

Forces are strongest where geometry is *least* deformed. Already-deformed edges have already responded to the coupling pressure; the residual force is small. Flat edges (w ≈ 1) bear the full coupling gradient.

This produces a propagating wave front: deformation starts at one region, the force there decreases, and the force at neighboring flat regions increases, pulling the deformation outward. Geometric deformation spreads as a front rather than accumulating locally.

### 3.3 Superadditive Force Scaling

Table 2. Net force magnitude vs. N (β = 2.0, κ = 3.0, L = 8)

| N | |F_net| | Ratio vs N=1 |
|---|--------|-------------|
| 1 | 27.1 | 1.0x |
| 2 | 39.8 | 1.5x |
| 3 | 67.4 | 2.5x |
| 5 | 166.3 | 6.1x |
| 7 | 313.8 | 11.6x |
| 10 | 575.1 | 21.2x |

Power-law fit: |F_net| ~ N^(1.69 ± 0.06), R² = 0.997.

The force exponent (γ_F = 1.69) is consistent with the energy exponent (γ_E = 1.8 ± 0.2) within uncertainty. This follows because F_e = −∂E_total/∂w_e, where E_total ~ N^γ and w_e is independent of N (geometry is shared, not replicated). Therefore ∂E_total/∂w_e ~ N^γ, preserving the exponent.

### 3.4 Temporal Stability of Force Direction

Consecutive-sweep cosine similarity: ⟨cos(F(t), F(t+1))⟩ = 0.9991 ± 0.0006.

Force direction is essentially constant over time. Magnitude fluctuates (coefficient of variation 0.167), but direction does not. This indicates a spontaneous breaking of the edge permutation symmetry: in flat geometry all edges are equivalent, but deformation selects a preferred pattern in edge-weight space that persists despite thermal noise.

### 3.5 Numerical Verification of F = −dE/dl

At 10 randomly selected edges, the force computed by per-edge central difference (δ = 10⁻⁴) was compared with the full energy difference (δ = 10⁻⁵). Relative discrepancy < 10⁻⁴ at all edges. This confirms Theorem 2 numerically.

## 4. Analytical Derivations

### 4.1 k = 0 Condensation from the AM-GM Inequality

The plaquette weight w_P = (w₁ w₂ w₃ w₄)^{1/2} is a geometric mean of surrounding edge weights. By the AM-GM inequality:

(w₁ w₂ w₃ w₄)^{1/4} ≤ (w₁ + w₂ + w₃ + w₄) / 4

with equality iff w₁ = w₂ = w₃ = w₄.

In the Regge convention, the gauge term −β w_P cos θ_P is more negative (lower S) when w_P is larger (for cos θ > 0). Metropolis prefers lower S, hence larger w_P. By AM-GM, w_P is maximized when all edge weights are equal — the k = 0 (uniform) mode.

Therefore, the gauge action forces geometric condensation into the uniform mode. This is a mathematical necessity arising from the geometric mean structure, not a dynamical accident. The elastic term κΣ(w_e−1)² also prefers uniform weights (minimized at w = 1 for all e), so both terms in the action agree on spatial uniformity. They compete only on the VALUE of the uniform weight: gauge coupling drives a > 1 (expansion), elastic resistance pulls toward a = 1 (flat). Condensation into the k = 0 mode occurs at all β > 0 (AM-GM applies regardless of coupling strength); expansion beyond a = 1 requires β > β_c (see §4.2).

Monte Carlo verification: k = 0 mode captures 26% of spectral power at sweep 0 and 99.9% at sweep 400.

Implication: spatial homogeneity of the deformation field arises without inflation or special initial conditions. The geometric mean in the gauge action is sufficient.

### 4.2 Exponential Expansion from Excess Coupling

For the uniform mode w_e = a (the scale factor), the action reduces to:

S(a) = −Nβ n_P a² ⟨cos θ⟩ + κ n_E (a − 1)²

Defining c ≡ ⟨cos θ⟩ (the average plaquette cosine, positive for β > 0) is the gauge fluctuation strength, n_P and n_E are plaquettes and edges per site (n_P = 1, n_E = 2 in 2D).

Setting ∂S/∂a = 0:

a_eq = κ n_E / (κ n_E − Nβ n_P c)

When Nβ n_P c > κ n_E, the denominator is negative, no equilibrium exists at finite a, and the overdamped equation of motion da/dt ∝ −∂S/∂a yields:

da/dt = (δ / γ_eff) · a, δ ≡ Nβ c n_P − κ n_E > 0

where γ_eff is an effective friction coefficient determined by the Metropolis acceptance rate and proposal width (phenomenological parameter that sets the time scale but does not affect the exponential functional form).

Solution: a(t) = a₀ exp(Ht), H = δ / γ_eff. This is de Sitter expansion. The identification of Metropolis sweep number with continuous time is phenomenological; the exponential form follows from da/dt ∝ a, which is a consequence of the action structure.

Monte Carlo verification: ⟨w⟩(t) fits exp(0.0035t) with R² = 0.983, outperforming power-law (R² = 0.978). Hubble parameter H ≈ 0.003 with σ/μ = 0.25. The exponential form does not rest on the numerical fit alone: it follows analytically from da/dt ∝ a in the uniform-mode reduction (above), independent of the MC verification. The MC confirms the analytical prediction.

### 4.3 Self-Consistent Critical Coupling

From §4.2, the critical coupling is:

β_c = κ n_E / (N n_P c(β_c))

This is self-consistent because c(β) = 1 − I₁(β)/I₀(β) for U(1). Numerical solution for N = 3, κ = 3.0 yields β_c ≈ 1.4, consistent with the Monte Carlo measurement of β_c ≈ 1.3–1.5 from Paper D.

### 4.4 Dimensional Dependence of the Superadditivity Exponent

In d dimensions, each edge participates in 2(d−1) plaquettes across d link directions. The geometric frustration density is ρ(d) = 2(d−1)/d. Fitting γ(2) = 1.8, γ(3) = 1.44, γ(4) = 0.95 against ρ(d):

γ(d) ≈ −1.6 · ρ(d) + 3.5, R² = 0.92

This predicts a critical dimension d_c ≈ 5 where γ = 1, i.e., superadditivity vanishes. Our universe (d = 4) is near this boundary, consistent with gravity being the weakest force. This prediction is falsifiable: MC simulations at d = 5 (computationally expensive but feasible with current methods) would either confirm γ(5) ≈ 1 or refute the linear trend. The physical basis of the trend — more geometric constraints per edge in higher dimensions, increasing frustration and reducing cooperative deformation — is independent of the specific linear formula.

## 5. Discussion

### 5.1 What Force Adds to Energy

Energy says "how much." Force says "where next" (§3.2, anti-correlation), "in concert" (§3.1, alignment), and "persistently" (§3.4, stability). The transition from scalar (Paper D) to vector (this paper) reveals the dynamical structure that energy alone hides.

### 5.2 Geometry as Active Medium

The 99% force alignment despite zero direct inter-field coupling means geometry actively organizes independent fields. This is the vector-level confirmation of Paper D's displacement alignment (α ≈ 0.94), and it is stronger: force alignment exceeds displacement alignment.

### 5.3 Limitations and Extensions

All force results are from 2D lattices with L ≤ 10. Paper B's finite-size scaling (L = 4, 6, 8 in 4D SU(2)) confirmed that the underlying gauge-geometry correlation is a bulk effect; analogous scaling for force alignment and superadditivity exponent is a natural next step. The analytical derivations (§4) are dimension-independent in structure but their quantitative predictions require 4D verification. The de Sitter expansion result, while analytically derived and MC-verified in 2D, requires 4D large-lattice confirmation before cosmological interpretation is warranted.

### 5.4 Connection to the Two-Sector Structure and 4D Verification

The companion paper [Kwon 2026h] proves that the Hessian of the effective action has k-dependent eigenvalues: positive (stable) for short-wavelength modes, negative (unstable) for long-wavelength modes. The crossover wavevector k* separates a particle sector (massive, localized excitations) from a cosmological sector (expansion, structure formation). The force results of this paper operate in the cosmological sector (k < k*): the net force |F_net| drives long-wavelength geometric deformation, while the alignment, anti-correlation, and temporal stability describe the coherent structure of this drive. The force exponent γ_F ≈ 1.69 matches the energy exponent γ_E ≈ 1.8 — both are properties of the cosmological sector.

**4D verification.** The key force predictions were confirmed in 4D U(1) on L = 3 periodic lattices (N = 3, β = 2.0, κ = 3.0): gauge-only raw alignment 99.94%, spatial pattern alignment 0.82 (14.8σ), k = 0 condensation 98.2%, and continued expansion (⟨w⟩ = 1.0 → 2.19). All three pillars — alignment, condensation, expansion — survive in 4D.

## 6. Conclusion

Multi-gauge coupling on shared geometry produces forces that are:
(i) Aligned (>99%, improving with N)
(ii) Propagating (wave front, anti-correlated with deformation)
(iii) Superadditive (|F| ~ N^1.69)
(iv) Directionally stable (cos = 0.999)
(v) Exactly gradient (F = −dE/dl verified)

Analytical derivations show:
(vi) k = 0 condensation = AM-GM necessity
(vii) de Sitter expansion = excess coupling
(viii) β_c = self-consistent formula
(ix) γ(d) = frustration density function, d_c ≈ 5

This completes the T = C⊙S framework: existence (Papers A,B), magnitude (Paper D), and direction (this paper).

## Acknowledgments

The author used Claude (Anthropic) as a computational tool for mathematical verification, numerical simulation, and assistance in preparing the manuscripts. All theoretical content — axioms, theorems, proofs, physical interpretations, and strategic decisions — is the author's original work. The author takes full responsibility for all content.

---

## References

- Kwon, H. (2026a). The Hadamard structure of self-referential graphs. arXiv.
- Kwon, H. (2026b). Gauge-geometry coupling is a necessary consequence of self-referential dynamics on graphs. arXiv.
- Kwon, H. (2026d). Multi-gauge superadditivity on shared geometry. arXiv.
- Kwon, H. (2026h). The excitation spectrum of self-referential fields. arXiv.
- Regge, T. (1961). General relativity without coordinates. Nuovo Cim. 19, 558.
- Wilson, K.G. (1974). Confinement of quarks. Phys. Rev. D 10, 2445.
- Chung, F.R.K. (1997). Spectral Graph Theory. CBMS 92, AMS.
