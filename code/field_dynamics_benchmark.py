"""
Field Dynamics Benchmark — T = C⊙S in its native environment

§0.1: "장이 존재한다. 자기를 읽는다. 읽는 행위가 장을 변형한다."

읽기(coupling 계산)와 쓰기(embedding 이동)가 동일한 연산.
외부 목적함수 없음. cross-entropy 없음. 역전파 없음.
장 자체의 역학으로 자기조직화.

각 순환:
  C = cos(emb_a, emb_b) — 내용 (동적: 매 순환 변함)
  S = 1/√(d_a·d_b)     — 구조 (정적: 그래프 토폴로지)
  T = coupling(C, S)    — 결합 연산자
  force_i = Σ_j dir(j→i) × T_ij × step — 국소 힘
  emb_i += force_i; normalize — 이동
  → emb 변화 → C 변화 → T 변화 → 다음 순환

예측:
  C⊙S: 유사 노드 강결합, 비유사 약/반발 → 명확 군집
  C+S: S > 0이므로 비유사도 끌림 → 불명확
  S만: 균일 결합 → 과도 평활화 → 단일 점 수렴
  노이즈: C≈0 → C⊙S≈0 (차단), C+S≈S (전파)

평가: kNN 정확도 (비지도 — 학습 없음)

!pip install torch-geometric ogb -q
"""
import torch, torch.nn.functional as F
import numpy as np, time, json, math

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Device: {device}")
if device.type == 'cuda':
    print(f"  GPU: {torch.cuda.get_device_name()}")
    print(f"  Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")

# ================================================================
# Core ops
# ================================================================

def compute_C(emb, ei):
    """Cosine similarity. emb is L2-normalized. Range [-1, 1]."""
    r, c = ei[0], ei[1]
    return (emb[r] * emb[c]).sum(dim=1)

def compute_S(ei, N):
    """Degree-normalized edge weight. S_ab = 1/√(d_a·d_b). Always ≥ 0."""
    r, c = ei[0], ei[1]
    d = torch.zeros(N, device=ei.device)
    d.scatter_add_(0, r, torch.ones(r.size(0), device=ei.device))
    d = d.clamp(min=1.0)
    return 1.0 / torch.sqrt(d[r] * d[c])

def add_noise_edges(ei, N, ratio):
    if ratio == 0:
        return ei
    n_noise = int(ei.size(1) * ratio)
    src = torch.randint(0, N, (n_noise,), device=ei.device)
    tgt = torch.randint(0, N, (n_noise,), device=ei.device)
    mask = src != tgt
    nei = torch.stack([src[mask], tgt[mask]])
    nei = torch.cat([nei, torch.stack([nei[1], nei[0]])], 1)
    return torch.unique(torch.cat([ei, nei], 1), dim=1)

def classify_edges(ei, ei_orig, N):
    """Classify edges as original or noise."""
    key_full = ei[0].long() * N + ei[1].long()
    key_orig = ei_orig[0].long() * N + ei_orig[1].long()
    is_orig = torch.isin(key_full, key_orig)
    return is_orig

# ================================================================
# Coupling functions
# ================================================================

def coupling_CmulS(C, S):
    """T = C ⊙ S. Signed. No clamp."""
    return C * S

def coupling_CaddS(C, S):
    """T = C + S. S always positive, so T > 0 when C > -S."""
    return C + S

def coupling_S(C, S):
    """T = S. No content. Always positive."""
    return S

# ================================================================
# Field dynamics engine
# ================================================================

def run_field_dynamics(emb_init, ei, N, coupling_fn, n_cycles=500,
                       step_size=0.05, eval_every=50,
                       labels=None, train_mask=None, test_mask=None,
                       ei_orig=None):
    """Run field dynamics. Returns trajectory of metrics.

    Each cycle:
      1. Compute C from current embeddings (reading)
      2. Compute T = coupling(C, S)
      3. Compute force per node from neighbors
      4. Move embeddings (writing)
      5. Normalize to unit sphere
      → C changes → next cycle's T changes (self-referential loop)
    """
    emb = emb_init.clone()
    S = compute_S(ei, N)  # fixed (graph topology)
    r, c = ei[0], ei[1]

    trajectory = []
    has_noise = ei_orig is not None

    for cyc in range(1, n_cycles + 1):
        # === Reading: compute coupling ===
        C = compute_C(emb, ei)
        T = coupling_fn(C, S)

        # === Writing: compute and apply forces ===
        d_vec = emb[r] - emb[c]  # direction: source → target (force on target toward source)
        d_norm = F.normalize(d_vec, dim=1)
        force_edges = d_norm * T.unsqueeze(1) * step_size  # (E, d)

        force = torch.zeros_like(emb)
        force.scatter_add_(0, c.unsqueeze(1).expand_as(force_edges), force_edges)

        emb = F.normalize(emb + force, dim=1)

        # === Evaluate periodically ===
        if cyc % eval_every == 0 or cyc == 1:
            metrics = {'cycle': cyc}

            # kNN accuracy
            if labels is not None and train_mask is not None and test_mask is not None:
                acc = knn_accuracy(emb, labels, train_mask, test_mask, k=10)
                metrics['knn_acc'] = round(acc * 100, 2)

            # Cluster quality (sample for large graphs)
            if labels is not None:
                intra, inter = cluster_quality(emb, labels, N)
                metrics['intra'] = round(intra, 4)
                metrics['inter'] = round(inter, 4)
                metrics['ratio'] = round(intra / max(abs(inter), 1e-6), 2)

            # Edge coupling diagnostics
            metrics['T_mean'] = round(T.mean().item(), 4)
            metrics['T_std'] = round(T.std().item(), 4)
            metrics['C_mean'] = round(C.mean().item(), 4)

            # Noise edge diagnostics
            if has_noise:
                is_orig = classify_edges(ei, ei_orig, N)
                metrics['T_orig'] = round(T[is_orig].mean().item(), 4)
                metrics['T_noise'] = round(T[~is_orig].mean().item(), 4)
                metrics['C_orig'] = round(C[is_orig].mean().item(), 4)
                metrics['C_noise'] = round(C[~is_orig].mean().item(), 4)

            trajectory.append(metrics)

    return emb, trajectory

# ================================================================
# Evaluation
# ================================================================

def knn_accuracy(emb, labels, train_mask, test_mask, k=10):
    """kNN classification on embeddings. No training needed."""
    train_emb = emb[train_mask]
    train_labels = labels[train_mask]
    test_emb = emb[test_mask]
    test_labels = labels[test_mask]

    # Cosine similarity (embeddings are L2 normalized)
    sim = test_emb @ train_emb.t()
    _, topk_idx = sim.topk(k, dim=1)
    topk_labels = train_labels[topk_idx]

    # Majority vote
    pred = torch.zeros(test_emb.size(0), dtype=torch.long, device=emb.device)
    for i in range(test_emb.size(0)):
        vals, counts = topk_labels[i].unique(return_counts=True)
        pred[i] = vals[counts.argmax()]

    return (pred == test_labels).float().mean().item()

def cluster_quality(emb, labels, N, max_sample=2000):
    """Average intra-class and inter-class cosine similarity."""
    if N > max_sample:
        idx = torch.randperm(N, device=emb.device)[:max_sample]
        emb_s = emb[idx]
        labels_s = labels[idx]
    else:
        emb_s = emb
        labels_s = labels

    n = emb_s.size(0)
    sim = emb_s @ emb_s.t()
    same = labels_s.unsqueeze(0) == labels_s.unsqueeze(1)
    mask_diag = ~torch.eye(n, dtype=torch.bool, device=emb.device)

    same_off = same & mask_diag
    diff_off = ~same & mask_diag

    intra = sim[same_off].mean().item() if same_off.any() else 0.
    inter = sim[diff_off].mean().item() if diff_off.any() else 0.
    return intra, inter

# ================================================================
# Data loading
# ================================================================

def load_datasets():
    import functools
    if not hasattr(torch, '_lp7'):
        _orig = torch.load
        @functools.wraps(_orig)
        def _pl(*a, **kw): kw.setdefault('weights_only', False); return _orig(*a, **kw)
        torch.load = _pl; torch._lp7 = True

    from torch_geometric.datasets import Planetoid
    import torch_geometric.transforms as Tr
    ds = {}
    for nm in ['Cora', 'CiteSeer', 'PubMed']:
        d = Planetoid(root=f'/tmp/{nm}', name=nm, transform=Tr.NormalizeFeatures())[0].to(device)
        ds[nm] = d
        print(f"  {nm}: {d.num_nodes}n {d.num_edges}e")
    return ds

# ================================================================
# Main
# ================================================================

def run():
    print()
    datasets = load_datasets()

    EMB_DIM = 64
    N_CYCLES = 500
    STEP_SIZE = 0.05
    EVAL_EVERY = 50
    NOISES = [0.0, 0.25, 0.5, 1.0]

    couplings = {
        'C*S': coupling_CmulS,
        'C+S': coupling_CaddS,
        'S':   coupling_S,
    }

    all_results = {}

    for dn, data in datasets.items():
        N = data.num_nodes
        ne = data.edge_index.size(1)
        in_dim = data.num_node_features
        out_dim = int(data.y.max().item()) + 1
        ei_orig = data.edge_index

        print(f"\n{'#' * 70}")
        print(f"#  {dn}  ({N}n {ne}e, {out_dim} classes)")
        print(f"{'#' * 70}")

        # Fixed random projection for initial embeddings
        torch.manual_seed(42)
        proj = torch.randn(in_dim, EMB_DIM, device=device)
        proj = proj / math.sqrt(EMB_DIM)
        emb_init = F.normalize(data.x @ proj, dim=1)

        # Verify initial C quality
        C_init = compute_C(emb_init, ei_orig)
        same_class_edges = (data.y[ei_orig[0]] == data.y[ei_orig[1]])
        c_same = C_init[same_class_edges].mean().item()
        c_diff = C_init[~same_class_edges].mean().item()
        print(f"  Initial: C_same={c_same:.3f}, C_diff={c_diff:.3f}, gap={c_same-c_diff:.3f}")

        ds_results = {}

        for noise in NOISES:
            torch.manual_seed(9999)
            ei_n = add_noise_edges(ei_orig, N, noise)
            n_e = ei_n.size(1)

            print(f"\n  ═══ Noise={noise:.0%} ({n_e}e) ═══")

            for cn, cfn in couplings.items():
                t0 = time.time()
                emb_final, traj = run_field_dynamics(
                    emb_init, ei_n, N, cfn,
                    n_cycles=N_CYCLES, step_size=STEP_SIZE,
                    eval_every=EVAL_EVERY,
                    labels=data.y, train_mask=data.train_mask, test_mask=data.test_mask,
                    ei_orig=ei_orig if noise > 0 else None,
                )
                dt = time.time() - t0

                # Print trajectory
                print(f"\n    --- {cn} (noise={noise:.0%}) ---  [{dt:.1f}s]")
                for m in traj:
                    line = f"      cyc={m['cycle']:>4}: kNN={m.get('knn_acc', '---'):>5}"
                    line += f"  intra={m.get('intra', 0):+.3f}  inter={m.get('inter', 0):+.3f}"
                    line += f"  ratio={m.get('ratio', 0):>5}"
                    line += f"  C_mean={m.get('C_mean', 0):+.4f}"
                    if 'T_orig' in m:
                        line += f"  T_orig={m['T_orig']:+.4f}  T_noise={m['T_noise']:+.4f}"
                    print(line)

                # Store final metrics
                final = traj[-1] if traj else {}
                key = f"n{noise:.0%}"
                if cn not in ds_results:
                    ds_results[cn] = {}
                ds_results[cn][key] = final

        all_results[dn] = ds_results

        # Summary table
        print(f"\n{'=' * 70}")
        print(f"  {dn}: Field Dynamics Summary (cycle {N_CYCLES})")
        print(f"{'=' * 70}")
        print(f"  {'Noise':>8}  {'S-kNN':>7}  {'C+S-kNN':>8}  {'C*S-kNN':>8}"
              f"  {'C*S−S':>7}  {'C*S−C+S':>8}")
        for noise in NOISES:
            key = f"n{noise:.0%}"
            s_acc = ds_results.get('S', {}).get(key, {}).get('knn_acc', 0.)
            cs_acc = ds_results.get('C*S', {}).get(key, {}).get('knn_acc', 0.)
            cps_acc = ds_results.get('C+S', {}).get(key, {}).get('knn_acc', 0.)
            print(f"  {noise:>7.0%}  {s_acc:>6.1f}  {cps_acc:>7.1f}  {cs_acc:>7.1f}"
                  f"  {cs_acc - s_acc:+6.1f}  {cs_acc - cps_acc:+7.1f}")

    out_file = 'field_dynamics_results.json'
    with open(out_file, 'w') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    print(f"\n{'=' * 70}")
    print(f"  Saved: {out_file}")
    print(f"{'=' * 70}")
    return all_results

if __name__ == '__main__':
    run()
