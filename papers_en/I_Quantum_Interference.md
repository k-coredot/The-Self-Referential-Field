# Quantum Interference from Self-Referential Spinor Structure

Hyeokjun Kwon — April 2026

---

**Abstract.** The axioms of self-referential field dynamics (Kwon 2026a) force the fundamental representation j = 1/2 of non-abelian gauge groups (Kwon 2026h, Theorem 7). The node states are then spinors ψ ∈ ℂ². This has a consequence that was not anticipated: the content similarity C = ⟨ψ_a, ψ_b⟩ is complex-valued, forcing the operator T = C ⊙ S, the action, and the Gibbs weight into the complex domain. The complex Gibbs weight exp(−S) = exp(−Re S) · exp(−i Im S) produces interference: configurations with aligned phases reinforce, those with opposing phases cancel. The complex Hessian h(k) = h_R + ih_I gives excitations that simultaneously decay (localized, particle-like) and oscillate (propagating, wave-like). Both quantum interference and wave-particle unity are derived, not postulated. The logical chain is: self-reference → faithful reading → spinor (Theorem 7) → ℂ² → complex inner product → complex action → interference → wave-particle unity. Every step is forced.

---

## 1. The Chain

Theorem 7 of the companion paper (Kwon 2026h) proves that among all representations of SU(2), the axioms uniquely select j = 1/2. The proof has two stages: integer representations have χ'(0) = 0 (blind spot, excluded by regularity), and higher half-integer representations have χ'(0) < 0 (sign inversion, excluded by fixed-point existence). The surviving representation has node states ψ ∈ ℂ².

This paper develops the consequences of ψ ∈ ℂ² for the structure of the theory.

## 2. Complex Content

The content similarity between two spinor states is:

    C_{ab} = ⟨ψ_a, ψ_b⟩ = ψ_a† ψ_b ∈ ℂ

This is complex. The real part Re(C) measures alignment. The imaginary part Im(C) measures the phase difference between the two spinors.

If the operator reads only Re(C), two configurations differing only in Im(C) produce the same T. The reading loses information. The field has changed but the operator does not notice. This violates faithful self-reference.

Therefore T = C ⊙ S ∈ ℂ. The operator is complex-valued.

## 3. Complex Action

The action S = −Nβ Σ_P w_P C_P + S_el[w], where C_P is the plaquette content. With C_P ∈ ℂ:

    S = S_R + iS_I

where S_R = −Nβ Σ w_P Re(C_P) + S_el and S_I = −Nβ Σ w_P Im(C_P).

The Gibbs weight:

    exp(−S) = exp(−S_R) · exp(−iS_I)

The first factor is real and positive — it determines the probability (how likely a configuration is). The second factor is a pure phase — it determines the direction in the complex plane.

## 4. Interference

The partition function is Z = Σ_{configs} exp(−S). Each configuration contributes a complex number to the sum. The magnitude |exp(−S_R)| determines how large the contribution is. The phase exp(−iS_I) determines which direction it points.

When two configurations have the same phase (S_I^{(1)} ≈ S_I^{(2)}), their contributions point in the same direction and add constructively. When they have opposite phases (S_I^{(1)} ≈ S_I^{(2)} + π), their contributions point in opposite directions and cancel.

This is interference. It is the arithmetic of adding complex numbers.

In a real-valued theory (scalar node states φ ∈ ℝ^d, C ∈ ℝ): all contributions are real and positive. No cancellation. No interference. Classical statistics.

In a complex-valued theory (spinor node states ψ ∈ ℂ², C ∈ ℂ): contributions have phases. Cancellation is possible. Interference exists. Quantum statistics.

The transition from classical to quantum is the transition from real to complex content, which is the transition from vector to spinor, which is forced by the axioms.

## 5. Wave-Particle Unity

The Hessian of the complex action is complex:

    h(k) = h_R(k) + ih_I(k)

The response to a localized perturbation:

    G(r) ~ exp(−√h_R · r) · exp(−i√h_I · r)

The first factor: exponential decay. The perturbation is localized within a region of size ξ = 1/√h_R. It does not spread to infinity. It has finite extent. This is the particle aspect.

The second factor: oscillation. The perturbation has a spatial frequency ω = √h_I. It propagates as a wave. It has wavelength λ = 2π/ω. This is the wave aspect.

Both aspects are contained in a single complex number h(k). They are not two separate properties but two parts (real and imaginary) of one property. The "duality" is the decomposition of a complex number into magnitude and phase.

At h_I = 0 (real Hessian, real action, real content, vector states): the excitation decays without oscillating. Pure particle. No wave character. This is the classical limit.

At h_R → 0 (near the crossover k*): the excitation oscillates without decaying. Pure wave. No particle character. This is the massless limit.

In between: both decay and oscillation. Localized wave. Particle-wave.

## 6. The Logical Necessity

The chain is:

    Self-reference
    → faithful reading (∂f/∂C|_0 finite, nonzero)
    → regularity excludes integer j (blind spot at C = 0)
    → sign preservation excludes j ≥ 3/2 (oscillation, no fixed point)
    → j = 1/2 (unique survivor)
    → ψ ∈ ℂ²
    → C = ⟨ψ_a, ψ_b⟩ ∈ ℂ (faithful reading of both components)
    → T ∈ ℂ, S ∈ ℂ
    → exp(−S) = |magnitude| × phase
    → interference (phase cancellation in sums)
    → complex h(k) = h_R + ih_I
    → decay × oscillation
    → wave-particle unity

No step is optional. No step introduces a new assumption. The entire chain follows from the definition of self-reference and the evaluation of 0^{α−1} and χ'(0).

## 7. What This Does Not Determine

The complex structure produces interference but does not determine its scale. In standard physics, the scale of quantum effects is set by Planck's constant ℏ: the phase is exp(iS/ℏ), and ℏ determines where quantum effects become important.

In this framework, the phase is exp(−iS_I) where S_I = Nβ Σ w_P Im(C_P). The scale of the phase is set by β and the typical values of Im(C_P). Whether this naturally produces a small parameter analogous to ℏ is an open question.

What is determined: the existence of interference, the existence of wave-particle unity, and the logical chain that produces them. What is not determined: the quantitative scale of quantum effects.

## 8. Connection to the Series

Paper A proves T = C ⊙ S. Paper B verifies it. Paper H (Math) proves j = 1/2 (Theorem 7). This paper develops the consequence: j = 1/2 forces ℂ, which forces interference.

The transition from Papers A–G (real content, classical statistics) to Papers H–I (complex content, quantum statistics) is not a change of framework. It is the same framework applied to the non-abelian case. The axioms are identical. The representation changes because the gauge group changes. Everything else follows.

---

## Acknowledgments

The author used Claude (Anthropic) as a computational tool for mathematical verification, numerical simulation, and assistance in preparing the manuscripts. All theoretical content — axioms, theorems, proofs, physical interpretations, and strategic decisions — is the author's original work. The author takes full responsibility for all content.

---

## References

- Kwon, H. The Hadamard structure of self-referential graphs. arXiv (2026a).
- Kwon, H. Gauge-geometry coupling from self-referential dynamics. arXiv (2026b).
- Kwon, H. The excitation spectrum of self-referential fields. arXiv (2026h).
- Feynman, R.P. Space-time approach to non-relativistic quantum mechanics. Rev. Mod. Phys. 20, 367 (1948).
- Osterwalder, K. & Schrader, R. Axioms for Euclidean Green's functions. Commun. Math. Phys. 31, 83 (1973).
- Dirac, P.A.M. The quantum theory of the electron. Proc. R. Soc. Lond. A 117, 610 (1928).
- Nelson, E. Derivation of the Schrödinger equation from Newtonian mechanics. Phys. Rev. 150, 1079 (1966).
- Osterwalder, K. & Seiler, E. Gauge field theories on a lattice. Ann. Phys. 110, 440 (1978).
- Wilson, K.G. Confinement of quarks. Phys. Rev. D 10, 2445 (1974).
- Wetterich, C. Quantum mechanics from classical statistics. Ann. Phys. 325, 852 (2010).
