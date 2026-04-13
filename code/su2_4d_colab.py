"""
╔══════════════════════════════════════════════════════════════╗
║  4D SU(2) Hadamard Gauge-Geometry Coupling: Monte Carlo     ║
║  Numba JIT-optimized for Google Colab                       ║
║  T = C ⊙ S  — Universality Test                            ║
╚══════════════════════════════════════════════════════════════╝

사용법 (Google Colab):
  1. 새 노트북 생성
  2. 이 파일 전체를 하나의 셀에 붙여넣기
  3. 런타임 실행 (GPU 불필요, CPU 충분)
  
예상 시간:
  L=4: ~20분 | L=6: ~3시간 | L=8: ~12시간 (Colab Pro)
"""

import numpy as np
from numba import njit, prange
import time
import json

# ============================================================
# SU(2) quaternion arithmetic (all @njit)
# SU(2) element = (a0, a1, a2, a3), a0²+a1²+a2²+a3² = 1
# Corresponds to matrix: [[a0+ia3, a2+ia1],[-a2+ia1, a0-ia3]]
# Re(Tr(U))/2 = a0
# ============================================================

@njit(cache=True)
def su2_mul(a, b, out):
    """Multiply two SU(2) elements: out = a * b"""
    out[0] = a[0]*b[0] - a[1]*b[1] - a[2]*b[2] - a[3]*b[3]
    out[1] = a[0]*b[1] + a[1]*b[0] + a[2]*b[3] - a[3]*b[2]
    out[2] = a[0]*b[2] - a[1]*b[3] + a[2]*b[0] + a[3]*b[1]
    out[3] = a[0]*b[3] + a[1]*b[2] - a[2]*b[1] + a[3]*b[0]

@njit(cache=True)
def su2_mul_dag(a, b, out):
    """Multiply a * b^dagger: out = a * b†"""
    # b† = (b0, -b1, -b2, -b3)
    out[0] = a[0]*b[0] + a[1]*b[1] + a[2]*b[2] + a[3]*b[3]
    out[1] = -a[0]*b[1] + a[1]*b[0] - a[2]*b[3] + a[3]*b[2]
    out[2] = -a[0]*b[2] + a[1]*b[3] + a[2]*b[0] - a[3]*b[1]
    out[3] = -a[0]*b[3] - a[1]*b[2] + a[2]*b[1] + a[3]*b[0]

@njit(cache=True)
def su2_dag_mul(a, b, out):
    """Multiply a^dagger * b: out = a† * b"""
    # a† = (a0, -a1, -a2, -a3)
    out[0] = a[0]*b[0] + a[1]*b[1] + a[2]*b[2] + a[3]*b[3]
    out[1] = a[0]*b[1] - a[1]*b[0] + a[2]*b[3] - a[3]*b[2]
    out[2] = a[0]*b[2] - a[1]*b[3] - a[2]*b[0] + a[3]*b[1]
    out[3] = a[0]*b[3] + a[1]*b[2] - a[2]*b[1] - a[3]*b[0]

@njit(cache=True)
def su2_normalize(a):
    """Project back to SU(2) (fix numerical drift)."""
    norm = np.sqrt(a[0]**2 + a[1]**2 + a[2]**2 + a[3]**2)
    if norm > 0:
        a[0] /= norm; a[1] /= norm; a[2] /= norm; a[3] /= norm

@njit(cache=True)
def su2_random_near_identity(eps):
    """Generate SU(2) element near identity for Metropolis."""
    r = np.empty(4)
    r[0] = 1.0 + eps * np.random.randn() * 0.1
    r[1] = eps * np.random.randn()
    r[2] = eps * np.random.randn()
    r[3] = eps * np.random.randn()
    norm = np.sqrt(r[0]**2 + r[1]**2 + r[2]**2 + r[3]**2)
    r[0] /= norm; r[1] /= norm; r[2] /= norm; r[3] /= norm
    return r

# ============================================================
# 4D lattice indexing
# ============================================================

@njit(cache=True)
def idx4(x, y, z, t, L):
    """Convert 4D coordinates to flat index."""
    return ((x % L) * L * L * L + (y % L) * L * L + (z % L) * L + (t % L))

@njit(cache=True)
def coords4(i, L):
    """Convert flat index back to 4D coordinates."""
    t = i % L
    z = (i // L) % L
    y = (i // (L * L)) % L
    x = (i // (L * L * L)) % L
    return x, y, z, t

@njit(cache=True)
def neighbor_plus(x, y, z, t, mu, L):
    """Return coordinates shifted by +1 in direction mu."""
    if mu == 0: return (x+1)%L, y, z, t
    elif mu == 1: return x, (y+1)%L, z, t
    elif mu == 2: return x, y, (z+1)%L, t
    else: return x, y, z, (t+1)%L

@njit(cache=True)
def neighbor_minus(x, y, z, t, mu, L):
    """Return coordinates shifted by -1 in direction mu."""
    if mu == 0: return (x-1)%L, y, z, t
    elif mu == 1: return x, (y-1)%L, z, t
    elif mu == 2: return x, y, (z-1)%L, t
    else: return x, y, z, (t-1)%L

# ============================================================
# Plaquette computation
# ============================================================

@njit(cache=True)
def compute_plaquette(U, x, y, z, t, mu, nu, L):
    """
    Compute Re(Tr(U_P))/2 for plaquette in (mu,nu) plane at (x,y,z,t).
    P = U_mu(x) * U_nu(x+mu) * U_mu†(x+nu) * U_nu†(x)
    Returns a0 of the product quaternion.
    """
    s = idx4(x, y, z, t, L)
    
    xm, ym, zm, tm = neighbor_plus(x, y, z, t, mu, L)
    s_mu = idx4(xm, ym, zm, tm, L)
    
    xn, yn, zn, tn = neighbor_plus(x, y, z, t, nu, L)
    s_nu = idx4(xn, yn, zn, tn, L)
    
    tmp1 = np.empty(4)
    tmp2 = np.empty(4)
    tmp3 = np.empty(4)
    
    # tmp1 = U_mu(x) * U_nu(x+mu)
    su2_mul(U[s, mu], U[s_mu, nu], tmp1)
    # tmp2 = tmp1 * U_mu†(x+nu)
    su2_mul_dag(tmp1, U[s_nu, mu], tmp2)
    # tmp3 = tmp2 * U_nu†(x)
    su2_mul_dag(tmp2, U[s, nu], tmp3)
    
    return tmp3[0]  # Re(Tr)/2

@njit(cache=True)
def plaquette_weight(w, x, y, z, t, mu, nu, L):
    """Compute geometric weight of plaquette sqrt(w1*w2*w3*w4)."""
    s = idx4(x, y, z, t, L)
    xm, ym, zm, tm = neighbor_plus(x, y, z, t, mu, L)
    s_mu = idx4(xm, ym, zm, tm, L)
    xn, yn, zn, tn = neighbor_plus(x, y, z, t, nu, L)
    s_nu = idx4(xn, yn, zn, tn, L)
    
    return np.sqrt(w[s, mu] * w[s_mu, nu] * w[s_nu, mu] * w[s, nu])

# ============================================================
# Local action computation for a single link
# ============================================================

@njit(cache=True)
def local_gauge_action(U, w, x, y, z, t, mu, beta, L):
    """
    Compute gauge action contribution from all plaquettes containing link (x,y,z,t,mu).
    Each link in 4D participates in 6 plaquettes (3 planes × forward/backward).
    """
    s_total = 0.0
    for nu in range(4):
        if nu == mu:
            continue
        # Forward plaquette: at (x,y,z,t) in (mu,nu) plane
        cp = compute_plaquette(U, x, y, z, t, mu, nu, L)
        wp = plaquette_weight(w, x, y, z, t, mu, nu, L)
        s_total += -beta * wp * cp
        
        # Backward plaquette: at (x-e_nu) in (mu,nu) plane
        xb, yb, zb, tb = neighbor_minus(x, y, z, t, nu, L)
        cp2 = compute_plaquette(U, xb, yb, zb, tb, mu, nu, L)
        wp2 = plaquette_weight(w, xb, yb, zb, tb, mu, nu, L)
        s_total += -beta * wp2 * cp2
    
    return s_total

# ============================================================
# Full Metropolis sweep
# ============================================================

@njit(cache=True)
def sweep_gauge(U, w, beta, L, eps):
    """Metropolis sweep over all gauge links."""
    V = L**4
    n_accept = 0
    n_total = 0
    
    for i in range(V):
        x, y, z, t = coords4(i, L)
        for mu in range(4):
            s = idx4(x, y, z, t, L)
            old_U = U[s, mu].copy()
            
            s_before = local_gauge_action(U, w, x, y, z, t, mu, beta, L)
            
            # Propose: U_new = R * U_old
            R = su2_random_near_identity(eps)
            new_U = np.empty(4)
            su2_mul(R, old_U, new_U)
            U[s, mu, 0] = new_U[0]
            U[s, mu, 1] = new_U[1]
            U[s, mu, 2] = new_U[2]
            U[s, mu, 3] = new_U[3]
            
            s_after = local_gauge_action(U, w, x, y, z, t, mu, beta, L)
            
            dS = s_after - s_before
            n_total += 1
            if dS <= 0 or np.random.random() < np.exp(-dS):
                n_accept += 1
            else:
                U[s, mu, 0] = old_U[0]
                U[s, mu, 1] = old_U[1]
                U[s, mu, 2] = old_U[2]
                U[s, mu, 3] = old_U[3]
    
    return n_accept / n_total

@njit(cache=True)
def sweep_weights(U, w, beta, kappa, L, delta_w):
    """Metropolis sweep over all edge weights."""
    V = L**4
    n_accept = 0
    n_total = 0
    
    for i in range(V):
        x, y, z, t = coords4(i, L)
        for mu in range(4):
            s = idx4(x, y, z, t, L)
            old_w = w[s, mu]
            
            s_before = local_gauge_action(U, w, x, y, z, t, mu, beta, L) + kappa * (old_w - 1.0)**2
            
            new_w = old_w + delta_w * np.random.randn()
            if new_w < 0.1:
                new_w = 0.1
            w[s, mu] = new_w
            
            s_after = local_gauge_action(U, w, x, y, z, t, mu, beta, L) + kappa * (new_w - 1.0)**2
            
            dS = s_after - s_before
            n_total += 1
            if dS <= 0 or np.random.random() < np.exp(-dS):
                n_accept += 1
            else:
                w[s, mu] = old_w
    
    return n_accept / n_total

@njit(cache=True)
def full_sweep(U, w, beta, kappa, L, eps_gauge, delta_w):
    """One complete sweep: gauge + weights."""
    acc_g = sweep_gauge(U, w, beta, L, eps_gauge)
    acc_w = sweep_weights(U, w, beta, kappa, L, delta_w)
    return acc_g, acc_w

# ============================================================
# Measurement
# ============================================================

@njit(cache=True)
def measure_correlation(U, w, L):
    """
    Measure Pearson correlation between plaquette weight and Re(Tr(U_P))/2
    across all plaquettes.
    """
    V = L**4
    n_plaq = V * 6  # 6 plaquette orientations per site in 4D
    
    cos_vals = np.empty(n_plaq)
    wp_vals = np.empty(n_plaq)
    
    idx = 0
    for i in range(V):
        x, y, z, t = coords4(i, L)
        for mu in range(4):
            for nu in range(mu+1, 4):
                cos_vals[idx] = compute_plaquette(U, x, y, z, t, mu, nu, L)
                wp_vals[idx] = plaquette_weight(w, x, y, z, t, mu, nu, L)
                idx += 1
    
    # Pearson correlation
    mc = np.mean(cos_vals)
    mw = np.mean(wp_vals)
    sc = np.std(cos_vals)
    sw = np.std(wp_vals)
    
    if sc < 1e-15 or sw < 1e-15:
        return 0.0
    
    cov = np.mean((cos_vals - mc) * (wp_vals - mw))
    return cov / (sc * sw)

@njit(cache=True)
def measure_plaquette_avg(U, L):
    """Average plaquette value on fixed lattice."""
    V = L**4
    total = 0.0
    count = 0
    for i in range(V):
        x, y, z, t = coords4(i, L)
        for mu in range(4):
            for nu in range(mu+1, 4):
                total += compute_plaquette(U, x, y, z, t, mu, nu, L)
                count += 1
    return total / count

# ============================================================
# Initialization
# ============================================================

@njit(cache=True)
def init_random_su2(V, n_dir):
    """Initialize random SU(2) link variables."""
    U = np.empty((V, n_dir, 4))
    for i in range(V):
        for mu in range(n_dir):
            r = np.random.randn(4)
            norm = np.sqrt(r[0]**2 + r[1]**2 + r[2]**2 + r[3]**2)
            U[i, mu, 0] = r[0] / norm
            U[i, mu, 1] = r[1] / norm
            U[i, mu, 2] = r[2] / norm
            U[i, mu, 3] = r[3] / norm
    return U

# ============================================================
# MAIN SIMULATION
# ============================================================

def run_simulation(L=4, kappa=1.0, betas=None, 
                   N_therm=200, N_meas=300,
                   eps_gauge=0.5, delta_w=0.05):
    """
    Run complete 4D SU(2) simulation with linearized Regge dynamics.
    """
    if betas is None:
        betas = [0.5, 1.0, 1.5, 2.0, 3.0, 5.0]
    
    V = L**4
    n_dir = 4
    
    print(f"{'='*65}")
    print(f"  4D SU(2) + Linearized Regge Dynamics")
    print(f"  L={L}, V={V}, links={V*4}, plaquettes={V*6}")
    print(f"  κ={kappa}, {N_therm} therm + {N_meas} meas")
    print(f"{'='*65}")
    
    # JIT warm-up
    print("\n  JIT compiling (first run only)...", flush=True)
    t0 = time.time()
    np.random.seed(999)
    U_test = init_random_su2(16, 4)  # tiny 2^4 lattice
    w_test = np.ones((16, 4))
    full_sweep(U_test, w_test, 1.0, 1.0, 2, 0.5, 0.05)
    measure_correlation(U_test, w_test, 2)
    print(f"  JIT compile time: {time.time()-t0:.1f}s\n")
    
    # ---- Fixed lattice validation ----
    print("  VALIDATION: Fixed lattice <Re Tr U_P>/2")
    print(f"  {'β':>5}  {'MC':>8}  {'acc':>6}")
    for beta in [1.0, 2.0, 4.0]:
        np.random.seed(42 + int(beta*10))
        U_val = init_random_su2(V, n_dir)
        for _ in range(100):
            sweep_gauge(U_val, np.ones((V, n_dir)), beta, L, eps_gauge)
        vals = []
        for _ in range(200):
            acc = sweep_gauge(U_val, np.ones((V, n_dir)), beta, L, eps_gauge)
            vals.append(measure_plaquette_avg(U_val, L))
        print(f"  {beta:5.1f}  {np.mean(vals):8.4f}  {acc:6.2%}")
    
    # ---- Null test ----
    print("\n  NULL TEST: r on fixed lattice (should be ~0)")
    np.random.seed(777)
    U_null = init_random_su2(V, n_dir)
    w_null = np.ones((V, n_dir))
    # Add tiny random noise to weights (but don't update them)
    w_null += np.random.normal(0, 0.01, (V, n_dir))
    w_null = np.maximum(w_null, 0.1)
    for _ in range(100):
        sweep_gauge(U_null, w_null, 2.0, L, eps_gauge)
    null_corrs = []
    for _ in range(100):
        sweep_gauge(U_null, w_null, 2.0, L, eps_gauge)
        null_corrs.append(measure_correlation(U_null, w_null, L))
    r_null = np.mean(null_corrs)
    e_null = np.std(null_corrs) / np.sqrt(len(null_corrs))
    sig_null = abs(r_null) / e_null if e_null > 0 else 0
    print(f"  r(null) = {r_null:.4f} ± {e_null:.4f} ({sig_null:.1f}σ)")
    print(f"  → {'PASS' if sig_null < 3 else 'FAIL'}: {'consistent with 0' if sig_null < 3 else 'NOT consistent with 0'}")
    
    # ---- Main dynamical simulation ----
    print(f"\n  DYNAMICAL LATTICE: Hadamard coupling r(β)")
    print(f"  {'β':>5}  {'r(β)':>8}  {'±err':>8}  {'σ':>6}  {'acc_g':>6}  {'acc_w':>6}  {'time':>6}")
    
    results = []
    for beta in betas:
        np.random.seed(42 + int(beta * 100) + L * 7)
        t0 = time.time()
        
        U = init_random_su2(V, n_dir)
        w = np.ones((V, n_dir))
        
        # Thermalize
        for i in range(N_therm):
            full_sweep(U, w, beta, kappa, L, eps_gauge, delta_w)
            if (i+1) % 50 == 0:
                print(f"    β={beta:.1f} therm {i+1}/{N_therm}", flush=True)
        
        # Measure
        corrs = []
        acc_g_total = 0
        acc_w_total = 0
        for i in range(N_meas):
            acc_g, acc_w = full_sweep(U, w, beta, kappa, L, eps_gauge, delta_w)
            corrs.append(measure_correlation(U, w, L))
            acc_g_total += acc_g
            acc_w_total += acc_w
            if (i+1) % 100 == 0:
                print(f"    β={beta:.1f} meas {i+1}/{N_meas} r={np.mean(corrs):.4f}", flush=True)
        
        r_mean = np.mean(corrs)
        r_err = np.std(corrs) / np.sqrt(len(corrs))
        sig = abs(r_mean) / r_err if r_err > 0 else 0
        elapsed = time.time() - t0
        
        print(f"  {beta:5.1f}  {r_mean:8.4f}  {r_err:8.4f}  {sig:6.1f}  "
              f"{acc_g_total/N_meas:6.2%}  {acc_w_total/N_meas:6.2%}  {elapsed:5.0f}s")
        
        results.append({
            'beta': beta,
            'r': round(float(r_mean), 4),
            'err': round(float(r_err), 4),
            'sigma': round(float(sig), 1),
            'acc_gauge': round(float(acc_g_total/N_meas), 3),
            'acc_weight': round(float(acc_w_total/N_meas), 3),
            'time_sec': round(elapsed, 1),
            'w_mean': round(float(np.mean(w)), 4),
            'w_std': round(float(np.std(w)), 4)
        })
    
    # ---- Summary ----
    rs = [d['r'] for d in results]
    peak_idx = np.argmax(rs)
    
    print(f"\n{'='*65}")
    print(f"  SUMMARY: 4D SU(2), L={L}")
    print(f"{'='*65}")
    print(f"  Peak r = {results[peak_idx]['r']} at β = {results[peak_idx]['beta']}")
    print(f"  Non-monotonic: {'YES' if peak_idx not in [0, len(rs)-1] else 'PLATEAU/MONOTONIC'}")
    print(f"  All >3σ: {'YES' if all(d['sigma'] > 3 for d in results) else 'NO'}")
    print(f"  All >5σ: {'YES' if all(d['sigma'] > 5 for d in results) else 'NO'}")
    print(f"  Min significance: {min(d['sigma'] for d in results):.1f}σ")
    
    # Save
    output = {
        'config': '4D SU(2)',
        'L': L,
        'kappa': kappa,
        'N_therm': N_therm,
        'N_meas': N_meas,
        'null_test': {'r': round(float(r_null), 4), 'err': round(float(e_null), 4), 'sigma': round(float(sig_null), 1)},
        'results': results
    }
    
    fname = f'su2_4d_L{L}_results.json'
    with open(fname, 'w') as f:
        json.dump(output, f, indent=2)
    print(f"\n  Results saved to {fname}")
    
    return results

# ============================================================
# RUN
# ============================================================

if __name__ == '__main__':
    print("Starting 4D SU(2) Hadamard coupling simulation...")
    print("(Numba JIT will compile on first call — ~30s overhead)\n")
    
    # ---- Phase 1: L=4 (quick, ~20 min) ----
    results_L4 = run_simulation(
        L=4, kappa=1.0,
        betas=[0.5, 1.0, 1.5, 2.0, 3.0, 5.0],
        N_therm=200, N_meas=300,
        eps_gauge=0.5, delta_w=0.05
    )
    
    # ---- Phase 2: L=6 (longer, ~3 hours) ----
    # Uncomment to run:
    # results_L6 = run_simulation(
    #     L=6, kappa=1.0,
    #     betas=[0.5, 1.0, 1.5, 2.0, 3.0, 5.0],
    #     N_therm=200, N_meas=300,
    #     eps_gauge=0.5, delta_w=0.05
    # )
    
    # ---- Phase 3: L=8 (overnight, ~12 hours) ----
    # Uncomment to run (Colab Pro recommended):
    # results_L8 = run_simulation(
    #     L=8, kappa=1.0,
    #     betas=[0.5, 1.0, 1.5, 2.0, 3.0, 5.0],
    #     N_therm=200, N_meas=300,
    #     eps_gauge=0.5, delta_w=0.05
    # )
    
    print("\n\nDone. All results saved.")
