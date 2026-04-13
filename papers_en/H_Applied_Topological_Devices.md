# Topological Protection, Programmable Band Gaps, and Energy Confinement:
# Applications of the Hadamard Excitation Spectrum

Hyeokjun Kwon — April 2026

---

**Abstract.** The Hadamard gauge-geometry framework produces three properties of matter from a single Hessian h(k): a mass gap (h(π) > 0, Theorem 2), topological conservation (Σ W_P = 0, Theorem 3), and exponential localization (Corollary 1). These three mathematical results map directly to three classes of engineered devices: (1) topologically protected information carriers immune to local perturbation, based on conserved winding numbers; (2) materials with mechanically programmable band gaps, based on the κ-dependence of h(π) = 2κ; and (3) sub-wavelength energy concentrators, based on exponential localization with tunable decay length ξ = 1/√h. Material candidates, design principles, and experimental protocols are presented. The key advantage over existing approaches: the Hadamard structure provides these three properties simultaneously from one mechanism, whereas current technologies treat them as independent engineering goals.

---

## 1. The Three Properties

Paper H of this series proves that the action S = −Nβ Σ w_P cos Θ_P + κ Σ(w−1)² necessarily produces:

**(i) Mass gap.** h(π) = K_el(π) > 0 because |Γ(π)|² = 0. The shortest-wavelength excitations are always gapped. The gap magnitude is set by the elastic stiffness: m = √(2κ).

**(ii) Topological conservation.** On a closed surface, Σ W_P = 0 (Stokes). Winding numbers are conserved by local dynamics. Excitations carrying winding number are permanent — they cannot be annihilated by local perturbation.

**(iii) Exponential localization.** When h(k) > 0, correlations decay as exp(−r/ξ) with ξ = 1/√h. Excitations are confined to a region of size ξ.

Each property enables a class of devices.

---

## 2. Application Class 1: Topological Information Carriers

### 2.1 Principle

A winding number W is a topological invariant. It can be changed only by creating or annihilating a winding-antiwinding pair. Local perturbations — thermal noise, material defects, electromagnetic interference — cannot change W because they modify the field within a finite region while W is determined by the global circulation.

Information encoded in W is therefore immune to local noise. This is topological protection.

### 2.2 Material Realization

In multiferroic materials with multiple order parameters coupled through a shared crystal lattice (the physical realization of T = C ⊙ S), vortex configurations in the order parameter field carry winding number. Examples:

**Magnetic skyrmions** in chiral magnets (MnSi, FeGe, Cu₂OSeO₃). The skyrmion number N_sk = (1/4π) ∫ m · (∂_x m × ∂_y m) d²x is an integer topological invariant. Current skyrmion memories encode bits in the presence/absence of skyrmions. The Hadamard framework predicts enhanced stability when the magnetic order parameter is coupled to a secondary order parameter (e.g., ferroelectric polarization in multiferroic hosts) through shared lattice geometry — the mass gap increases with N (the number of coupled order parameters).

**Ferroelectric vortices** in PbTiO₃/SrTiO₃ superlattices. Polarization vortex arrays with topological winding. The Hadamard prediction: coupling to magnetic order (via multiferroic interface engineering) stabilizes the vortices beyond single-order-parameter limits.

### 2.3 Predicted Enhancement

The mass gap m = √(2κ) protects the topological excitation from thermal fluctuations. The activation energy for pair annihilation is E_a ∝ m × ξ, where ξ is the excitation size. With N coupled order parameters:

    E_a(N) ∝ N^{γ/2} × E_a(1)

For γ ≈ 1.8: E_a(3) ≈ 2.4 × E_a(1). Three coupled order parameters increase the topological protection by 2.4×. This translates to an operating temperature increase of the same factor.

### 2.4 Experimental Protocol

Fabricate a multiferroic heterostructure (e.g., CoFe₂O₄/BaTiO₃ nanocomposite) with controlled number of coupled order parameters (magnetic, ferroelectric, ferroelastic). Measure skyrmion or vortex stability (lifetime, nucleation barrier) as a function of the number of active order parameters. Compare with the prediction E_a(N) ~ N^{γ/2}.

---

## 3. Application Class 2: Programmable Band Gaps

### 3.1 Principle

The mass gap h(π) = 2κ is determined by the elastic stiffness κ. In a material where κ can be externally controlled, the band gap is programmable.

This is fundamentally different from existing tunable-bandgap approaches:

- **Semiconductor bandgap engineering** (e.g., AlGaAs composition): bandgap set at fabrication, not tunable in operation.
- **Photonic crystals with mechanical tuning**: bandgap shifts with lattice deformation, but the relationship is indirect and material-specific.
- **Hadamard bandgap**: m = √(2κ). Direct, exact, material-independent relationship between mechanical stiffness and spectral gap.

### 3.2 Material Realization

**Piezoelectric metamaterials.** A lattice of piezoelectric elements (PZT, PMN-PT) with electrically controllable stiffness. Applying voltage changes the effective elastic modulus C₁₁ of each element. In the Hadamard framework, this directly changes κ and hence the band gap.

    Δm/m = (1/2) Δκ/κ = (1/2) ΔC₁₁/C₁₁

For PMN-PT near the morphotropic phase boundary: ΔC₁₁/C₁₁ ≈ 50% under applied field. This gives Δm/m ≈ 25% — a 25% tunable band gap.

**Shape-memory alloy lattices.** NiTi lattices with temperature-dependent stiffness. Austenite-martensite transition changes the elastic modulus by a factor of 2–3. Band gap switches between two discrete values — a binary spectral switch.

**Hydrogel-embedded lattices.** Polymer lattices with humidity- or pH-dependent swelling. Swelling changes the effective spring constant of the lattice links. Continuously tunable κ via environmental stimuli.

### 3.3 Design Rule

The Hadamard framework provides a universal design rule:

    f_gap = (1/2π) √(2κ_eff / m_eff)

where κ_eff is the effective elastic stiffness per lattice link and m_eff is the effective mass per node. The gap frequency is independent of the lattice topology — it depends only on the local stiffness and mass. This simplifies design: choose the desired gap frequency, compute the required κ/m ratio, select materials accordingly.

---

## 4. Application Class 3: Sub-Wavelength Energy Concentration

### 4.1 Principle

Exponential localization means the excitation amplitude decays as exp(−r/ξ) with ξ = 1/√h(k). Inside a region of size ξ, the energy is concentrated. Outside, it is exponentially small.

By tuning h(k) — through κ (stiffness), β (coupling), or N (number of fields) — the localization length ξ is controllable.

Small ξ: energy concentrated in a small volume. High energy density. Useful for sensing, actuation, energy harvesting.

Large ξ: energy spread over a large volume. Low energy density. Useful for shielding, filtering, damping.

### 4.2 Material Realization

**Multiferroic resonators.** A multiferroic element embedded in a passive matrix. The multiferroic region has large β (strong gauge-geometry coupling). The surrounding matrix has large κ (strong elastic resistance). The excitation is localized within the multiferroic element with decay length ξ ≈ 1/√(2κ_matrix).

Multiple coupled order parameters within the multiferroic element increase the effective coupling, reducing ξ and concentrating more energy. The concentration factor scales as N^{γ/2}.

**Acoustic metamaterial concentrators.** A lattice of coupled resonators with tunable stiffness. Creating a localized "soft spot" (low κ region) surrounded by stiff regions concentrates acoustic energy at the soft spot. The Hadamard framework predicts the concentration ratio exactly: exp(2Δκ × d), where Δκ is the stiffness contrast and d is the distance from the soft spot.

### 4.3 Performance Metric

The figure of merit for energy concentration is the Q-factor × concentration ratio:

    FoM = (ξ_outer/ξ_inner) × (1/loss)

where ξ_outer is the localization length in the passive region and ξ_inner is the localization length in the active region. The Hadamard prediction:

    FoM(N) ∝ N^{γ/2} × √(κ_outer/κ_inner)

---

## 5. Unified Design Principle

The three application classes share a single design principle: **control κ and N.**

| Parameter | Topological protection | Band gap | Energy concentration |
|-----------|----------------------|----------|---------------------|
| Increase κ | Larger activation barrier | Wider gap | Tighter confinement |
| Increase N | Superadditive protection | N/A (gap is κ-only) | Superadditive concentration |
| Decrease κ locally | Create mobile excitations | Close gap locally | Create energy sink |

The Hadamard framework provides quantitative predictions for all three effects from a single formula:

    h(k) = 2κ − Nβ Φ(βa²) |Γ(k)|²

Protection, gap, and concentration are three readings of the same function.

---

## 6. Experimental Roadmap

| Phase | Target | Material | Measurement | Hadamard prediction |
|-------|--------|----------|-------------|-------------------|
| 1 | Topological stability vs N | CoFe₂O₄/BaTiO₃ composite | Skyrmion lifetime | E_a(N) ~ N^{0.9} |
| 2 | Tunable band gap | PMN-PT metamaterial lattice | Transmission spectrum vs voltage | Δf/f = ΔC₁₁/(2C₁₁) |
| 3 | Energy concentration | Multiferroic in passive matrix | Near-field energy mapping | Concentration ~ N^{0.9} |
| 4 | Integrated device | All three in one structure | Combined measurement | Three effects from one κ, N |

Phase 4 is the key differentiator: a single multiferroic metamaterial providing topological memory, tunable filtering, and energy harvesting simultaneously — three functions from one mechanism.

---

## Acknowledgments

The author used Claude (Anthropic) as a computational tool for mathematical verification, numerical simulation, and assistance in preparing the manuscripts. All theoretical content — axioms, theorems, proofs, physical interpretations, and strategic decisions — is the author's original work. The author takes full responsibility for all content.

---

## References

- Kwon, H. The excitation spectrum of self-referential fields. arXiv (2026h).
- Kwon, H. Superadditive energy from multi-gauge coupling. arXiv (2026d).
- Fert, A. et al. Magnetic skyrmions: advances in physics and potential applications. Nature Rev. Mater. 2, 17031 (2017).
- Yadav, A.K. et al. Observation of polar vortices in oxide superlattices. Nature 530, 198 (2016).
- Hasan, M.Z. & Kane, C.L. Topological insulators and superconductors. Rev. Mod. Phys. 82, 3045 (2010).
- Ozawa, T. et al. Topological photonics. Rev. Mod. Phys. 91, 015006 (2019).
- Sigalas, M.M. & Economou, E.N. Band structure of elastic waves in two-dimensional systems. Solid State Commun. 86, 141 (1993).
- Pendry, J.B. Negative refraction makes a perfect lens. Phys. Rev. Lett. 85, 3966 (2000).
- Ma, G. et al. Topological phases in acoustic and mechanical systems. Rev. Mod. Phys. 91, 015005 (2019).
