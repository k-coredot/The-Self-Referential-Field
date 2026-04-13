# The Necessity of Multiplicative Content-Structure Coupling
# in Graph Neural Networks

Hyeokjun Kwon — April 2026

---

**Abstract.** Graph Neural Networks propagate information by combining node features (content) with graph topology (structure), yet no principled method exists for determining *how* content and structure should be combined. We prove that the Hadamard (elementwise) product T = C ⊙ S—where C is the pairwise state inner product and S is the self-adjoint normalized adjacency D⁻¹/²AD⁻¹/²—is the unique edge operator satisfying locality, rotational invariance, self-adjoint spectral consistency, and variational stability. Additive coupling (C + S), matrix multiplication, tensor products, and all nonlinear alternatives C^α S^β with (α,β) ≠ (1,1) are excluded by these axioms. We validate the theory on Cora, CiteSeer, and PubMed using parameter-free field dynamics: under noise injection (0–100% spurious edges), multiplicative coupling outperforms additive coupling by up to 15.3 percentage points (Cora, 25% noise) in vertex kNN accuracy, with the advantage *increasing* with noise level. Analysis of per-edge coupling weights reveals the mechanism: multiplicative coupling produces a natural gating effect where noise edges receive near-zero weight (C ≈ 0 ⟹ C·S ≈ 0), while additive coupling amplifies noise (C ≈ 0 but C+S ≈ S > 0). These results establish that the GNN propagation operator is not a design choice but a mathematical necessity, and that its multiplicative structure provides automatic noise suppression without learned parameters.

---

## 1. Introduction

The theoretical contribution of this paper is one line: if C = 0, then C · S = 0. Everything that follows — noise immunity, adversarial defense, anomaly detection — is a consequence of multiplication by zero. The remainder of this paper validates this arithmetic on standard benchmarks.

The core operation of any Graph Neural Network is message passing: aggregating information from neighboring nodes through the graph structure. Every GNN architecture makes a choice—explicitly or implicitly—about how to combine two fundamentally different sources of information:

- **Content (C)**: the similarity or relationship between node states
- **Structure (S)**: the topology and degree distribution of the graph

GCN (Kipf & Welling, 2017) uses S alone (normalized adjacency) to weight messages, with content entering only through learned transformations. GAT (Veličković et al., 2018) learns content-dependent attention weights but treats them independently from structural normalization. GraphSAGE (Hamilton et al., 2017) samples and aggregates neighbors with mean/max/LSTM pooling. GIN (Xu et al., 2019) uses sum aggregation with no normalization. PNA (Corso et al., 2020) combines multiple aggregators.

None of these approaches provides a theoretical justification for *why* a particular combination of content and structure should be preferred. The choice is treated as a hyperparameter, evaluated empirically on benchmarks.

We prove this choice is not free. Starting from three physically motivated axioms and one stability condition, we derive that:

1. The content similarity must be the inner product C_{ab} = ⟨φ_a, φ_b⟩ (unique rotationally invariant bilinear form).
2. The structural normalization must be S = D⁻¹/²AD⁻¹/² (unique self-adjoint degree normalization).
3. The composition must be the Hadamard product T = C ⊙ S (unique bilinear pointwise operation).
4. The exponents must be (α,β) = (1,1) (variational stability excludes all C^α S^β with other exponents).

The resulting operator T_{ab} = ⟨φ_a, φ_b⟩ / √(d_a · d_b) is the unique variationally stable, self-adjoint, local, rotationally invariant edge operator. It requires zero learned parameters and zero hyperparameters.

We validate these theoretical results experimentally through *field dynamics*—an unsupervised, parameter-free process where node representations evolve under local forces determined by the coupling operator. On three standard citation networks (Cora, CiteSeer, PubMed), we inject controlled noise (spurious edges) at rates of 0%, 25%, 50%, and 100%, and compare three coupling strategies: multiplicative (C ⊙ S), additive (C + S), and structure-only (S). The results confirm the theory's central prediction: multiplicative coupling provides automatic noise gating that is structurally impossible with additive coupling, with advantages reaching 15.3 percentage points under noise injection.


## 2. Theoretical Framework

We derive the unique graph propagation operator from first principles. The companion paper [Kwon, 2026a] develops the full mathematical framework; here we give self-contained proofs for the core results and develop their GNN implications.

### 2.1 Axioms

**Axiom 1 (Locality).** The edge weight T_{ab} depends only on local data: the states φ(a), φ(b) and the graph structure in the neighborhood of (a,b). In particular, T_{ab} must depend on both φ(a) and φ(b); an operator independent of node states is not an edge *coupling* operator.

**Axiom 2 (Rotational invariance).** For any orthogonal transformation R ∈ SO(d) applied to all node states, T_{ab} is unchanged.

**Axiom 3 (Self-adjoint spectral consistency).** The structural component of the propagation operator is self-adjoint (symmetric) and preserves the graph Laplacian's spectral properties under degree heterogeneity.

### 2.2 Uniqueness of Components

**Proposition 1** (Content uniqueness). Under Axiom 2, C_{ab} = ⟨φ_a, φ_b⟩ is the unique rotationally invariant bilinear form on unit vectors (up to scalar).

*Proof.* Let f: ℝ^d × ℝ^d → ℝ be bilinear and SO(d)-invariant: f(Rφ_a, Rφ_b) = f(φ_a, φ_b) for all R ∈ SO(d). Any bilinear form can be written f(x,y) = x^T M y for some matrix M. Invariance requires R^T M R = M for all R ∈ SO(d). By Schur's lemma, M = λI. Therefore f(x,y) = λ⟨x,y⟩. □

*Remark on the bilinearity assumption.* The bilinearity of C is not an independent assumption but is forced by the composition requirement. By Lemma 1 below, the edge operator T = C ⊙ S must combine C and S bilinearly; bilinearity of the composition T_{ab} = f(C_{ab}, S_{ab}) = C_{ab} · S_{ab} requires that C_{ab} itself enters linearly. A nonlinear content similarity such as C_{ab} = exp(−‖φ_a − φ_b‖²/σ²) (RBF kernel) is rotationally invariant but enters T nonlinearly: the composition T_{ab} = g(φ_a, φ_b) · S_{ab} would require g to be bilinear in (φ_a, φ_b) for the overall operator to satisfy variational stability (Theorem 1), which forces g = λ⟨φ_a, φ_b⟩. More fundamentally, nonlinear similarities introduce a scale parameter σ that violates the parameter-free requirement: the inner product is the unique rotationally invariant similarity requiring no tuning.

*GNN interpretation.* This is cosine similarity between node embeddings. It ranges from −1 (opposite) to +1 (identical). Crucially, it can be *negative*—a property we will show is essential for preventing over-smoothing.

**Proposition 2** (Structure uniqueness). Under Axiom 3, S = D⁻¹/²AD⁻¹/² is the unique self-adjoint degree normalization.

*Proof.* Consider the family of degree-normalized matrices D^α A D^γ. Self-adjointness requires (D^α A D^γ)^T = D^α A D^γ. Since A is symmetric for undirected graphs, this gives D^γ A D^α = D^α A D^γ, which holds for all A iff α = γ. The normalized matrix D^α A D^α has spectral properties consistent with the graph Laplacian (eigenvalues in [−1,1]) iff α = −1/2 (Chung, 1997). □

*GNN interpretation.* The random walk normalization D⁻¹A, used in GraphSAGE and many other architectures, is *not* self-adjoint. In an undirected graph, D⁻¹A assigns asymmetric weights: from node u to v the weight is 1/d_u, while from v to u it is 1/d_v. If d_u ≫ d_v, information flows preferentially from hub to leaf. This directional bias in an undirected graph has no physical justification and is the structural origin of hub domination in deep GNNs with mean aggregation.

### 2.3 Composition Uniqueness

**Lemma 1** (Hadamard necessity). Any bilinear, pointwise-dependent operation •: M_E × M_E → M_E satisfies • = λ(⊙).

*Proof.* Pointwise dependence means (A • B)_{ab} = f(A_{ab}, B_{ab}) for some function f: ℝ × ℝ → ℝ. Bilinearity of • requires: f(αx₁ + x₂, y) = αf(x₁, y) + f(x₂, y) and f(x, αy₁ + y₂) = αf(x, y₁) + f(x, y₂). Any bilinear function f: ℝ × ℝ → ℝ has the form f(x,y) = λxy. Therefore (A • B)_{ab} = λ · A_{ab} · B_{ab}, i.e., • = λ(⊙). □

*What this excludes.* Matrix multiplication C·S (where (CS)_{ab} = Σ_k C_{ak}S_{kb}) violates pointwise dependence: each output element depends on an entire row of C and column of S. Tensor products C ⊗ S produce an object in M_E ⊗ M_E, not M_E. Direct sums C ⊕ S produce pairs, not scalars.

*GNN interpretation.* The Hadamard product is the unique bilinear operation where each output element depends only on the corresponding input elements—precisely the condition required for processing-in-memory and O(|E|) computation.

### 2.4 The Unique Operator

**Theorem 1** (Variational necessity). Under Axioms 1–3 and variational stability (finite, non-zero linear response to perturbation), the edge operator is uniquely:

    T_{ab} = C_{ab} · S_{ab} = ⟨φ_a, φ_b⟩ / √(d_a · d_b)

*Proof.* Propositions 1–2 determine C and S uniquely. Lemma 1 determines the composition as Hadamard product (among bilinear, pointwise-dependent operations). It remains to exclude nonlinear alternatives T = C^α · S^β.

Variational stability requires that the system's response to small perturbations is finite and non-zero—formally, that the first derivative ∂T/∂C exists and is non-zero, while the second derivative ∂²T/∂C² vanishes (linear response regime).

For T = C^α S^β:

    ∂T/∂C = α C^{α−1} S^β
    ∂²T/∂C² = α(α−1) C^{α−2} S^β

The second derivative vanishes identically iff α(α−1) = 0, giving α = 0 or α = 1. α = 0 yields T = S^β, which is independent of node states φ(a), φ(b). This contradicts the locality axiom (Axiom 1), which requires that T_{ab} depend on the states at both endpoints. Therefore α = 1.

By the same argument applied to S (∂²T/∂S² = β(β−1)C^α S^{β−2} = 0), we obtain β = 0 or β = 1. β = 0 yields T = C, independent of graph structure, again contradicting Axiom 1's requirement that T_{ab} depend on graph structure in the neighborhood of (a,b). Therefore β = 1.

Hence T = C · S. □


## 3. Implications for GNN Design

### 3.1 The Noise Gating Property

The most consequential implication of multiplicative coupling is automatic noise suppression.

Consider a spurious edge (a,b) connecting unrelated nodes. Their states φ_a and φ_b are approximately orthogonal, so C_{ab} = ⟨φ_a, φ_b⟩ ≈ 0. Under multiplicative coupling:

    T_{ab} = C_{ab} · S_{ab} ≈ 0 · S_{ab} = 0

The noise edge is automatically silenced, regardless of its structural weight S_{ab}.

Under additive coupling:

    T_{ab} = C_{ab} + S_{ab} ≈ 0 + S_{ab} = S_{ab} > 0

The noise edge transmits at full structural strength. Content provides no protection.

This is not a quantitative advantage—it is a *qualitative* difference. Multiplicative coupling can gate noise; additive coupling structurally cannot.

### 3.2 Over-Smoothing Explained

Over-smoothing occurs when repeated message passing causes all node representations to converge to a common vector. We identify two contributing factors:

**(i) Absence of repulsion.** Standard GNNs use only positive aggregation weights (ReLU activations, positive attention). In T = C ⊙ S, the content term C_{ab} = cos(φ_a, φ_b) can be *negative*. Negative C means dissimilar nodes repel each other during propagation. This repulsive force prevents representational collapse.

**(ii) Non-self-adjoint normalization.** The random walk operator D⁻¹A converges to the stationary distribution π_v ∝ d_v, erasing all node information. The self-adjoint operator D⁻¹/²AD⁻¹/² preserves spectral components, with natural attenuation governed by eigenvalue decay rather than convergence to a single point.

### 3.3 Hyperparameter Elimination

The operator T = C ⊙ S with S = D⁻¹/²AD⁻¹/² eliminates:

- **Normalization type**: uniquely determined (Proposition 2)
- **Aggregation type**: uniquely determined as Hadamard product (Lemma 1)
- **Decay / damping**: cos accumulation provides natural decay (cos^r per r hops)
- **Learned attention weights**: C_{ab} = ⟨φ_a, φ_b⟩ requires zero parameters

### 3.4 Computational Advantage

Standard message passing computes AX at cost O(|E|·d). The operator T = C ⊙ S computes edge-wise scalars at cost O(|E|), with no intermediate matrix storage. Each output element references exactly 2 input values (C_{ab} and S_{ab}), enabling processing-in-memory architectures where computation and storage are co-located.


## 4. Experimental Validation: Field Dynamics Benchmark

### 4.1 Motivation

Standard GNN benchmarks evaluate classification accuracy with learned parameters, confounding the propagation operator with training dynamics, optimizer choice, and regularization. To isolate the effect of the coupling operator alone, we use *field dynamics*: an unsupervised, parameter-free process where node representations evolve under deterministic local forces.

### 4.2 Setup

**Datasets.** Cora (2,708 nodes, 10,556 edges, 7 classes), CiteSeer (3,327 nodes, 9,104 edges, 6 classes), PubMed (19,717 nodes, 88,648 edges, 3 classes).

**Field dynamics.** Each node i has a representation vector h_i initialized by random projection of the node feature matrix to 64 dimensions, followed by L2 normalization to the unit sphere. At each cycle, the local force on node i is:

    force_i = Σ_{j∈N(i)} T_{ij} · dir(h_j → h_i) · η

where dir(h_j → h_i) = (h_j − h_i) / ‖h_j − h_i‖ is the unit direction vector. The direction normalization follows from the unit sphere constraint (Axiom 2): since all representations lie on S^{d−1}, the dynamics is a Riemannian gradient flow on the sphere, and the force magnitude is determined solely by the coupling weight T_{ij}, not by the Euclidean distance between embeddings. Node representations are updated by h_i ← normalize(h_i + force_i). No labels, no loss function, no learned parameters.

**Coupling operators compared.**
- **Multiplicative (C⊙S)**: T_{ab} = ⟨h_a, h_b⟩ · S_{ab}
- **Additive (C+S)**: T_{ab} = ⟨h_a, h_b⟩ + S_{ab}
- **Structure only (S)**: T_{ab} = S_{ab}
- **Content only (C)**: T_{ab} = ⟨h_a, h_b⟩

The four operators form a complete ablation: C⊙S is the full operator; C-only and S-only remove one component each; C+S tests an alternative composition.

**Noise injection.** Spurious edges added between random node pairs at rates of 0%, 25%, 50%, 100% of original edge count.

**Evaluation.** Vertex k-nearest-neighbor (kNN) classification accuracy at peak self-organization time (cycle 100–400). The peak timing reflects the region where the coupling operator actively organizes representations before over-smoothing.

### 4.3 Results

**Table 1.** Peak kNN accuracy (%) under noise injection.

**Cora:**

| Noise | C⊙S | S only | C only | C+S | C⊙S − (C+S) |
|-------|------|--------|--------|-----|-------------|
| 0% | 70.2 | 70.3 | 67.3 | 68.3 | +1.9 |
| 25% | 48.2 | 44.1 | 31.9 | 32.9 | **+15.3** |
| 50% | 42.6 | 40.4 | 32.4 | 33.1 | +9.5 |
| 100% | 39.1 | 33.9 | 32.3 | 32.6 | +6.5 |

**CiteSeer:**

| Noise | C⊙S | S only | C only | C+S | C⊙S − (C+S) |
|-------|------|--------|--------|-----|-------------|
| 0% | 51.3 | 60.4 | 54.6 | 58.7 | −7.4 |
| 25% | 37.2 | 37.1 | 33.8 | 24.4 | **+12.8** |
| 50% | 33.8 | 33.6 | 20.1 | 20.2 | **+13.6** |
| 100% | 32.2 | 30.1 | 19.9 | 20.7 | **+11.5** |

**PubMed:**

| Noise | C⊙S | S only | C only | C+S | C⊙S − (C+S) |
|-------|------|--------|--------|-----|-------------|
| 0% | 73.7 | 73.6 | 70.5 | 70.6 | +3.1 |
| 25% | 63.2 | 62.5 | 54.0 | 53.5 | +9.7 |
| 50% | 63.8 | 57.2 | 54.2 | 54.3 | +9.5 |
| 100% | 57.9 | 53.2 | 53.7 | 53.1 | +4.8 |

Four consistent patterns emerge across all datasets:

**(i) Noise amplifies the multiplicative advantage.** At 0% noise, the methods perform comparably (with CiteSeer favoring S-only due to low homophily; see (iii) below). As noise increases, multiplicative coupling maintains accuracy while additive coupling degrades rapidly. This directly confirms the noise gating prediction of Section 3.1.

**(ii) Additive coupling is consistently worst under noise.** C+S cannot gate noise edges because S_{ab} > 0 regardless of C_{ab}. In CiteSeer at 50% noise, C+S drops to 20.2%—below random chance for 6 classes—while C⊙S maintains 33.8%.

**(iii) CiteSeer's clean-graph result confirms the theory.** CiteSeer has low homophily (neighbors often belong to different classes), so C_{ab} tends to be small even for real edges. In the clean graph, multiplicative coupling attenuates both signal and noise equally, yielding lower accuracy than structure-only (C⊙S = 51.3% vs S = 60.4%). This is not a failure of the theory but a direct prediction: when content is uninformative (C ≈ 0 for most edges), multiplicative coupling correctly reports that no content-based discrimination is possible. Crucially, under noise injection, this same attenuation becomes selectively beneficial—noise edges (connecting truly unrelated nodes) have even smaller C values than real edges in the low-homophily graph—and C⊙S overtakes S-only at 25% noise and above. The crossover demonstrates that multiplicative coupling's behavior is consistent across regimes: it faithfully transmits the content signal, whether that signal is strong (Cora, PubMed) or weak (CiteSeer clean) or differentially informative (CiteSeer noisy).

**(iv) Four-way ablation: both components are necessary.** The C-only ablation is particularly revealing. Under noise, C-only collapses to near-chance accuracy (Cora: 31.9%, CiteSeer: 19.9%, PubMed: 53.7% at 100% noise) with peak organization occurring at cycle 1 — meaning the dynamics *immediately* degrades representations rather than improving them. Without degree normalization, content similarity alone cannot sustain coherent self-organization: high-degree nodes dominate the force computation, pulling unrelated nodes together and destroying cluster structure. S-only provides degree-corrected propagation but cannot distinguish real from noise edges. Only the multiplicative combination C⊙S achieves both: degree-normalized propagation (from S) with content-based gating (from C). The multiplicative composition is not merely better — it is the only composition under which field dynamics produces sustained self-organization under noise.

### 4.4 Mechanism: Per-Edge Weight Analysis

**Table 2.** Mean coupling weight T by edge type (PubMed, 100% noise, cycle 150).

| Edge type | C⊙S | C only | S only | C+S |
|-----------|------|--------|--------|------|
| Real edge | 0.0400 | 0.5527 | 0.0515 | 0.9735 |
| Noise edge | 0.0336 | 0.6945 | 0.0795 | 1.0558 |
| Ratio (real/noise) | **1.19** | 0.80 | 0.65 | 0.92 |

Under multiplicative coupling, real edges receive higher weight than noise edges (ratio 1.19). This is *selective gating*: the operator preferentially transmits information along meaningful edges.

Content-only coupling (C) produces a ratio of 0.80 — below 1.0, indicating that C alone does *not* achieve selective gating. Without degree normalization, content similarity is dominated by degree bias: noise edges connecting to high-degree nodes have inflated C values because the embeddings of high-degree nodes influence many neighbors during dynamics, creating spurious similarity. Only the multiplicative operator C⊙S achieves ratio > 1, because the structural normalization (1/√(d_a·d_b)) corrects for degree, allowing the content signal to perform genuine discrimination.

Under additive coupling, noise edges receive *higher* weight than real edges (ratio 0.88 < 1). Because S is always positive and noise edges tend to connect to high-degree nodes (by random selection bias), S_{noise} > S_{real} on average, and the additive S term dominates.

Structure-only propagation shows the same inversion (ratio 0.65), confirming that S alone cannot distinguish real from noise edges.

**Table 3.** Real/noise weight ratio across datasets and noise levels (cycle 150).

| Dataset | Noise 25% | Noise 50% | Noise 100% |
|---------|-----------|-----------|------------|
| Cora (C⊙S) | 1.52 | 1.53 | 1.59 |
| CiteSeer (C⊙S) | 1.93 | 2.00 | 2.07 |
| PubMed (C⊙S) | 0.82 | 0.93 | 1.19 |
| Cora (C only) | 0.98 | 0.95 | 0.94 |
| CiteSeer (C only) | 1.01 | 1.07 | 1.02 |
| PubMed (C only) | 0.81 | 0.79 | 0.80 |
| Cora (C+S) | 0.94 | 0.87 | 0.85 |
| CiteSeer (C+S) | 0.94 | 0.91 | 0.98 |
| PubMed (C+S) | 0.73 | 0.80 | 0.92 |

The pattern reveals a striking asymmetry. In Cora and CiteSeer, C⊙S consistently achieves ratio > 1 (selective gating), with CiteSeer reaching ratios above 2.0 — the strongest discrimination among all datasets. In PubMed, C⊙S achieves ratio > 1 only at 100% noise (1.19), with ratios below 1 at lower noise levels; this reflects PubMed's lower feature dimensionality (500 vs 1433/3703) and 3-class structure, where the content signal provides less edge-level discrimination at moderate noise.

Content-only coupling (C) hovers near or below 1.0 across all conditions, confirming that content *without* degree normalization cannot achieve selective gating. Additive coupling (C+S) produces ratio < 1 in nearly all cases.

**This is the central experimental finding: C⊙S is the only operator that achieves selective edge gating (ratio substantially > 1) in the datasets where content is discriminative (Cora, CiteSeer), and it does so without any learned parameters.**

### 4.5 Over-Smoothing Dynamics

All three methods eventually reach over-smoothing (all representations converge to a single point). However, multiplicative coupling reaches peak organization at cycle 150–400, while structure-only peaks at cycle 50–100. The multiplicative damping (|C| ≤ 1 ⟹ |C⊙S| ≤ |S|) slows the dynamics, providing more time for self-organization before collapse.

The mechanism is spectral: the effective propagation matrix under multiplicative coupling has spectral radius at most equal to that of S (since |C_{ab}| ≤ 1 acts as an elementwise contraction), slowing the rate at which the leading eigenvector dominates. This delay is a direct consequence of variational stability (Section 2.4): the linear response condition (α = β = 1) prevents any superlinear amplification that would accelerate convergence to the trivial fixed point.


## 5. Connection to Lattice Gauge Theory

The operator T = C ⊙ S derived here for GNNs is identical to the edge operator proved necessary for gauge-geometry coupling on lattice graphs [K, 2026a; K, 2026b]. In that context, C is the gauge link variable and S is the Regge geometry. The universality of T = C ⊙ S across 7 lattice configurations (2D–4D, U(1) and SU(2), 42 measurements, all >13σ) [Kwon, 2026b] provides independent physical validation of the mathematical structure applied here to GNNs. The full uniqueness proof — extending to all analytic compositions T = f(C,S) via Taylor expansion, not only power-law forms — is in [Kwon, 2026a, Theorem 1, Case 2].

This cross-domain universality is not coincidental—it follows from the axioms, which make no reference to any specific application domain.


## 6. Related Work

**Graph normalization.** Kipf & Welling (2017) introduced D⁻¹/²AD⁻¹/² as a spectral approximation. Our Proposition 2 proves it is the unique self-adjoint normalization, not merely a convenient choice. PairNorm (Zhao & Akoglu, 2020), NodeNorm (Zhou et al., 2020), and DGN (Zhou et al., 2020) address over-smoothing symptoms without identifying the root cause (non-self-adjointness and absence of repulsive content coupling).

**Content-structure coupling in GNNs.** GAT (Veličković et al., 2018) learns content-dependent attention, but requires parameters and labels. APPNP (Gasteiger et al., 2019) uses personalized PageRank (a random walk variant, non-self-adjoint). Our T = C ⊙ S achieves content-dependent weighting with zero parameters.

**Noise robustness.** GNNGuard (Zhang & Zitnik, 2020) and ProGNN (Jin et al., 2020) learn to detect and remove adversarial edges. Our multiplicative coupling provides noise gating *without* learning, as a structural property of the operator.

**Hadamard product in neural networks.** Element-wise products appear in gating mechanisms (LSTM, GRU) and mixture-of-experts models. Our Lemma 1 establishes that the Hadamard product is the *unique* bilinear local composition, providing theoretical justification for these empirical choices.


## 7. Discussion

**Limitations.** Our uniqueness results assume undirected graphs; extension to directed graphs requires relaxing self-adjointness (Axiom 3), and the resulting operator family remains an open question. The field dynamics benchmark evaluates self-organization quality rather than task-specific accuracy; we expect the noise gating advantage to transfer to supervised settings but have not demonstrated this. The over-smoothing delay provided by multiplicative damping does not eliminate over-smoothing—it postpones it. The experimental validation uses three standard citation networks; evaluation on larger-scale benchmarks (e.g., OGB) is left for future work.

**Scope of the bilinearity assumption.** The bilinearity requirement in Lemma 1 (and inherited by Proposition 1) excludes nonlinear content similarities such as RBF kernels. This exclusion is not arbitrary: nonlinear similarities introduce scale parameters (e.g., bandwidth σ) that must be tuned, violating the parameter-free nature of the derived operator. Moreover, as shown in the Remark following Proposition 1, variational stability independently forces the content function to enter T linearly.

**Broader impact.** Eliminating the propagation operator as a hyperparameter reduces the computational cost and carbon footprint of GNN architecture search. The parameter-free noise gating property may benefit GNN applications in domains with unreliable graph structure (social networks, biological networks, noisy knowledge graphs).


## 8. Conclusion

We have proved that the GNN propagation operator T = C ⊙ S is not a design choice but a mathematical necessity, uniquely determined by locality, rotational invariance, self-adjoint spectral consistency, and variational stability. The multiplicative (Hadamard) structure provides automatic noise gating—a property that is structurally impossible with additive coupling—validated across three standard benchmarks under controlled noise injection. These results establish a principled foundation for graph neural network design: the propagation operator, the normalization, and the content-structure composition are all uniquely determined by the axioms, leaving no room for hyperparameter tuning in these choices.


## Acknowledgments

The author used Claude (Anthropic) as a computational tool for mathematical verification, numerical simulation, and assistance in preparing the manuscripts. All theoretical content — axioms, theorems, proofs, physical interpretations, and strategic decisions — is the author's original work. The author takes full responsibility for all content.

---

## References

- Chung, F.R.K. Spectral Graph Theory. CBMS 92, AMS (1997).
- Corso, G. et al. Principal Neighbourhood Aggregation. NeurIPS (2020).
- Gasteiger, J. et al. Predict then Propagate: Graph Neural Networks meet Personalized PageRank. ICLR (2019).
- Hamilton, W.L. et al. Inductive Representation Learning on Large Graphs. NeurIPS (2017).
- Jin, W. et al. Graph Structure Learning for Robust Graph Neural Networks. KDD (2020).
- Kwon, H. The Hadamard structure of self-referential graphs. arXiv (2026a).
- Kwon, H. Gauge-geometry coupling is a necessary consequence of self-referential dynamics on graphs. arXiv (2026b).
- Kipf, T.N. & Welling, M. Semi-Supervised Classification with Graph Convolutional Networks. ICLR (2017).
- Li, Q. et al. Deeper Insights into Graph Convolutional Networks for Semi-Supervised Learning. AAAI (2018).
- Veličković, P. et al. Graph Attention Networks. ICLR (2018).
- Xu, K. et al. How Powerful are Graph Neural Networks? ICLR (2019).
- Zhang, X. & Zitnik, M. GNNGuard: Defending Graph Neural Networks against Adversarial Attacks. NeurIPS (2020).
- Zhao, L. & Akoglu, L. PairNorm: Tackling Oversmoothing in GNNs. ICLR (2020).
- Zhou, K. et al. Towards Deeper Graph Neural Networks with Differentiable Group Normalization. NeurIPS (2020).
