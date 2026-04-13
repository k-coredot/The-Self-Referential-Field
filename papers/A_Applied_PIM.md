# Processing-in-Memory as the Unique Architecture
# for Content-Structure Computation:
# From the Hadamard Operator to ReRAM Crossbar Circuits

Hyeokjun Kwon — April 2026

---

**Abstract.** The Hadamard product T = C⊙S — proved to be the unique variationally stable composition of content and structure on graphs (Kwon 2026a) — has a direct hardware realization: the analog crossbar array. In a resistive memory (ReRAM) crossbar, Ohm's law computes the elementwise product of input voltage (content) and conductance (structure) at each junction, without data transfer between memory and processor. We show that this correspondence is not an analogy but a structural identity: (1) the crossbar naturally computes the Hadamard product, not matrix multiplication; (2) the self-adjoint normalization D⁻¹/²AD⁻¹/² maps to symmetric conductance scaling, automatically correcting degree imbalance; (3) the computational complexity reduces from O(n²) (matrix multiplication) to O(|E|) (number of edges), matching the sparsity of real graphs; and (4) the variational stability condition (α = β = 1) excludes all non-linear activation-in-memory schemes. These results establish processing-in-memory not as an engineering optimization but as the physically necessary architecture for content-structure computation.

---

## 1. The Correspondence

### 1.1 The Problem

Graph neural networks, recommendation systems, knowledge graphs, and lattice simulations all compute operations of the form "combine content at nodes with the structure of their connections." The standard approach separates storage (memory) and computation (processor): structure is stored in memory, content is transferred to the processor, computation occurs, results are transferred back.

This separation creates the von Neumann bottleneck: data transfer dominates energy and time. For sparse graphs with millions of nodes, the transfer cost overwhelms the computation cost.

### 1.2 The Observation

Paper A proved that the unique variationally stable composition of content C and structure S is the Hadamard (elementwise) product: T_{ab} = C_{ab} · S_{ab}. This operation has a special property: **it is local.** Each output element depends only on the corresponding input elements at the same position. No element depends on any other position.

A ReRAM crossbar junction stores a conductance G_{ab} (structure) and receives an input voltage V_a (content). Ohm's law gives the current I_{ab} = V_a · G_{ab}. This is the Hadamard product, computed in place, with zero data transfer.

### 1.3 The Claim

This correspondence is not coincidental. The Hadamard product is the **unique** operation that is:
- Bilinear (required by variational stability)
- Pointwise (required by locality)
- Scalar-valued (required by edge-level computation)

These are exactly the properties that make in-memory computation possible. Matrix multiplication is bilinear but non-local (each output depends on an entire row and column). Tensor products are local but not scalar-valued. Only the Hadamard product satisfies all three.

**Processing-in-memory is not an engineering choice. It is the unique architecture for content-structure computation.**

## 2. Four Structural Advantages

### 2.1 Natural Hadamard Computation

In a crossbar array with conductances G_{ij} and input voltages V_i:

I_{ij} = V_i × G_{ij}   (Ohm's law at each junction)

This is T_{ij} = C_{ij} × S_{ij} with C → V and S → G. The computation happens at the physical location of the data. No fetch, no transfer, no cache.

Standard matrix-vector multiplication in a crossbar computes y_j = Σ_i V_i G_{ij} (Kirchhoff's current law sums the column). This is **not** the Hadamard product — it is the matrix product, which Lemma 1 of Paper A proved is not the correct composition. The individual junction currents I_{ij} = V_i G_{ij}, before column summation, are the Hadamard product.

### 2.2 Automatic Degree Normalization

The self-adjoint normalized adjacency S = D⁻¹/²AD⁻¹/² (Proposition 2, Paper A) scales each edge by 1/√(d_source × d_target). In a crossbar, this maps to:

G_{ij}^{normalized} = G_{ij} / √(Σ_k G_{ik}) / √(Σ_k G_{kj})

This can be implemented by resistive voltage dividers at row and column terminals, using the total row/column conductance as the normalization factor. The normalization is symmetric (self-adjoint) — each edge is scaled by both endpoints, not just the source.

This automatically corrects degree imbalance: hub nodes (high degree) have their per-edge influence reduced by √d, giving each neighbor equal voice. No software-level normalization is needed.

### 2.3 Sparsity-Natural Complexity

Matrix multiplication on a dense n×n matrix requires O(n²) operations. The Hadamard product on a sparse graph with |E| edges requires O(|E|) operations — only non-zero entries are computed.

In a crossbar, this maps directly: only junctions with non-zero conductance (physical connections) carry current. Zero-conductance junctions consume no energy. The hardware automatically exploits graph sparsity.

For a social network with 10⁶ nodes and average degree 100: matrix multiplication requires 10¹² operations; Hadamard product requires 10⁸. A factor of 10,000 in energy and time.

### 2.4 Variational Stability Excludes Nonlinear PIM

The variational stability condition (Paper A, Theorem 1) requires α = β = 1 in T = C^α S^β. This excludes:
- Quadratic compositions T = C² · S (α = 2): non-uniform sensitivity
- Activation-in-memory T = σ(C · S) where σ is nonlinear: violates linearity
- Power-law compositions T = C^α S^β with α ≠ 1 or β ≠ 1: excluded by ∂²T/∂C² = 0

In hardware terms: the junction should compute the **linear** product V × G, not V² × G or tanh(V × G). Nonlinear activation functions, if needed, should be applied **after** the in-memory Hadamard computation, not during it.

This is a design constraint from the mathematics, not from engineering convenience.

## 3. Architecture

### 3.1 Single-Layer PIM Graph Processor

```
Input: node feature vectors {v_i} (content)
Stored: edge conductances {G_{ij}} (structure)
Output: updated node features {v'_i}

For each node i:
  1. Apply voltage v_i to row i
  2. Read junction currents I_{ij} = v_i × G_{ij}  (Hadamard product)
  3. Normalize: I_{ij}^{norm} = I_{ij} / √(d_i × d_j)  (degree correction)
  4. Aggregate: v'_i = Σ_j I_{ij}^{norm}  (column sum, Kirchhoff)
```

Steps 1–2 are in-memory (zero transfer). Step 3 requires row/column conductance sums (precomputable). Step 4 is a physical sum (Kirchhoff's current law).

### 3.2 Multi-Scale Architecture

For graph neural networks with L layers:
- L crossbar arrays in series
- Each array stores one layer's edge weights
- Output of layer l feeds directly into layer l+1 (no intermediate storage)
- Total data transfer: input features in + output features out
- All intermediate computation: in-memory

### 3.3 Comparison with Existing PIM

| Architecture | Operation | Data Transfer | Normalization |
|---|---|---|---|
| Standard GPU | Matrix multiply | O(n²) per layer | Software (asymmetric OK) |
| Conventional PIM | Matrix-vector product | O(n) per layer | Software |
| **Hadamard PIM** | **Elementwise product** | **O(1) per layer** | **Hardware (symmetric)** |

The Hadamard PIM eliminates per-layer data transfer entirely. The only transfer is initial input and final output.

## 4. Predicted Performance

### 4.1 Energy

Energy per operation in a ReRAM junction: ~1 fJ (femtojoule).
Operations per graph layer: |E| (number of edges).
For a graph with 10⁶ nodes, average degree 100: |E| = 10⁸.
Energy per layer: 10⁸ × 10⁻¹⁵ J = 100 nJ.

Compared to GPU (estimated 10 μJ per layer for same graph): **100× energy reduction**.

### 4.2 Latency

Crossbar computation is analog and parallel: all junctions compute simultaneously.
Latency per layer: ~10 ns (RC time constant of crossbar).
For L = 3 layers: 30 ns.

Compared to GPU (estimated 1 ms for sparse matrix operations): **30,000× latency reduction**.

### 4.3 Scaling

Energy and latency scale as O(|E|), not O(n²). For scale-free graphs (degree distribution follows power law), |E| ~ n × ⟨k⟩ where ⟨k⟩ is average degree (constant for most real networks). Therefore: **linear scaling in number of nodes**.

## 5. Material Candidates

| Platform | Conductance Range | Endurance | Maturity |
|---|---|---|---|
| HfO₂ ReRAM | 10 μS – 1 mS | 10⁶ cycles | Production |
| TaOₓ ReRAM | 1 μS – 500 μS | 10⁸ cycles | Research |
| Phase-change (GST) | 10 μS – 10 mS | 10⁹ cycles | Production |
| Ferroelectric (HZO) | Analog, 4-bit | 10¹⁰ cycles | Research |

All platforms support the key requirement: analog conductance representing continuous edge weights.

## 6. Discussion

### 6.1 What This Is

This paper establishes that processing-in-memory is not merely faster or more efficient — it is the **structurally correct** architecture for computing T = C⊙S. The Hadamard product requires locality; locality requires co-located storage and computation; co-located storage and computation is the definition of processing-in-memory.

### 6.2 What This Is Not

This paper does not claim that all computation should be in-memory. Operations that are not Hadamard products (e.g., sorting, branching, sequential logic) do not benefit from this architecture. The claim is specific: for content-structure computation on graphs, PIM is the unique correct architecture.

### 6.3 Relation to the Series

Paper A proved T = C⊙S is unique. Paper C showed it outperforms alternatives in GNN benchmarks. This paper shows its hardware realization is processing-in-memory. The mathematical structure determines the computation; the computation determines the architecture; the architecture determines the hardware.

## 7. Conclusion

The Hadamard product T = C⊙S is the unique content-structure composition (Paper A). It is pointwise, bilinear, and scalar — the three properties that make in-memory computation possible and correct. A ReRAM crossbar naturally computes this product through Ohm's law, with automatic degree normalization through conductance scaling, O(|E|) complexity through sparsity exploitation, and no data transfer through physical co-location. Processing-in-memory is not an optimization — it is the necessary architecture for the necessary operation.

## Acknowledgments

The author used Claude (Anthropic) as a computational tool for mathematical verification, numerical simulation, and assistance in preparing the manuscripts. All theoretical content — axioms, theorems, proofs, physical interpretations, and strategic decisions — is the author's original work. The author takes full responsibility for all content.

---

## References

- Kwon, H. The Hadamard structure of self-referential graphs. arXiv (2026a).
- Kwon, H. Multiplicative coupling in GNNs. arXiv (2026c).
- Ielmini, D. & Wong, H.-S.P. In-memory computing with resistive switching devices. Nature Electronics 1, 333 (2018).
- Sebastian, A. et al. Memory devices and applications for in-memory computing. Nature Nanotechnology 15, 529 (2020).
- Kipf, T.N. & Welling, M. Semi-Supervised Classification with GCNs. ICLR (2017).
