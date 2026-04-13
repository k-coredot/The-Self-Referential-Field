# Emergent Matter from a Self-Referential Field

Hyeokjun Kwon — April 2026

---

**Abstract.** A field that reads itself — formalized as the unique Hadamard operator T = C⊙S (Kwon 2026a) — necessarily produces matter. We show that the two structural conditions for a well-defined self-reading cycle (elastic restoring force κ > 0 and gauge content β > 0) together guarantee: (i) a spectral mass gap m ∈ (0, ∞), (ii) topologically protected excitations, (iii) exponential localization of disturbances, and (iv) a characteristic scale for structure formation. These are the four ingredients of a particle. Monte Carlo simulations on 2D dynamical lattices with U(1) gauge fields confirm each prediction: exponential correlator decay (m ≈ 0.2–0.4), vortex conservation (1.3% change rate), soliton stability (energy concentration 15× after 60 sweeps), geometric condensation (96.5% in k = 0), and a crossover near k = 3. The numerical results confirm the predictions; the argument does not rest on them.

---

## 1. One Axiom

A field exists. It reads itself. Reading deforms the field. The deformed field is read again.

This axiom — the complete content of the framework — forces the unique edge operator T = C⊙S, where C = ⟨φ_a, φ_b⟩ (state comparison, gauge content) and S = (D^{-1/2}AD^{-1/2})_{ab} (structural propagation, geometry). The uniqueness proof is in Paper A: locality, rotational invariance, self-adjoint spectral consistency, and variational stability exclude all alternatives.

T is a Hadamard (elementwise) product. The value at each edge is a single number — the product of gauge content and geometric structure. This product cannot be uniquely factored. The field is one entity, not two coupled sectors.

Paper B verified this inseparability across 42 configurations spanning 2D–4D, U(1) and SU(2), with all measurements significant at 13σ or above.

## 2. Two Conditions

For the self-reading cycle to be stable, deformation must have a restoring force. Without it, reading → deformation → larger deformation → divergence. The cycle blows up. Call this restoring force κ.

For the reading to carry information, the field must have varying content. Without it, every location is identical and there is nothing to read. Call this content β.

These are not adjustable parameters. They are the minimum conditions for the axiom to define a well-posed, non-trivial dynamics. If κ = 0, the partition function diverges (Proposition 1, companion paper). If β = 0, all correlations vanish (Proposition 2, companion paper).

The action is:

S = −Nβ Σ_P w_P cos Θ_P + κ Σ_e (w_e − 1)²

The first term is T = C⊙S applied to the lattice. The second is the elastic cost of deformation. N is the number of independent gauge fields sharing the geometry.

## 3. Four Necessities

### 3.1 Mass

κ > 0 provides a restoring force for each edge weight. Any excitation — departure from the ground state — costs energy proportional to κ. The minimum energy is m > 0. Excitations are massive.

β > 0 couples neighboring edges through the plaquette term w_P cos Θ_P. Excitations propagate from site to site. The correlation length is finite: m < ∞.

Therefore m ∈ (0, ∞): every excitation of the field has finite, nonzero mass. This is the spectral gap.

More precisely: the Hessian of the effective action (after integrating out gauge angles) has k-dependent eigenvalues. Short-wavelength modes (large k) are always gapped because the elastic confinement 2κ dominates the gauge coupling, which is attenuated by plaquette averaging. The companion paper (H Math) proves that for all modes with wavevector |k| > k* (the crossover scale), the spectral mass m(k) > 0. In the subcritical regime (β < β_c), k* = 0 and ALL modes are gapped. In the supercritical regime (β > β_c), modes with k < k* are unstable — these are the expansion modes of §3.4, not particle excitations.

The physical content: creating a disturbance in the field costs energy. The disturbance can travel, but it decays exponentially over a distance ξ = 1/m. This is the field-theoretic definition of a massive particle.

No Higgs field is introduced. The mass arises from the elastic response of the field to its own fluctuations — κ resists deformation, β couples deformation to gauge content, and the competition sets the mass scale.

**Confirmation.** The geometric correlator G(r) = ⟨δw(0)δw(r)⟩ shows exponential decay at β ≥ 5.0 across lattice sizes L = 12–24, with m_∞ ≈ 0.2–0.4. The finite-size variation (cv ≈ 0.3) reflects measurement precision, not the existence of the gap.

### 3.2 Protection

On a periodic lattice, the total plaquette winding number Q = Σ W_P = 0 for every configuration (Stokes' theorem on a torus). Under any single-link Metropolis update, the winding numbers of the two affected plaquettes change by equal and opposite amounts. The total is invariant.

This is topological, not dynamical. It holds regardless of β, κ, temperature, or any other parameter. An excitation carrying nonzero winding number cannot decay to the vacuum through any sequence of local updates.

The physical content: some excitations carry a conserved quantum number. They are permanent — they cannot disappear. This is the analog of charge conservation.

**Confirmation.** Total topological charge fluctuates with std < 1 over 300 sweeps. Vortex count changes in 1.3% of sweeps. Vortex lifetime exceeds all simulation times.

### 3.3 Localization

If m > 0, a localized perturbation of size R generates a response that decays as exp(−mr) outside the region of size R + ξ. The disturbance cannot spread to infinity. It stays localized, losing energy slowly to the surrounding field.

This is a direct mathematical consequence of the spectral gap (Corollary 1, companion paper). It requires no additional mechanism.

The physical content: particles have finite size. They sit somewhere. They do not instantly dissolve into the vacuum.

**Confirmation.** A 3×3 perturbation on a thermalized L = 16 lattice retains energy concentration 15.9× after 60 sweeps. Center-of-mass displacement < 0.3 sites. Internal vibrational modes observed for weak perturbations.

### 3.4 Structure

The plaquette weight w_P = (∏ w_e)^{1/2} is the plaquette area measure — the square root of the product of surrounding edge weights. By the AM-GM inequality, it is maximized when all edge weights are equal. The gauge action prefers larger w_P (for cos Θ > 0). Therefore the field condenses into the uniform mode: k = 0 absorbs the dominant fraction of spectral power.

But AM-GM is a strict inequality. Fluctuations persist.

When N ≥ 2 fields share one geometry, the multiplicative coupling creates positive feedback: deformation by one field increases w_P, which strengthens the coupling for all fields. Energy grows superadditively: E ~ N^γ, γ > 1. If the total coupling exceeds elastic resistance, the uniform mode grows — the field expands.

Expansion drives k = 0 growth. Elasticity suppresses short wavelengths. Between them, the intermediate value theorem guarantees a crossover wavenumber k* where the growth rate changes sign. Perturbations below k* grow into structure. Above k*, they are damped.

The physical content: a perfectly uniform field is unstable. Structure at a characteristic scale forms spontaneously. This is the Jeans instability of the gauge-geometry field.

The crossover scale k* separates two sectors of the theory: below k*, modes are unstable and drive expansion and structure (cosmology); above k*, modes are gapped and produce massive, localized excitations (particles). Both sectors arise from the same action. The existence of k* is a theorem (intermediate value theorem applied to the k-dependent Hessian eigenvalue, see H Math companion paper). The same framework that produces matter (§3.1–3.3) also produces cosmology (§3.4) — they are not independent theories but two sectors of one spectrum.

**Confirmation.** k = 0 mode absorbs 96.5% of spectral power. ⟨w⟩: 1.0 → 2.58. Superadditivity: R(N=5) = 4.48, γ = 2.28. Crossover near k = 3 (mean growth ratio 1.32). All seed-independent (CV = 0.01).

## 4. One Consequence

Mass (§3.1) + protection (§3.2) + localization (§3.3) + structure (§3.4). These are the defining properties of matter: massive, stable, finite-size excitations in a structured geometry. All four are necessary consequences of T = C⊙S with κ > 0 and β > 0.

On any graph where a field reads itself with elastic response — a lattice, a network, a discretized manifold — these four properties hold. The excitations of that field are particles. Their mass is set by κ and β. Their stability is set by topology. Their size is set by ξ = 1/m. Their spatial arrangement is set by the Jeans scale k*.

This is not a model. It is a derivation. The axiom determines the operator. The operator determines the action. The action determines the spectrum. The spectrum contains matter.

## 5. What Remains

The derivation of existence is complete: mass gap, topological conservation, localization, spinor selection, and continuum limit are all proven. The remaining questions are quantitative:

(i) **Specific mass values.** The mass gap exists in any dimension, but its numerical value m(β, κ, d) depends on the coupling constants. Determining whether m corresponds to known particle masses requires fixing β/κ — which may be determined by the self-referential fixed point (see Discussion).

(ii) **Grassmann statistics.** Theorem 7 proves the axioms select the spinor REPRESENTATION (half-integer spin). Full fermionic STATISTICS (anti-commutation) requires the spin-statistics theorem, which follows from Osterwalder-Schrader reflection positivity in Euclidean lattice theory. OS reflection positivity is proven for the full dynamical-geometry Hadamard action (I Math, Theorem 6). Spin-statistics follows unconditionally (I Math, Theorem 7).

(iii) **The value of ℏ.** The complex action (forced by the spinor) introduces a phase exp(−iS). The scale of the phase — Planck's constant — sets the boundary between classical and quantum behavior. Whether ℏ is determined by the self-referential fixed point or is a free parameter is the deepest open question.

These are questions about which universe, not whether a universe.

## 6. The Series

| Paper | What | Why |
|-------|------|-----|
| A | T = C⊙S | Uniqueness: the only variationally stable self-referential operator |
| B | One field | Inseparability: C and S are one entity, verified 42×, ≥13σ |
| C | Noise gating | The Hadamard product gates noise: C ≈ 0 ⟹ T ≈ 0 |
| D | Superadditive energy | Multiplicative coupling + shared geometry → E ~ N^γ |
| F | Coherent force | Shared geometry funnels independent fields into alignment |
| G | Spacetime | AM-GM → condensation; excess coupling → expansion |
| **H** | **Matter** | **Mass, protection, localization, spinor selection, continuum limit** |

One axiom. One operator. One field. Energy, force, spacetime, matter.

The field is one. Its excitations are matter. The axioms select the spinor representation — fermions are not added but derived. The UV mass gap is exact — the continuum limit is trivial. The question is not whether gauge binds to geometry — they were never apart.

## Methods

2D periodic lattice, L = 10–24. N = 1–5 independent U(1) gauge fields. Metropolis algorithm alternating gauge link and edge weight updates. Elastic stiffness κ = 3.0 unless noted. Deterministic seeds with multi-seed verification (5–10 seeds for key results). Decorrelation interval ≈ 2τ_int for independent measurements. Bootstrap errors for mass gap extraction. Source code provided as supplementary material.

## Acknowledgments

The author used Claude (Anthropic) as a computational tool for mathematical verification, numerical simulation, and assistance in preparing the manuscripts. All theoretical content — axioms, theorems, proofs, physical interpretations, and strategic decisions — is the author's original work. The author takes full responsibility for all content.

---

## References

- Kwon, H. The Hadamard structure of self-referential graphs. arXiv (2026a).
- Kwon, H. Gauge-geometry coupling from self-referential dynamics. arXiv (2026b).
- Kwon, H. Multiplicative coupling in GNNs. arXiv (2026c).
- Kwon, H. Superadditive energy from multi-gauge coupling. arXiv (2026d).
- Kwon, H. Superadditive forces from multi-gauge coupling. arXiv (2026f).
- Kwon, H. Emergent cosmology from gauge-geometry coupling. arXiv (2026g).
- Kwon, H. The excitation spectrum of self-referential fields. arXiv (2026h).
- Regge, T. General relativity without coordinates. Nuovo Cim. 19, 558 (1961).
- Wilson, K.G. Confinement of quarks. Phys. Rev. D 10, 2445 (1974).
- Ambjorn, J., Jurkiewicz, J. & Loll, R. Reconstructing the universe. Phys. Rev. D 72, 064014 (2005).
- Hamber, H.W. Quantum Gravitation. Springer (2009).
