# Superadditive Energy Harvesting from Multiferroic Materials:
# Predictions from the Hadamard Gauge-Geometry Framework

Hyeokjun Kwon — April 2026

---

**Abstract.** The Hadamard gauge-geometry framework predicts that N order parameters sharing a crystal lattice produce geometric deformation energy scaling as E ~ N^γ (γ > 1) above a critical coupling — superadditivity. We map this prediction to multiferroic materials, where ferromagnetic, ferroelectric, ferroelastic, and orbital order parameters share a perovskite or composite lattice. The mapping yields five quantitative predictions testable with existing experimental techniques: (1) the coupling energy density in a 3-order-parameter multiferroic exceeds 3× the single-order value; (2) a critical magnetoelectric coupling coefficient α_ME^c ≈ 10–50 mV/cm·Oe separates competitive (subadditive) and cooperative (superadditive) regimes; (3) the superadditivity exponent γ is larger in thin films (d = 2) than in bulk (d = 3); (4) intentional lattice defects amplify superadditivity by ~9%; (5) force alignment between order parameters exceeds 99%, enabling directional energy extraction without rectification. We identify CoFe₂O₄/P(VDF-TrFE) nanocomposites as the most promising candidate (α_ME ≈ 100–400 mV/cm·Oe, well above the predicted threshold) and propose three experimental protocols for verification.

---

## 1. From Theory to Materials

### 1.1 The Theoretical Result

Paper D of this series established that when N gauge fields share a dynamical lattice geometry through the Hadamard-coupled action S = −Nβ Σ w_P cos Θ_P + κ Σ(w−1)², the geometric deformation energy scales superadditively:

E(N) / [N × E(1)] = R(N) > 1  for β > β_c

with R(N) ~ N^{γ−1}, γ = 1.8 ± 0.2 in 2D. This is a necessary consequence of the multiplicative coupling structure: deformation by one field increases the plaquette weight w_P, which strengthens the coupling for all fields (positive feedback through the shared geometric mean).

### 1.2 The Mapping

| Lattice model | Multiferroic material |
|---|---|
| Gauge field θ^{(i)} | Order parameter (magnetization M, polarization P, strain ε, orbital order) |
| Edge weight w_e | Local lattice parameter (bond length, unit cell dimension) |
| Plaquette weight w_P | Local cell volume (geometric mean of surrounding bond lengths) |
| cos Θ_P | Order parameter coherence (nearest-neighbor correlation) |
| β (coupling constant) | Magnetoelectric coupling α_ME, piezoelectric coefficient d₃₃, magnetostrictive coefficient λ |
| κ (elastic stiffness) | Bulk modulus C₁₁ |
| N (number of fields) | Number of distinct order parameters |

The mapping is structural: both systems have multiple fields coupled to a shared geometry through a multiplicative (Hadamard) term. The lattice model captures the essential physics — positive feedback through shared geometric degrees of freedom — while abstracting away material-specific details.

### 1.3 Why This Matters

Conventional energy harvesting exploits one physical effect at a time: piezoelectric (strain → voltage), pyroelectric (temperature → voltage), or magnetostrictive (field → strain). If N effects are combined, conventional design predicts additive scaling: total output ~ N × single output.

Superadditivity predicts N^γ scaling with γ ≈ 1.8. For N = 3 order parameters, this yields R(3) ≈ 1.9 — nearly twice the additive prediction. For N = 5, R(5) ≈ 4.5 — over four times additive. This is not a small correction; it is a qualitative change in the scaling law.

## 2. Five Predictions

### 2.1 Prediction 1: Superadditive Energy Density

A multiferroic material with N ≥ 3 order parameters, coupled above the critical threshold, will exhibit coupling energy density exceeding N times the single-order coupling energy.

Quantitative prediction from MC simulation (Table 1 of Paper D):

| N | R(N) | Amplification vs single-order |
|---|------|------|
| 2 | 1.1 | 2.2× |
| 3 | 1.5 | 4.5× |
| 5 | 3.1 | 15.6× |

These ratios are lattice-model values. The material-specific values will differ in magnitude but the superlinear scaling R(N) > 1 for N ≥ 3 is a structural prediction that depends only on the Hadamard coupling, not on specific parameter values.

### 2.2 Prediction 2: Critical Coupling Threshold

Below a critical coupling β_c, order parameters compete for lattice degrees of freedom (subadditive: R < 1). Above β_c, they cooperate through the shared lattice (superadditive: R > 1).

The critical coupling maps to a critical magnetoelectric coupling coefficient:

β_c = κ n_E / (N n_P c(β_c))

In material parameters: α_ME^c is determined by the balance between lattice stiffness (C₁₁) and order-parameter-lattice coupling strength. Estimated range:

- Single-crystal BiFeO₃ (α_ME ≈ 1–3 mV/cm·Oe): near or below β_c → marginal superadditivity
- CoFe₂O₄/PZT nanocomposite (α_ME ≈ 100–400 mV/cm·Oe): well above β_c → strong superadditivity
- CoFe₂O₄/P(VDF-TrFE) (α_ME ≈ 200–800 mV/cm·Oe): deep in superadditive regime

The transition from subadditive to superadditive is sharp (phase transition, Paper D §3.2) and should be observable by scanning α_ME through temperature variation, composition tuning, or epitaxial strain.

### 2.3 Prediction 3: Thin Film Enhancement

The superadditivity exponent γ depends on dimension:

| Dimension | γ |
|---|---|
| 2D (thin film) | 1.8 ± 0.2 |
| 3D (bulk) | 1.4 ± 0.2 |

Thin films (thickness < correlation length ξ, typically < 500 nm) should exhibit stronger superadditivity than bulk samples of the same material. This is because reduced dimensionality increases geometric frustration — fewer lattice directions available for deformation relief.

Testable by comparing coupling energy in the same composition at varying thickness: 1 μm (3D-like), 500 nm, 200 nm, 50 nm.

### 2.4 Prediction 4: Defect Amplification

Intentional lattice defects (point defects, dislocations) increase geometric frustration and amplify superadditivity. MC simulation predicts R(5) increases from 3.10 to 3.37 (~9%) with moderate defect density.

Testable by Ar⁺ ion irradiation of epitaxial thin films at controlled dose (10¹² – 10¹⁴ cm⁻²) and measuring coupling energy vs dose.

### 2.5 Prediction 5: Force Alignment

Paper F established that forces from N independent fields on shared geometry align to >99% (cos θ ≥ 0.964 for N ≥ 2). In a multiferroic, this predicts:

- The lattice strain produced by magnetic, electric, and elastic order parameters is nearly unidirectional
- Energy extraction does not require rectification (the output is DC-like)
- Force direction is temporally stable (consecutive-measurement cosine similarity 0.999)

This is testable by simultaneous measurement of magnetostriction direction and piezoelectric strain direction in a multiferroic under multi-stimulus excitation.

## 3. Candidate Materials

### 3.1 Primary Candidate: CoFe₂O₄/P(VDF-TrFE) Nanocomposite

| Property | Value |
|---|---|
| Order parameters | Ferromagnetic (CoFe₂O₄) + Ferroelectric (PVDF) + Ferroelastic (lattice) |
| N | 3 |
| α_ME | 200–800 mV/cm·Oe |
| β estimate | 2–5 (well above β_c ≈ 1.5) |
| C₁₁ estimate | 3–10 GPa (polymer matrix) |
| κ estimate | 0.5–2 (near optimal range κ ≈ 2–3) |
| Predicted R(3) | 1.5–2.0 |
| Film thickness | 100–500 nm achievable by spin coating |

Advantage: high α_ME, tunable stiffness (polymer fraction), easy thin film fabrication.

### 3.2 Secondary Candidate: BiFeO₃ Epitaxial Thin Film

| Property | Value |
|---|---|
| Order parameters | Ferromagnetic + Ferroelectric + Ferroelastic |
| N | 3 |
| α_ME | 1–3 mV/cm·Oe (bulk); up to 100 mV/cm·Oe in strained films |
| β estimate | 0.5–3 (near β_c, tunable by strain) |
| C₁₁ | ~200 GPa |
| Predicted behavior | Transition from sub- to superadditive observable by strain tuning |

Advantage: the critical transition β_c is accessible, enabling direct observation of the phase transition.

### 3.3 Tertiary Candidate: BaTiO₃/CoFe₂O₄ Laminate

4 order parameters (two ferroelectric, one ferromagnetic, one ferroelastic). Predicted R(4) ≈ 1.6× R(3). Testable by comparing 3-order and 4-order compositions on the same substrate.

## 4. Experimental Protocols

### 4.1 Protocol 1: Superadditivity Ratio Measurement

(a) Fabricate a series of thin films with N = 1, 2, 3, 4 order parameters on identical substrates.
(b) Apply identical thermal cycling (ΔT = 10 K across a ferroic transition) to each film.
(c) Measure lattice strain energy (by X-ray diffraction) or electrical output (from piezoelectric extraction layer).
(d) Compute R(N) = E(N) / [N × E(1)].
(e) If R(N) > 1 for N ≥ 3 and R(N) increases with N: superadditivity confirmed.

### 4.2 Protocol 2: Critical Coupling Transition

(a) Use BiFeO₃ thin film under variable epitaxial strain (achievable by different substrates: SrTiO₃, LaAlO₃, DyScO₃).
(b) Strain tunes α_ME, scanning β from below β_c to above.
(c) Measure coupling energy vs strain.
(d) If a sharp transition from R < 1 to R > 1 is observed: critical coupling confirmed.

### 4.3 Protocol 3: Force Alignment

(a) Apply simultaneous magnetic field (H) and electric field (E) to a multiferroic thin film.
(b) Measure magnetostriction direction and piezoelectric strain direction independently.
(c) Compute cos θ between the two strain directions.
(d) If cos θ > 0.95: force alignment confirmed.

## 5. Energy Harvesting Performance Estimate

For a CoFe₂O₄/P(VDF-TrFE) nanocomposite (N = 3, R ≈ 1.5):

- Single-order piezoelectric harvester (N = 1): ~0.5 μW/cm²
- Additive prediction (N = 3): ~1.5 μW/cm²
- Superadditive prediction (R = 1.5): ~2.25 μW/cm² (50% enhancement)
- With thin film enhancement (γ_2D > γ_3D): ~3 μW/cm²
- With defect amplification (+9%): ~3.3 μW/cm²

For N = 5 (if achievable): R ≈ 3, giving ~7.5 μW/cm² vs additive 2.5 μW/cm² (3× enhancement).

These estimates are order-of-magnitude. The structural prediction (superlinear scaling) is robust; the precise coefficients require experimental calibration.

## 6. Discussion

### 6.1 What Is New

Multiferroic energy harvesting has been studied extensively (Priya & Inman 2009, Nan et al. 2008). The new element is the prediction of **superadditive** scaling — not just combining multiple effects additively, but exploiting the nonlinear amplification that arises from shared geometry. This amplification is a necessary consequence of the Hadamard structure of the gauge-geometry coupling, not an empirical observation.

### 6.2 Limitations

The parameter mapping (β → α_ME, κ → C₁₁) is qualitative. Quantitative correspondence requires experimental calibration. The MC simulations are on idealized lattices; real materials have disorder, grain boundaries, and finite-temperature effects. The predicted γ values may differ quantitatively in real materials while preserving the qualitative superlinear scaling.

### 6.3 Symmetry Group Dependence of γ

Paper D (§6.3) shows that the superadditivity exponent γ depends on the symmetry of the order parameter. In lattice simulations, SU(2) fields (3 internal generators) show weaker superadditivity than U(1) fields (1 generator): at N = 3, the superadditivity ratio R is 1.16 for SU(2) versus 1.61 for U(1). The explanation: SU(2) fields have internal degrees of freedom that reduce the independent information each additional field contributes.

For material selection, this translates to a design rule: **maximize the number of independent order parameters, minimize their internal symmetry.** Concretely:

- U(1)-like order parameters (scalar polarization, uniaxial strain) contribute most to superadditivity — each one is maximally independent.
- SU(2)-like order parameters (3D magnetization vectors) contribute less per parameter — they have internal correlations.

A composite with 5 scalar order parameters (ferroelectric + pyroelectric + piezoelectric + photovoltaic + thermoelectric) will show stronger superadditivity than a composite with 5 vector order parameters. The optimal material has many weakly correlated scalar responses sharing one stiff lattice.

### 6.4 Relation to Existing Work

Conventional multiferroic energy harvesting (Ryu et al. 2015, Zhou et al. 2019) treats multi-order coupling as additive or at best weakly synergistic. The T = C⊙S framework provides a quantitative prediction for the coupling law (E ~ N^γ) and the existence of a critical threshold (β_c), neither of which appears in existing multiferroic theory.

## 7. Conclusion

The Hadamard gauge-geometry framework makes five testable predictions for multiferroic energy harvesting: superadditive energy density, critical coupling threshold, thin film enhancement, defect amplification, and force alignment. All five are necessary consequences of the multiplicative coupling structure T = C⊙S. CoFe₂O₄/P(VDF-TrFE) nanocomposites are identified as the primary candidate for experimental verification. The prediction is not "multiferroics might be useful for energy harvesting" — that is known. The prediction is "the energy scales as N^γ with γ > 1" — that is new, quantitative, and falsifiable.

## Acknowledgments

The author used Claude (Anthropic) as a computational tool for mathematical verification, numerical simulation, and assistance in preparing the manuscripts. All theoretical content — axioms, theorems, proofs, physical interpretations, and strategic decisions — is the author's original work. The author takes full responsibility for all content.

---

## References

- Kwon, H. Superadditive energy from multi-gauge coupling. arXiv (2026d).
- Kwon, H. Superadditive forces from multi-gauge coupling. arXiv (2026f).
- Eerenstein, W. et al. Multiferroic and magnetoelectric materials. Nature 442, 759 (2006).
- Spaldin, N.A. & Ramesh, R. Advances in magnetoelectric multiferroics. Nature Materials 18, 203 (2019).
- Nan, C.W. et al. Multiferroic magnetoelectric composites. J. Appl. Phys. 103, 031101 (2008).
- Priya, S. & Inman, D.J. Energy Harvesting Technologies. Springer (2009).
- Ryu, J. et al. Magnetoelectric composite energy harvesters. Adv. Funct. Mater. 25, 4631 (2015).
