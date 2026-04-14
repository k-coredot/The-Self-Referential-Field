# The Three Depths:
# Gauge Symmetries, Generations, Coupling Hierarchy,
# and Spacetime Dimension from Self-Referential Depth

Hyeokjun Kwon — April 2026

---

**Abstract.** Self-reference has depth. A field reads itself (depth 1). The reading is read (depth 2). The reading of the reading is read (depth 3). Each depth requires a state space to encode the reading: ℂ¹, ℂ², ℂ³. The norm-preserving symmetries of these spaces are U(1), SU(2), SU(3), with 1, 3, 8 generators respectively. Depth 4 would read a 3-component result with 4 components — the reading exceeds the read, producing redundancy incompatible with self-reference. Depth stops at 3. The total degrees of freedom per node are 1 + 3 + 8 = 12. Requiring these to distribute integrally over plaquette orientations in d dimensions gives 12/[d(d−1)/2] ∈ ℤ, selecting d = 4 as the unique dimension above 3. Each depth sustains a self-referential cycle with its own fixed point, producing three stable excitations of different mass — three generations. The number of generators determines the number of feedback channels, hence the coupling strength: 8 > 3 > 1. This paper derives the gauge group content, the spacetime dimension, the generation count, and the coupling hierarchy from the depth structure of self-reference.

---

## 1. Self-Referential Depth

The operator T = C ⊙ S is self-referential: T depends on the field Φ through C = ⟨φ_a, φ_b⟩, and Φ evolves through T. This is depth 1: the field reads itself.

But the result of the reading — the propagated field Φ' = TΦ — is itself a field. It can be read. The operator at the next step, T' = T[Φ'], reads the result of the first reading. This is depth 2.

The result of reading the result, Φ'' = T'Φ', can itself be read. This is depth 3.

Each depth is a self-referential cycle: Φ^{(n)} → T^{(n)} → Φ^{(n+1)}. Each cycle acts on a state space. The question is: what state space does each depth require?

## 2. State Spaces

**Depth 1.** The simplest self-referential reading. The field reads its own phase — one complex number suffices. State space: ℂ¹. A single complex component.

**Depth 2.** The reading distinguishes the reader from the read. Two roles, two components. State space: ℂ². This is the minimum space in which "the one who reads" and "what is read" can coexist as distinct entities.

**Depth 3.** The reading of the reading introduces a third entity: the relation between reader and read. Three roles, three components. State space: ℂ³.

**Depth 4?** Four components would be needed to read the three-component result of depth 3. But reading is not creation — it does not add information. A reading that requires more components than the object being read introduces redundancy: the excess components encode nothing new. Self-reference reads what is there, not what is not.

Therefore depth stops at 3.

**Theorem 1 (Depth Termination).** The independent degrees of freedom in the self-referential operator T = C ⊙ S are exhausted at depth 3. No depth ≥ 4 contributes new gauge-invariant information.

*Proof.* The self-referential dynamics on a lattice defines three levels of gauge-invariant data:

*Level 1 (nodes, 0-cells).* The field state φ_a at each node — one complex degree of freedom per gauge factor. State space: ℂ¹. These are the *objects* of the categorical structure.

*Level 2 (edges, 1-cells).* The coupling T_{ab} = C_{ab} · S_{ab} along each edge — encoding the relation between two node states. The spinor selection theorem (Paper H, Theorem 7) forces the fundamental representation: ℂ² for SU(2). These are the *morphisms*.

*Level 3 (plaquettes, 2-cells).* The plaquette action w_P cos Θ_P, where Θ_P = Σ_{e ∈ ∂P} ±θ_e is the oriented composition of edge phases around a minimal closed path. This encodes the curvature — the irreducible relation among three or more edges meeting at a face. The fundamental representation gives ℂ³ for SU(3). These are the *compositions*.

*Level ≥ 4 (cubes, hypercubes, n-cells for n ≥ 3).* Any n-cell with n ≥ 3 decomposes into plaquettes: the action on a cube is the product of its face plaquette actions. This decomposition is unique because:

(i) The Hadamard product ⊙ is associative: (a ⊙ b) ⊙ c = a ⊙ (b ⊙ c).

(ii) Gauge group composition is associative: U_{ac} = U_{ab} · U_{bc}.

(iii) On a CW complex, any closed n-surface (n ≥ 3) is the boundary of an (n+1)-chain and decomposes into 2-cells (Stokes' theorem on CW complexes).

Therefore, the gauge-invariant content of any n-cell (n ≥ 3) is a function of its constituent plaquettes. No independent degree of freedom exists beyond the plaquette level.

In categorical language: the self-referential structure defines a category (objects = node states, morphisms = edge couplings, composition = plaquette action). The nerve of any category is 2-coskeletal — all simplices of dimension ≥ 3 are uniquely determined by those of dimension ≤ 2. Depth 4 would correspond to a 3-simplex, which is determined by its 2-faces (plaquettes) via associativity. □

**Corollary 1.** The total state space is ℂ¹ ⊕ ℂ² ⊕ ℂ³, the symmetry group is U(1) × SU(2) × SU(3), and the total number of generators is 1 + 3 + 8 = 12.

*Remark (Relation to established results).* The depth termination has three independent mathematical roots: (i) in lattice gauge theory, every Wilson loop decomposes into plaquettes — the plaquette is the irreducible gauge-invariant building block (Wilson 1974); (ii) in category theory, the nerve of a category is 2-coskeletal (a standard result); (iii) in Peirce's semiotics, the categories (Firstness, Secondness, Thirdness) are complete — Fourthness reduces to compositions of Thirdness. The convergence of these three independent traditions on the same conclusion — independent structure terminates at the third level — constitutes strong evidence for the depth-3 limit. The predictions it generates — three gauge groups, d = 4, three generations — are independently testable.

## 3. Symmetries

Each state space has a natural symmetry: the group of transformations that preserve the norm (probability) and the determinant (volume) of the state.

    ℂ¹:  ψ → e^{iα}ψ.               U(1).    1 continuous parameter.
    ℂ²:  ψ → Uψ, U ∈ SU(2).         SU(2).   3 continuous parameters.
    ℂ³:  ψ → Uψ, U ∈ SU(3).         SU(3).   8 continuous parameters.

The number of generators (continuous parameters) of SU(n) is n² − 1:

    n = 1:  1² − 1 = 0, but U(1) has 1 generator (phase).
    n = 2:  2² − 1 = 3 generators.
    n = 3:  3² − 1 = 8 generators.

Total: 1 + 3 + 8 = 12 generators.

Each generator corresponds to a mediating field — a connection between nodes that carries the corresponding charge. Twelve generators, twelve mediating fields.

## 4. Spacetime Dimension

The total state at each node has 6 complex = 12 real degrees of freedom (from ℂ¹ ⊕ ℂ² ⊕ ℂ³). On a d-dimensional lattice, each node participates in d(d−1)/2 independent plaquette orientations. For the 12 degrees of freedom to distribute integrally among the plaquettes:

    12 / [d(d−1)/2] ∈ ℤ

Evaluation:

    d = 2:   12/1 = 12.    ✓  (but d = 2 has no propagating degrees of freedom)
    d = 3:   12/3 = 4.     ✓  (but see below)
    d = 4:   12/6 = 2.     ✓
    d = 5:   12/10 = 1.2.  ✗
    d = 6:   12/15 = 0.8.  ✗
    d ≥ 5:   all fail.

For d ≥ 5, no integral distribution exists. d = 4 is the unique dimension above 3 satisfying the condition.

The value 2 at d = 4 has geometric meaning: in four dimensions, the 6 plaquette orientations decompose into 3 self-dual and 3 anti-self-dual components. Each set carries 2 × 3 = 6 real degrees of freedom. The 12 internal degrees of freedom split evenly: 6 self-dual, 6 anti-self-dual. This decomposition is unique to d = 4.

**Why not d = 3?** In d = 3, the integrality condition gives 12/3 = 4 per plaquette. While this is integral, three-dimensional lattice gauge theory has no propagating gauge degrees of freedom — the plaquette variables are fully constrained by the link variables. The physical gauge field has d − 2 = 1 polarization in d = 3 (versus d − 2 = 2 in d = 4). The 12 degrees of freedom require 2 polarizations per plaquette orientation to form proper propagating fields, selecting d = 4.

## 5. Three Generations

Each depth sustains an independent self-referential cycle:

    Depth 1:  Φ₁ → T₁[Φ₁] → Φ₁'     (1 component, U(1) symmetry)
    Depth 2:  Φ₂ → T₂[Φ₂] → Φ₂'     (2 components, SU(2) symmetry)
    Depth 3:  Φ₃ → T₃[Φ₃] → Φ₃'     (3 components, SU(3) symmetry)

Each cycle has a fixed point: a field configuration that reproduces itself under the self-referential dynamics. Each fixed point is a stable excitation — a particle.

The three cycles are not independent: depth 2 reads the result of depth 1, and depth 3 reads the result of depth 2. The deeper the reading, the more complex the cycle, the higher the energy of the fixed point.

Three fixed points. Three energies. Three masses. Same gauge quantum numbers (each participates in all three symmetries through the product structure of the total state space). Different mass scales.

## 6. Coupling Hierarchy

The strength of the coupling at each depth is determined by the number of generators — the number of independent channels through which the positive feedback of Paper D operates.

**Depth 3 (8 generators):** Eight feedback channels. The most channels means the strongest coupling. At strong coupling, the mediating fields self-interact (non-abelian). Self-interaction produces confinement: excitations are permanently bound (see Complete Tree, §18).

**Depth 2 (3 generators):** Three feedback channels. Intermediate coupling. Non-abelian, but weaker than depth 3. The expansion of geometry (Paper G) breaks the vacuum symmetry at depth 2. The product T = C ⊙ S couples geometry and content: when geometric symmetry breaks, content symmetry inherits the breaking. Three mediators acquire mass.

**Depth 1 (1 generator):** One feedback channel. Weakest gauge coupling. Abelian — the mediator carries no charge, does not self-interact. No mechanism for mass acquisition. The mediator is massless.

**Geometry:** The geometric excitations (Paper H, mass gap 2κ) have their mass set by the elastic stiffness κ, which appears in a different term of the action than the gauge coupling β. The two scales are structurally independent — their ratio is not tuned but is a consequence of the action's multiplicative structure.

The hierarchy: depth 3 > depth 2 > depth 1 > geometry.


### 6.2 Hierarchy from AM-GM and Casimir (Paper K)

The qualitative hierarchy (depth 3 > depth 2 > depth 1 > geometry) is made quantitative by the coupled RG flow (Paper K). Two independently established effects compete:

**Universal geometric suppression (AM-GM).** The plaquette weight w_P = (prod w_e)^{1/2} satisfies <w_P> <= 1 by the AM-GM inequality. This suppresses the effective gauge coupling: delta_beta_geom < 0. The suppression is the same for all gauge groups — w_P is a geometric quantity, independent of the gauge structure.

**Group-dependent gauge self-coupling.** The non-abelian gauge self-interaction A wedge A produces a positive contribution delta_beta_gauge > 0, proportional to the quadratic Casimir C_2(adj): b_0 = 11 C_2(adj)/3. For SU(3): C_2 = 3, b_0 = 11. For SU(2): C_2 = 2, b_0 = 22/3. For U(1): C_2 = 0, b_0 = 0.

**The hierarchy is the competition:** SU(3) has the largest gauge compensation, overcoming the universal suppression most effectively. SU(2) compensates partially. U(1) has no compensation at all.

Result: g_3 > g_2 > g_1. The ordering is a structural consequence of two mathematical facts — AM-GM and Lie algebra — combined through the Hadamard coupling.

### 6.3 Weakness of Gravity from Gauge Multiplicity

Gauge fluctuations universally stiffen geometry: delta_kappa proportional to N_total x beta^2. The gravitational coupling G ~ 1/kappa is therefore suppressed by the total number of gauge generators:

G_eff ~ 1/(kappa_0 + N_total x delta_kappa)

In the Standard Model, N_total = 1 + 3 + 8 = 12. The gauge-gravity hierarchy is a structural consequence of 12 gauge degrees of freedom sharing a single geometry.

## 7. Predictions

The three-depth structure makes specific structural predictions:

(i) **Three and only three gauge symmetries.** Depth stops at 3. No fourth force exists (other than gravity, which is the geometry itself).

(ii) **Generator counts: 1, 3, 8.** Fixed by the dimensions of U(1), SU(2), SU(3). Total: 12 mediating fields.

(iii) **d = 4.** The unique dimension above 3 compatible with 12 degrees of freedom.

(iv) **Three generations.** Three depths, three fixed points. No fourth generation (depth stops at 3).

(v) **Mass ordering.** Generation 3 > generation 2 > generation 1. Deeper reading is heavier.

(vi) **Coupling ordering.** Strong (8) > electromagnetic (1) > weak (3, after symmetry breaking). Gravity weakest (geometric, κ-scale).

(vii) **Confinement at depth 3 only.** 8 generators with self-interaction produce flux tubes. Depths 1 and 2 do not confine.

(viii) **One massless mediator.** The depth-1 mediator (abelian, no self-interaction, no symmetry breaking).

(ix) **Three massive mediators.** Depth-2 symmetry breaking by geometric expansion.

(x) **CP violation.** Three generations produce one irreducible complex phase in the 3×3 mixing matrix. Two generations would not.

## 8. What This Does Not Determine

The depth structure determines the FORM of the gauge groups, the NUMBER of generations, and the ORDERING of couplings. It does not determine:

- The absolute values of coupling constants (these depend on β/κ).
- The absolute values of particle masses (these depend on the fixed-point energies).
- The mixing angles between generations (these depend on the overlap between cycles at different depths).

These quantities require solving the self-referential fixed-point equation at each depth — a computation that is well-defined but not yet performed.

## 9. Discussion

The three depths are not an input. They are a consequence of the structure of self-reference: reading, reading the reading, reading the reading of the reading. The fourth level fails because it reads more than what is there.

The coincidence between the depth structure (1, 2, 3 → 1, 3, 8 generators → 12 d.o.f. → d = 4) and the observed universe (U(1) × SU(2) × SU(3), 12 gauge bosons, 4 spacetime dimensions, 3 generations) is either:

(a) An accident — the depth structure happens to match reality by chance, or
(b) A derivation — the observed structure IS the depth structure, because the universe IS self-referential.

General relativity states that matter determines geometry and geometry determines matter. This is self-reference. If self-reference has the depth structure described here, then (b) follows.

---

## Acknowledgments

The author used Claude (Anthropic) as a computational tool for mathematical verification, numerical simulation, and assistance in preparing the manuscripts. All theoretical content — axioms, theorems, proofs, physical interpretations, and strategic decisions — is the author's original work. The author takes full responsibility for all content.

---

## References

- Kwon, H. The Hadamard structure of self-referential graphs. arXiv (2026a).
- Kwon, H. Gauge-geometry coupling from self-referential dynamics. arXiv (2026b).
- Kwon, H. The excitation spectrum of self-referential fields. arXiv (2026h).
- Kwon, H. Quantum interference from self-referential spinor structure. arXiv (2026i).
- Georgi, H. & Glashow, S.L. Unity of all elementary-particle forces. Phys. Rev. Lett. 32, 438 (1974).
- Weinberg, S. A model of leptons. Phys. Rev. Lett. 19, 1264 (1967).
- Fritzsch, H., Gell-Mann, M. & Leutwyler, H. Advantages of the color octet gluon picture. Phys. Lett. B 47, 365 (1973).
- Pati, J.C. & Salam, A. Lepton number as the fourth "color". Phys. Rev. D 10, 275 (1974).
- Baez, J. & Huerta, J. The algebra of grand unified theories. Bull. Amer. Math. Soc. 47, 483 (2010).
- Witten, E. Search for a realistic Kaluza-Klein theory. Nuclear Phys. B 186, 412 (1981).
- Wilson, K.G. Confinement of quarks. Phys. Rev. D 10, 2445 (1974).
