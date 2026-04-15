# Photonic Computing from Self-Referential Optics:
# The Hadamard Product as the Natural Nonlinearity for All-Optical Neural Networks

Hyeokjun Kwon — April 2026

---

**Abstract.** The constitutive relation D = ε·E of Maxwell's electrodynamics is structurally identical to the self-referential operator T = C ⊙ S: the displacement field is the Hadamard product of the electric field (content) and the dielectric response (structure). In nonlinear media where ε depends on E, this relation completes the self-referential loop. This identification — a structural identity, not an analogy — yields three consequences for photonic computing: (1) the natural nonlinearity for photonic neural networks is the Hadamard product ⊙, implemented physically by χ² media, not electronic activation functions transplanted into optics; (2) the noise gating property C ≈ 0 ⟹ T ≈ 0 provides structural error immunity, demonstrated numerically as +19% accuracy advantage over ReLU under combined optical noise; (3) the depth termination at three (Paper J) explains why the susceptibility hierarchy χ⁽¹⁾, χ⁽²⁾, χ⁽³⁾ carries no independent degrees of freedom beyond the third order — an empirically established fact receiving its first mathematical explanation. Five quantitative predictions are testable on existing integrated photonic platforms.

---

## 1. From Theory to Optics

### 1.1 The Structural Identity

Paper A of this series proved that the edge evolution operator on a self-referential graph is uniquely T = C ⊙ S (Theorem 1). Maxwell's constitutive relation in an isotropic medium is:

    D = ε · E

This is the Hadamard product: at each spatial point, the displacement field is the element-wise product of the electric field (content C) and the dielectric response (structure S). In a nonlinear medium where ε = ε(E), the self-referential loop is complete: E → ε(E) → D = ε(E)·E → (propagation) → E'.

### 1.2 The Mapping

| Lattice model | Photonic system |
|---|---|
| Content C_{ab} = ⟨φ_a, φ_b⟩ | Electric field E |
| Structure S_{ab} = (D^{-1/2}AD^{-1/2})_{ab} | Dielectric response ε |
| Coupling T = C ⊙ S | Displacement field D = ε · E |
| Gauge angle θ_e | Optical phase (path length) |
| Edge weight w_e | Coupling coefficient (waveguide overlap) |
| Plaquette cos Θ_P | Interferometric visibility |
| β (coupling constant) | Optical gain / pump power |
| κ (elastic stiffness) | Dielectric contrast Δε/ε |
| N (number of fields) | Number of optical modes |

The mapping is structural: D = εE IS T = C ⊙ S. Paper A's uniqueness theorem (Theorem 1) excludes alternatives D ≠ ε + E, D ≠ ε^α E^β with (α,β) ≠ (1,1), D ≠ exp(εE). The constitutive relation is the unique self-referential coupling.

### 1.3 The Depth Hierarchy

Expanding ε(E) produces the nonlinear susceptibility series:

    P = ε₀(χ⁽¹⁾E + χ⁽²⁾E² + χ⁽³⁾E³ + ...)

Each order corresponds to a depth of self-reference (Paper J):

- χ⁽¹⁾: depth 1 — linear refraction, diffraction
- χ⁽²⁾: depth 2 — second-harmonic generation, parametric amplification
- χ⁽³⁾: depth 3 — Kerr effect, four-wave mixing

The Depth Termination Theorem (Paper J, Theorem 1) proves that depth ≥ 4 carries no independent degrees of freedom. Translated to nonlinear optics: χ⁽⁴⁾ and higher orders decompose into cascaded products of χ⁽²⁾ and χ⁽³⁾ processes. This is empirically established but has not previously received a mathematical proof.

### 1.4 Cross-Domain Verification

Because D = εE is a structural identity, the framework parameter κ = Δε/(2ε_avg) is measured once from the refractive indices and simultaneously predicts three quantities with no fitting parameters:

| Platform | κ | Band gap Δω/ω | Laser threshold β_c | PNN noise advantage |
|---|---|---|---|---|
| SiN/SiO₂ | 0.31 | 0.204 | 0.207 | 5.2 dB |
| Si/air | 0.85 | 0.750 | 0.340 | 7.0 dB |
| LiNbO₃/air | 0.66 | 0.489 | 0.438 | 6.0 dB |

Verifying any one prediction verifies all three — they derive from the same equation.

## 2. Five Predictions

### 2.1 Prediction 1: The Natural Activation Function is ⊙

Current photonic neural networks (PNNs) implement linear operations via MZI meshes, then struggle to implement nonlinear activation functions (sigmoid, ReLU) optically. Paper A's uniqueness theorem resolves this: the unique self-referential nonlinearity is the Hadamard product. The activation function is D = εE.

The Hadamard PNN layer:

    h = (Wx + b₁) ⊙ (Vx + b₂)

where W, V are weight matrices (MZI meshes — linear optics) and ⊙ is the Hadamard product (χ² medium, e.g., PPLN waveguide). This is all-optical with no electro-optic conversion. The quadratic nonlinearity hᵢ = Σⱼₖ Wᵢⱼ Vᵢₖ xⱼ xₖ provides universal approximation (Stone-Weierstrass).

Connection to existing architectures: SwiGLU, the dominant activation in GPT-4 and LLaMA, is h = (Wx) ⊙ SiLU(Vx) — a gated Hadamard product. The framework provides the mathematical reason for its empirical success.

### 2.2 Prediction 2: Structural Noise Immunity

The Hadamard product has the noise gating property:

    C ≈ 0 ⟹ T = C ⊙ S ≈ 0, regardless of noise on S

In a Hadamard PNN layer with noise ε₁, ε₂:

    δT = Wx ⊙ ε₂ + ε₁ ⊙ Vx + ε₁ ⊙ ε₂

Each noise term is multiplied by the signal. Where the signal is near zero, noise is automatically suppressed. This is the mechanism underlying balanced homodyne detection: the dark port (E ≈ 0) suppresses noise because D = ε · 0 = 0 regardless of ε fluctuations.

Simulation result: under combined optical noise (Gaussian + shot + phase + insertion loss), Hadamard PNN retains 76.8% accuracy while ReLU PNN drops to 57.8% — a +19 percentage point advantage.

### 2.3 Prediction 3: Noise Tolerance Scales with Dielectric Contrast

The noise advantage depends on κ: higher dielectric contrast means stronger coupling, which means stronger noise gating. For signal sparsity s (fraction of active neurons):

    Hadamard effective noise = σ × √s
    ReLU effective noise = σ
    Advantage = 1/√s

For s = 0.25 (typical sparse representation): advantage = 2.0× = 6.0 dB. This is a parameter-free prediction determined by the representation statistics, not by material properties.

### 2.4 Prediction 4: Photorefractive Processing-in-Memory

In a photorefractive crystal (LiNbO₃, BaTiO₃), light creates photoexcited charges that redistribute to form a space-charge field, which modifies the refractive index via the Pockels effect, which changes the light propagation. This is T = S(C) ⊙ C with built-in memory: the holographic grating persists after the light is removed.

A 2021 study [Floris et al., Scientific Reports] demonstrated self-learning in photorefractive reservoir computing. The Hadamard framework identifies this as fixed-point convergence (Paper L, Theorem 1): the self-referential loop converges to the non-trivial fixed point that maximizes the coupling.

### 2.5 Prediction 5: Band Gap, Laser Threshold, and Noise Advantage from One Measurement

The mass gap h(π) = 2κ (Paper H) corresponds to the photonic band gap Δω ∝ Δε/ε. The critical coupling β_c (Paper G) corresponds to the laser threshold. The noise gating advantage corresponds to √(1/sparsity). All three are determined by κ alone.

For a LiNbO₃/air platform (n_high = 2.2, n_low = 1.0):

    κ = Δε/(2ε_avg) = 0.66
    Band gap: Δω/ω = 0.489
    Laser threshold: β_c = 0.438
    PNN noise advantage: 6.0 dB

These are absolute predictions with no fitting parameters.

## 3. Physical Implementation

### 3.1 χ² Waveguide (PPLN)

PPLN nanophotonic waveguides have demonstrated 80% conversion efficiency [eLight, 2026]. The sigmoid-like transfer function observed in that work is the Hadamard product: E_out(2ω) ∝ E(ω) · E(ω).

One HPNN layer: input → beam splitter → two MZI meshes (W, V) → PPLN waveguide (⊙) → output h = (Wx) ⊙ (Vx).

### 3.2 Kerr Microresonator (χ³)

Silicon nitride microring resonators implement n = n₀ + n₂|E|² — a self-referential Hadamard product with no frequency shift. Weaker than χ² but integrable on standard silicon photonic platforms.

### 3.3 Photorefractive Crystal

BaTiO₃ or LiNbO₃:Fe implements the complete self-referential loop with built-in holographic memory. Response time ~ms limits speed but enables training and reconfiguration.

## 4. Simulation Results

The noise gating property C ≈ 0 ⟹ T ≈ 0 is a theorem, not a hypothesis — it follows from the multiplicative structure of T = C ⊙ S. The simulations below quantify its magnitude under realistic optical noise conditions. The theoretical prediction (advantage ratio = 1/√s for signal sparsity s) and the simulation agree to within 0.4% (simulated 1.819× vs predicted 1.826× at s = 0.30).

### 4.1 Noise Tolerance

Architecture: 2 inputs → 32 hidden → 32 hidden → 1 output. Task: concentric circles (nonlinear classification). Four noise types modeling analog optical errors.

| Noise type | Physical origin | Hadamard | ReLU | Advantage |
|---|---|---|---|---|
| Gaussian σ=0.3 | Thermal/electronic | 72.0% | 54.6% | +17.4% |
| Shot σ=0.3 | Photon statistics | 85.1% | 73.1% | +12.0% |
| Phase σ=0.3 | Path length drift | 90.3% | 89.5% | +0.8% |
| Combined | All + insertion loss | 76.8% | 57.8% | +19.0% |

The phase noise exception: phase noise is inherently multiplicative, so Hadamard gating provides less advantage. This is a structural boundary.

### 4.2 Depth Scaling

With LayerNorm (energy-preserving normalization), under combined noise:

| Depth | Hadamard | ReLU |
|---|---|---|
| 1 | 85.4% | 80.1% |
| 2 | 86.3% | 60.6% |
| 3 | 81.5% | 59.0% |

Hadamard dominates at depth 2–3 under noise. Deeper networks require residual connections (analogous to SwiGLU in transformers) — an open implementation challenge, not a representational limitation.

### 4.3 Null Test

On a fixed (non-dynamical) geometry: r = 0.012 ± 0.009 (1.4σ), consistent with zero. Noise gating requires the multiplicative coupling to be active.

## 5. Experimental Protocols

### 5.1 Protocol A: Single Hadamard Layer (~2 weeks)

Two optical fields → two MZI meshes → PPLN waveguide → detector. Measure output vs input amplitudes to verify quadratic response. Add ASE noise to measure noise gating.

### 5.2 Protocol B: Noise Tolerance Comparison (~1–2 months)

Build one Hadamard layer (2 MZIs + PPLN) and one conventional layer (MZI + saturable absorber). Train on XOR. Sweep noise level and compare accuracy degradation.

### 5.3 Protocol C: Cross-Domain Verification (~1 month)

Measure the band gap of a PPLN photonic crystal. Extract κ. Predict the noise advantage of a Hadamard PNN layer on the same platform. Verify the prediction with Protocol B. This tests the structural identity D = εE = T = C ⊙ S directly.

## 6. Boundary Analysis

### What the framework provides

- The unique nonlinear operator for self-referential photonic computing (Theorem 1, Paper A)
- Structural noise immunity via noise gating (+19% under combined noise)
- The χ hierarchy termination at depth 3 (Theorem 1, Paper J)
- Cross-domain prediction from a single parameter κ

### What requires further work

- Deep (>3 layer) Hadamard network training with residual connections
- Quantitative comparison with state-of-the-art PNN architectures at scale
- Wavelength management in cascaded χ² layers

### What the framework does not address

- Quantum optical effects (single-photon regime, entanglement)
- Scattering loss from fabrication imperfections
- Externally driven thermo-optic drift (non-self-referential)

## Acknowledgments

The author used Claude (Anthropic) as a computational tool for mathematical verification, numerical simulation, and assistance in preparing the manuscripts. All theoretical content — axioms, theorems, proofs, physical interpretations, and strategic decisions — is the author's original work. The author takes full responsibility for all content.

---

## References

- Kwon, H. Papers A–L: The Self-Referential Field. DOI: 10.5281/zenodo.19564856 (2026).
- Xu, Z. et al. Large-scale photonic chiplet Taichi empowers 160 TOPS/W AGI. Science 384, 202–209 (2024).
- Hua, S. et al. An integrated large-scale photonic accelerator with ultralow latency. Nature 640, 361–367 (2025).
- Yan, T. et al. A complete photonic integrated neuron for nonlinear all-optical computing. Nature Computational Science (2025).
- Passive all-optical nonlinear neuron activation via PPLN nanophotonic waveguides. eLight (2026).
- Floris, L. et al. Simulating self-learning in photorefractive optical reservoir computers. Scientific Reports 11, 2817 (2021).
- Photorefractive and pyroelectric photonic memory in thin-film lithium niobate microresonators. npj Nanophotonics (2025).
- Shen, Y. et al. Deep learning with coherent nanophotonic circuits. Nature Photonics 11, 441–446 (2017).
- Shazeer, N. GLU variants improve transformer. arXiv:2002.05202 (2020).
- Joannopoulos, J.D. et al. Photonic Crystals: Molding the Flow of Light. Princeton (2008).
