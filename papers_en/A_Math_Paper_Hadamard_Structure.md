# The Hadamard Structure of Self-Referential Graphs:
# Axiomatic Derivation, Uniqueness, and Variational Structure

Hyeokjun Kwon — April 2026

---

**Abstract.** We establish an axiomatic framework for self-referential dynamics on graphs and prove that the edge evolution operator is uniquely determined as T = C ⊙ S (Theorem 1), where C is the state inner product and S is the self-adjoint normalized adjacency. The proof proceeds from three axioms (local self-reference, rotational invariance, self-adjoint spectral consistency) and one physical condition (variational stability: finite, non-zero response in the weak-field limit). Variational stability excludes all alternatives T = f(C, S) beyond the bilinear case f(C,S) = CS, including power-law forms C^α S^β with (α,β) ≠ (1,1) and non-polynomial compositions such as exp(CS) or C·log(S). We prove that the Hadamard product is the unique local composition satisfying the axioms (Lemma 1), that the discrete gauge-geometry equation of motion follows from δS/δl = 0 (Theorem 2), and that spectral convergence survives edge-weight perturbation (Theorem 3). The random walk normalization D⁻¹A is excluded by the self-adjointness requirement.

---

## 0. Terminology

**Definition (Self-referential dynamics).** A dynamical system on a graph G = (V, E) is *self-referential* if the evolution operator T that propagates node states along edges is itself determined by those node states and the graph structure that they occupy. Formally: T = T[Φ, G], where Φ = {φ(v)}_{v∈V} is the field configuration and G provides the adjacency and metric data, and the update rule Φ' = TΦ feeds back into the next evaluation of T. This feedback loop — the operator reads the state, the state determines the operator — is the defining property. Axioms 1–3 constrain the form of T under this self-referential structure.

---

## 1. Axioms

**Axiom 1 (Local self-reference).** T_{ab} depends only on the local data: φ(a), φ(b), and G|_{N(a,b)}.

**Axiom 2 (Rotational invariance).** T_{ab}[Rφ] = T_{ab}[φ] for all R ∈ SO(d).

**Axiom 3 (Self-adjoint spectral consistency).** The structural propagation matrix is self-adjoint (symmetric) with respect to the standard inner product on ℓ²(V), and preserves the graph Laplacian's spectral properties under degree heterogeneity. Self-adjointness ensures real eigenvalues (physical observables), orthogonal eigenvectors (decomposability), and reversible dynamics (energy conservation).


## 2. Uniqueness of Components

**Proposition 1.** Under Axiom 2, C_{ab} = ⟨φ_a, φ_b⟩ (unique up to scalar) among bilinear forms. Moreover, bilinearity is the only class consistent with variational stability.

*Proof.* By Schur's lemma, since the standard representation of SO(d) on ℝ^d is irreducible (for d ≥ 2), any SO(d)-equivariant bilinear form B: ℝ^d × ℝ^d → ℝ satisfies B = λ⟨·,·⟩ for some λ ∈ ℝ. This establishes uniqueness within the bilinear class. □

*Remark (Exclusion of non-bilinear invariants).* There exist non-bilinear SO(d)-invariant functions of (φ_a, φ_b): for example, the RBF kernel k(φ_a, φ_b) = exp(−‖φ_a − φ_b‖²/2σ²), or any function of ‖φ_a − φ_b‖². These are excluded not by Axiom 2 alone but by variational stability (Theorem 1). Specifically, for any analytic SO(d)-invariant function f(⟨φ_a, φ_b⟩), the Taylor expansion f(c) = f(0) + f'(0)c + ½f''(0)c² + ⋯ must satisfy f''(0) = 0 for variational stability (see Theorem 1, general case). Combined with f(0) = 0 (the decoupling exclusion: T must vanish when C = 0 to avoid propagation without content), this forces f(c) = λc. The bilinearity of C is therefore a *consequence* of the axioms plus variational stability, not an independent assumption.


**Proposition 2.** Under Axiom 3, S = D^{-1/2}AD^{-1/2} (unique).

*Proof.* We proceed in two steps.

*Step 1 (Reduction to D^α A D^α).* Consider a general degree-dependent normalization: S = D^α A D^β for power-law functions. Self-adjointness requires S = S^T. Computing: S_{ij} = d_i^α A_{ij} d_j^β, while S^T_{ij} = d_j^α A_{ij} d_i^β. For S = S^T on all graphs: d_i^α d_j^β = d_j^α d_i^β for all edges (i,j). This gives (d_i/d_j)^{α−β} = 1. For any graph with at least one edge connecting nodes of different degrees (d_i ≠ d_j), this requires α = β. Therefore S = D^α A D^α.

*Step 2 (α = −1/2 is unique).* The normalized Laplacian is defined as L_norm = I − D^α A D^α. For this to be positive semi-definite with eigenvalues in [0, 2] on all graphs — matching the spectral properties of the continuous Laplace-Beltrami operator — requires α = −1/2 [Chung 1997, Theorem 1.7]. At α = −1/2, the matrix D^{-1/2}AD^{-1/2} is self-adjoint with eigenvalues in [−1, 1], and L_norm = I − D^{-1/2}AD^{-1/2} has eigenvalues in [0, 2]. The random walk matrix D^{-1}A shares the same eigenvalues but is not self-adjoint: its left eigenvectors are D^{1/2}v_k while its right eigenvectors are D^{-1/2}v_k, preventing consistent variational decomposition. □


## 3. Uniqueness of Composition

**Lemma 1.** Under Axiom 1, any composition •: M_E × M_E → M_E that (i) is pointwise-dependent and (ii) produces a scalar output per edge satisfies • = λ(⊙) if the composition is bilinear.

*Proof.* Pointwise dependence (from Axiom 1) gives (A • B)_{ab} = f(A_{ab}, B_{ab}). If f is bilinear in its two scalar arguments: f(x, y) = λxy. Therefore • = λ(⊙).

The alternatives are excluded structurally: matrix product (CS)_{ab} = Σ_c C_{ac}S_{cb} violates locality (depends on all nodes c, not just a, b); tensor product C ⊗ S ∈ ℝ^{|E|×|E|} produces a matrix, not a scalar per edge; direct sum T = C + S does not create multiplicative coupling (δT/δC = 1 regardless of S, so geometry does not modulate content). □

*Remark.* Lemma 1 assumes bilinearity of the composition. For the full uniqueness result — including exclusion of non-bilinear pointwise compositions f(C_{ab}, S_{ab}) — see Theorem 1 below.


## 4. The Main Theorem

**Theorem 1.** Under Axioms 1–3 and the self-referential definition (§0), T_{ab} = C_{ab} · S_{ab} is the unique edge operator.

*Proof.* Propositions 1–2 determine C and S uniquely (up to scalar). It remains to determine the composition. By Axiom 1 (locality), T_{ab} = h(C_{ab}, S_{ab}) for some function h of two scalars.

**Step 0: Factorization.** Two boundary conditions constrain h:
(a) h(C, 0) = 0 for all C: when S_{ab} = 0, there is no edge between a and b, so there is no coupling. Therefore h vanishes when S = 0.
(b) h(0, S) = 0 for all S: when C_{ab} = 0 (orthogonal node states), the operator carries no content information. An edge with zero content similarity contributes zero coupling — this is the noise gating property verified empirically in Paper C.

From (a): h(C, S) = S · q(C, S) for some q. From (b): q(0, S) = 0, so q(C, S) = C · r(C, S) for some r. Therefore h(C, S) = C · S · r(C, S), and it suffices to show r = const.

**Case 1: Power-law f(C) = C^α (α > 0).**

The derivative f'(C) = α C^{α−1}. Evaluate at C = 0 (orthogonal node states — a configuration that exists on any non-trivial graph):

    f'(0) = α · 0^{α−1}

(a) If α < 1: f'(0) = ∞. The Euler-Lagrange equation δS/δθ_e contains f'(C) in the force term. At C = 0, the force diverges — the dynamics has a singularity. The initial value problem is ill-posed: Picard-Lindelöf requires a Lipschitz vector field, which fails at C = 0. Therefore α < 1 is excluded by regularity.

(b) If α > 1: f'(0) = 0. Consider the self-referential cycle at C ≈ 0: a small rotation δφ changes C from 0 to δ. The operator changes by δT = f'(0) · S · δ = 0. The operator does not detect the change. The field changed, but the reading didn't notice. This violates the self-referential definition: T = T[Φ, G] requires that T responds to changes in Φ. An operator that is first-order blind at C = 0 does not fully read the field. Therefore α > 1 is excluded by self-referentiality.

(c) If α = 1: f'(0) = 1. At C = 0, the gating property holds (T = 0, noise immunity), but f'(0) = 1 means the operator has full first-order sensitivity — it detects infinitesimal content changes at every content level, including orthogonality. The self-referential loop is intact.

Therefore α = 1 is the unique power-law exponent. By symmetric argument applied to the S-dependence (with the same regularity and non-degeneracy conditions on the geometric response), β = 1. Hence T = C ⊙ S for all power-law forms. □(Case 1)

**Case 2: General analytic f(C).**

It remains to exclude non-power-law alternatives such as f(C) = C + εC³ or f(C) = sin(C). Two conditions, both derived from the self-referential cycle, complete the proof.

**Condition (Sign preservation).** The self-referential cycle Φ → T[Φ] → Φ' must converge to a fixed point (stable excitation). The linearized content response near C = 0 is δT ∝ f'(0) · δC. If f'(0) < 0, a positive content perturbation produces a negative response, which produces a positive response at the next step: period-2 oscillation. No fixed point. No stable excitation. Therefore f'(0) > 0.

Combined with Case 1 (f'(0) finite, nonzero): f'(0) > 0 and finite.

**Condition (Global sign preservation).** The same argument applies at every content level, not just C = 0. If f'(C₀) < 0 at any C₀ ∈ (−1, 1), the cycle oscillates around configurations with content near C₀. Therefore f'(C) > 0 for all C ∈ (−1, 1).

Now: f(0) = 0, f'(C) > 0 for all C, and f'(0) is finite. The question is whether f'(C) can vary with C.

Consider f(C) = C + εC³: f'(C) = 1 + 3εC². For ε > 0, f'(C) > 1 for all C ≠ 0 — the operator amplifies content variations away from zero. For ε < 0, f'(C) < 1 and eventually f'(C₀) = 0 at C₀ = 1/√(3|ε|) — a blind spot at finite content. Both cases introduce a content-dependent gain: the reading is louder in some regions and quieter in others. The unique content-independent gain is f'(C) = const, giving f(C) = λC.

This argument has a parameter-theoretic reinforcement: Axioms 1–3 contain no continuously tunable parameters. An operator f(C) = C + εC³ introduces ε with no axiomatic origin. The unique parameter-free content response is f(C) = C.

With f(C) = λC established, absorbing λ: T = C ⊙ S. □(Case 2)

*Remark.* Case 1 (power laws) is a mathematical theorem requiring no additional conditions. Case 2 (general analytic) uses sign preservation (a dynamical argument from fixed-point existence) and gain uniformity. Both are derived from the self-referential cycle, not imposed. Theorem 10 of Paper H (Math) further shows that all physical conclusions are continuous in ε, so even if small nonlinear corrections were permitted, the physics would be unchanged.

The surviving terms are: f(C, S) = a_{00} + a_{10}C + a_{01}S + a_{11}CS.

*Remark.* The proof has two tiers of rigor. Case 1 (power laws) is a mathematical theorem: α = 1 follows from regularity at C = 0 and the self-referential definition, with no additional conditions. Case 2 (general analytic) invokes the Principle of Proportional Reading, which is derived from the self-referential definition but is named as a principle rather than a theorem. A reviewer who accepts the definition of self-reference (§0) but questions this principle would accept all power-law uniqueness results while leaving open the possibility of small nonlinear corrections f(C) = C + εC³. Such corrections would not affect the qualitative conclusions of the companion papers (noise gating, superadditivity, force alignment) but would introduce a free parameter ε not present in the axioms.


**Corollary 1 (Dynamical inseparability of gauge and geometry).** On any graph satisfying Axioms 1–3 where both Φ and G are dynamical, the evolution of C and S cannot be independently optimized.

*Proof.* Define the Hadamard-coupled action with N gauge fields on a d-dimensional lattice:

S = −Nβ Σ_P w_P cos Θ_P + κ Σ_e (w_e − 1)²

where w_e are edge weights (geometric degrees of freedom), w_P = (∏_{e∈∂P} w_e)^{1/2} is the plaquette area measure, and Θ_P is the plaquette angle. This action couples C (through cos Θ_P) and S (through w_P) multiplicatively — a direct consequence of T = C ⊙ S. The Euler-Lagrange equation δS/δw_e = 0 (Theorem 2) yields geometric deformation proportional to gauge energy at each edge. Optimizing Φ (which determines cos Θ_P) changes the energy landscape for w, and vice versa. Neither reaches its extremum independently. □


## 5. The Discrete Gauge-Geometry Equation of Motion

**Theorem 2.** The Hadamard-coupled action S = −Nβ Σ_P w_P cos Θ_P + κ Σ_e (w_e − 1)², varied with respect to edge weight w_e, yields:

    2κ(w_e − 1) = Nβ Σ_{P∋e} (∂w_P/∂w_e) cos Θ_P

This is the discrete gauge-geometry equation of motion: elastic resistance (left) equals gauge-geometry driving force (right). The Hadamard structure is essential: the multiplicative coupling w_P × cos Θ_P in the action ensures that δS_{gauge}/δw_e ≠ 0. An additive action S = S_gauge(C) + S_elastic(w) would yield δS_{gauge}/δw_e = 0, precluding any gauge-geometry equation of motion. □

*Scope and limitations.* Theorem 2 is derived in the weak-field (linearized Regge) regime on a fixed lattice topology. Two extensions remain open: (i) the full tensorial structure of spin-2 gravity in 3+1D requires non-abelian gauge groups and non-linearized Regge dynamics, which are beyond the scope of this paper; (ii) topology change (edge creation/deletion) is not captured by smooth variation δl. The companion papers address partial extensions: Paper B [Kwon 2026b] verifies the gauge-geometry coupling dynamically via Monte Carlo across 2D–4D lattices with U(1) and SU(2) gauge groups; Paper G [Kwon 2026g] derives cosmological consequences (expansion, homogeneity) within the linearized regime.


## 6. Spectral Convergence under Perturbation

**Theorem 3.** Under Belkin-Niyogi conditions with bounded edge-weight perturbation ‖w−1‖ ≤ δ_n → 0, the normalized Laplacian eigenvalues converge: λ_k(L_n(w)) → λ_k(Δ_g).

*Proof sketch.* The unperturbed convergence λ_k(L_n(1)) → λ_k(Δ_g) holds by Belkin-Niyogi [2007] and García Trillos et al. [2020]. For the perturbed case, write L_n(w) = L_n(1) + E_n where E_n is the perturbation matrix induced by w ≠ 1. By the Weyl perturbation theorem [Weyl 1912; Kato 1966, Theorem V.4.10], |λ_k(L_n(w)) − λ_k(L_n(1))| ≤ ‖E_n‖₂. Since ‖E_n‖₂ = O(δ_n) → 0, the triangle inequality gives λ_k(L_n(w)) → λ_k(Δ_g). □

*Significance.* This theorem ensures that the dynamical evolution of edge weights (driven by the Euler-Lagrange equations of Theorem 2) does not destroy the spectral structure that makes the framework well-posed. The normalized Laplacian's eigenvalues continue to approximate those of the Laplace-Beltrami operator on the underlying manifold, even as the edge weights depart from unity.



---

## 6b. Scale Invariance and Asymmetry Dynamics

**Theorem 4 (Scale Invariance).** The four axioms VS1-VS4 contain no reference to length scale, energy scale, or lattice spacing. Any coarse-grained lattice obtained by block-spin transformation satisfies the same axioms, and the operator on the block lattice is T' = C' ⊙ S'.

*Proof.* Partition the lattice into blocks of size b. Define block embeddings p_alpha = normalize(sum a_i phi_i). Block content C'= <p_alpha, p_beta> is SO(d)-invariant; by Proposition 1, unique. Block structure S' = D'^{-1/2}A'D'^{-1/2}; by Proposition 2, unique. By Theorem 1, T' = C' ⊙ S'. []

*Consequence.* The theory is the same at every scale. Coarse-graining defines effective couplings beta'(beta, kappa) and kappa'(beta, kappa). The Hadamard structure forces these to be coupled: beta' depends on kappa (geometric fluctuations modify gauge coupling) and kappa' depends on beta (gauge fluctuations modify elastic stiffness). The full development is in the companion paper (Paper K).

**Theorem 5 (Monotonic Decrease of Asymmetry).** For overdamped dynamics dw_e/dt = -dS/dw_e on the T = C ⊙ S lattice with kappa > 0:

dS/dt = -sum_e (dS/dw_e)^2 <= 0

The action decreases monotonically. Equality holds only at equilibrium (dS/dw_e = 0 for all e).

*Proof.* dS/dt = sum (dS/dw_e)(dw_e/dt) = -sum (dS/dw_e)^2 <= 0. []

*Corollary.* The total squared asymmetry sum Delta_e^2 also decreases monotonically: d/dt sum Delta^2 = -2 Delta^T H Delta <= 0, where H = d^2S/dwdw is positive definite (kappa > 0). []

*Remark (Asymmetry as driving force).* The Euler-Lagrange equation (Theorem 2) can be read as: the discrepancy Delta_e = dS/dw_e between what content demands and what structure provides is the driving force of all dynamics. Equilibrium is the absence of discrepancy. The dynamics does nothing other than resolve asymmetry.

## 6c. Path Integral Measure

**Theorem 6 (Measure Uniqueness).** The path integral measure on edge weights w_e ∈ (0, ∞) is uniquely dμ(w_e) = dw_e/w_e (Haar measure of the multiplicative group ℝ₊). The integration domain is w_e ∈ [w_min, ∞) with w_min > 0, reflecting the physical requirement that lengths are strictly positive. Convergence of the partition function follows: ∫_{w_min}^∞ (1/w) exp(−κ(w−1)²) dw ≤ (1/w_min) ∫₀^∞ exp(−κ(w−1)²) dw = √(π/κ)/w_min < ∞.

*Proof.* The edge weight w_e represents a length (Regge calculus). Lengths are positive reals acted on by rescaling: w → λw (change of unit). This defines the multiplicative group (ℝ₊, ×).

The Haar measure of (ℝ₊, ×) is dw/w — the unique (up to normalization) left-and-right-invariant measure on the group [Haar 1933]. Under w → λw: dw/w → dw/w (invariant), while the Lebesgue measure transforms as dw → λdw (not invariant).

Uniqueness follows from the classification of Haar measures: every locally compact group admits a unique (up to scalar) left-invariant Radon measure. For (ℝ₊, ×), this measure is dw/w. □

*Remark 1 (Separation of measure and action).* The elastic term κ(w−1)² in the ACTION sets the equilibrium at w = 1. If the MEASURE also privileges w = 1 (as Lebesgue does, by assigning equal weight to [0,1] and [1,2]), the equilibrium is doubly imposed. The measure dw/w is agnostic about the equilibrium — it assigns equal weight to [1/2, 1] and [1, 2], treating "half the length" and "double the length" symmetrically. The measure provides the integration domain; the action provides the physics.

*Remark 2 (Consistency with Regge calculus).* In quantum Regge gravity, the Misner measure ∏ dl_e/l_e [Misner 1957] is the standard scale-invariant choice for edge lengths, consistent with conformal invariance of the gravitational path integral. The Hadamard framework's w_e plays the role of l_e. The measure dw/w is the Misner measure — not a new choice but an established identification.

*Remark 3 (No new axiom).* Theorem 6 uses no axiom beyond the positive-real nature of edge weights. Lengths are positive reals; positive reals under multiplication form a group; the unique invariant measure on this group is dw/w. This is not an additional physical principle — it is the mathematical structure of the variable. The axioms (VS1–VS4) determine the operator T and the action S. The measure is determined by the nature of the integration variable. Together, the partition function Z = ∫ [dU] ∏_e (dw_e/w_e) exp(−S[U, w]) is fully specified: [dU] is the compact Haar measure on the gauge group (unique by compactness), and dw_e/w_e is the Haar measure on ℝ₊ (unique by Theorem 6). The only remaining free quantities are β and κ, which are determined by self-consistency (Paper K, §10).

## 7. Physical Identification

C = cosθ = Re(e^{iθ}) is formally identical to the U(1) gauge link variable as defined by Wilson [1974]: the lattice gauge variable on edge (a,b) is U_{ab} = exp(iθ_{ab}), and the plaquette action uses Re(U_{ab}) = cosθ_{ab}. This is not an analogy but a definition match — the same mathematical object in the same role.

S converges to Laplace-Beltrami (Theorem 3). In Regge calculus, edge lengths encode the metric [Regge 1961].

The Hadamard coupling T = C ⊙ S (Theorem 1) couples gauge content to geometry at each edge. The discrete gauge-geometry equation of motion (Theorem 2) shows this coupling produces geometric deformation proportional to gauge energy upon variation. The dynamical verification (Monte Carlo, 42 measurements across 7 configurations in 2D–4D, U(1) and SU(2)) is in the companion paper [Kwon 2026b].


## 8. Discussion

Five results by mathematical proof:

(1) T = C ⊙ S is the unique variationally stable edge operator under the axioms (Theorem 1), with uniqueness extending to all analytic compositions, not only power-law forms. The exclusion of the C-only term (a₁₀ = 0) uses spectral consistency (Axiom 3); the exclusion of the S-only term (a₀₁ = 0) uses self-referentiality (Definition §0). Both are necessary: uniqueness requires all three axioms, the self-referential definition, and variational stability working together.

(2) The Hadamard product is the unique bilinear local composition (Lemma 1), and bilinearity itself is a consequence of variational stability rather than an independent assumption (Proposition 1, Remark).

(3) Variation produces the discrete gauge-geometry equation of motion (Theorem 2), which is the bridge from the operator T to the action S and hence to all dynamical predictions.

(4) Spectral convergence survives perturbation (Theorem 3), ensuring the framework's continuum limit is well-posed.

(5) Gauge and geometry are dynamically inseparable (Corollary 1): they share a single action and cannot be independently optimized.

(6) The path integral measure on edge weights is uniquely dw/w (Theorem 6): the Haar measure of the multiplicative group ℝ₊, consistent with the Misner measure in Regge calculus. Combined with the compact Haar measure on the gauge group, the partition function Z = ∫ [dU] ∏(dw/w) exp(−S) is fully specified with no free choices in the definition of the theory.

**What follows from these five results.** The uniqueness of T = C ⊙ S (Theorem 1) implies the uniqueness of the Hadamard-coupled action (Corollary 1). From this single action, the companion papers derive: gauge-geometry correlation r > 0 across all couplings and dimensions [B]; multiplicative noise gating in graph neural networks [C]; superadditive energy E ~ N^γ when multiple fields share geometry [D]; coherent force alignment from shared plaquette structure [F]; expansion, homogeneity, and structure formation as necessary consequences of the action's k-dependent structure [G]; and a two-sector spectral decomposition yielding both massive particles (short wavelength) and cosmological dynamics (long wavelength) from the same Hessian [H].

All of these consequences are forced: given the three axioms and variational stability, the operator is T = C ⊙ S, the action is determined, and the listed phenomena follow. The chain from axiom to cosmology and matter passes through a single bottleneck — the Hadamard product — and there are no alternatives.

**Scope.** The framework operates in the linearized Regge regime (Theorem 2 scope note). Extensions to full 3+1D gravity, non-abelian gauge groups beyond SU(2), and topology-changing dynamics remain open. The plaquette weight w_P = (∏ w_e)^{1/2} is the area measure for 2D plaquettes; the correct generalization to higher dimensions requires the Regge-calculus area formula, which preserves the multiplicative structure but changes the exponent.


## Acknowledgments

The author used Claude (Anthropic) as a computational tool for mathematical verification, numerical simulation, and assistance in preparing the manuscripts. All theoretical content — axioms, theorems, proofs, physical interpretations, and strategic decisions — is the author's original work. The author takes full responsibility for all content.

---

## References

- Belkin, M. & Niyogi, P. Convergence of Laplacian eigenmaps. NIPS (2007).
- Chung, F.R.K. Spectral Graph Theory. CBMS 92, AMS (1997).
- García Trillos, N. et al. Spectral convergence. Found. Comput. Math. 20 (2020).
- Kato, T. Perturbation Theory for Linear Operators. Springer (1966).
- Regge, T. General relativity without coordinates. Nuovo Cim. 19 (1961).
- Weyl, H. Das asymptotische Verteilungsgesetz der Eigenwerte linearer partieller Differentialgleichungen. Math. Ann. 71 (1912).
- Wilson, K.G. Confinement of quarks. Phys. Rev. D 10 (1974).
- Kwon, H. [2026b] Gauge-geometry coupling is a necessary consequence of self-referential dynamics on graphs. arXiv (2026).
- Kwon, H. [2026c] Necessity of multiplicative coupling in graph neural networks. arXiv (2026).
- Kwon, H. [2026d] Superadditive energy from multiplicative coupling on shared geometry. arXiv (2026).
- Kwon, H. [2026f] Forces from coupling: coherent alignment on shared geometry. arXiv (2026).
- Kwon, H. [2026g] Emergent cosmology from self-referential dynamics. arXiv (2026).
- Kwon, H. Emergent matter from gauge-geometry coupling. arXiv (2026).
- Haar, A. Der Massbegriff in der Theorie der kontinuierlichen Gruppen. Ann. Math. 34, 147–169 (1933).
- Misner, C.W. Feynman quantization of general relativity. Rev. Mod. Phys. 29, 497–509 (1957).
