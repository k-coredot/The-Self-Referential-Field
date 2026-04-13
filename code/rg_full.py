"""
Full 1-loop RG: geometry AND gauge sectors simultaneously.

Key insight from analysis: at quadratic order, w and θ sectors decouple.
The coupling appears at CUBIC order: V = -Nβ/4 × s_P × Θ_P²

Three contributions to β flow:
1. Quadratic (geometry): δβ_quad < 0 (AM-GM suppression of <w_P>)
2. Cubic bubble (θ→w): fast θ fluctuations stiffen geometry (δκ > 0)
3. Cubic bubble (w→θ): fast w fluctuations enhance gauge coupling (δβ_cubic > 0)

The NET flow = sum of all three.
"""

import numpy as np
from scipy.special import i0, i1

def gauge_avg(beta):
    return i1(beta) / i0(beta)

def compute_full_rg(beta, kappa, N, L=16, b=2, d=2):
    c = gauge_avg(beta)
    g = N * beta * c
    
    ks = 2*np.pi*np.arange(L)/L
    k_cut = np.pi/b
    
    # Storage
    H_w_fast_inv = []     # 1/eigenvalue for fast w modes
    H_theta_fast_inv = [] # 1/eigenvalue for fast θ modes
    H_w_fast_eigs = []
    H_theta_fast_eigs = []
    n_slow = 0
    n_fast = 0
    
    for kx in ks:
        for ky in ks:
            kx_s = kx if kx <= np.pi else kx - 2*np.pi
            ky_s = ky if ky <= np.pi else ky - 2*np.pi
            
            # === Geometry Hessian (from previous calculation) ===
            Hw_hh = kappa + g*(1 - np.cos(ky))/4
            Hw_vv = kappa + g*(1 - np.cos(kx))/4
            gamma_h = 1 + np.exp(1j*ky)
            gamma_v = 1 + np.exp(1j*kx)
            cross_w = np.real(np.conj(gamma_h)*gamma_v)
            Hw_hv = -g/4 * cross_w
            
            Hw = np.array([[Hw_hh, Hw_hv],[Hw_hv, Hw_vv]])
            eigs_w = np.linalg.eigvalsh(Hw)
            
            # === Gauge Hessian ===
            # Θ_P = δθ_h(1-e^{iky}) + δθ_v(e^{ikx}-1)
            # H_θ = Nβ × [|μ_h|²     Re(μ_h*μ_v)]
            #             [Re(μ_h*μ_v)     |μ_v|²]
            mu_h = 1 - np.exp(1j*ky)
            mu_v = np.exp(1j*kx) - 1
            mh2 = np.abs(mu_h)**2  # 2(1-cos ky)
            mv2 = np.abs(mu_v)**2  # 2(1-cos kx)
            cross_theta = np.real(np.conj(mu_h)*mu_v)
            
            Ht = N*beta * np.array([[mh2, cross_theta],[cross_theta, mv2]])
            eigs_t = np.linalg.eigvalsh(Ht)
            
            is_slow = abs(kx_s) < k_cut - 1e-10 and abs(ky_s) < k_cut - 1e-10
            
            if is_slow:
                n_slow += 1
            else:
                n_fast += 1
                H_w_fast_eigs.extend(eigs_w)
                H_theta_fast_eigs.extend(eigs_t)
                # Store inverse eigenvalues (propagators)
                for e in eigs_w:
                    if e > 1e-10:
                        H_w_fast_inv.append(1.0/e)
                    else:
                        H_w_fast_inv.append(0)  # skip pathological
                for e in eigs_t:
                    if e > 1e-10:
                        H_theta_fast_inv.append(1.0/e)
                    else:
                        H_theta_fast_inv.append(0)
    
    H_w_fast_inv = np.array(H_w_fast_inv)
    H_theta_fast_inv = np.array(H_theta_fast_inv)
    H_w_fast_eigs = np.array(H_w_fast_eigs)
    H_theta_fast_eigs = np.array(H_theta_fast_eigs)
    
    # Check for stability
    n_neg_w = np.sum(H_w_fast_eigs < 0)
    n_neg_t = np.sum(H_theta_fast_eigs < 0)
    n_zero_t = np.sum(np.abs(H_theta_fast_eigs) < 1e-10)
    
    if n_neg_w > 0 or n_neg_t > 0:
        return None  # Gaussian approximation breaks down
    
    # ============================================
    # CONTRIBUTION 1: Quadratic geometry (δβ_quad)
    # From <w_P> = 1 - n × <δw²>_fast / 8
    # ============================================
    var_w_fast = np.mean(H_w_fast_inv[H_w_fast_inv > 0])  # <δw²> per fast mode
    n_edges_per_plaq = 2*d
    w_P_correction = -n_edges_per_plaq * var_w_fast / 8
    delta_beta_quad = beta * w_P_correction
    
    # ============================================
    # CONTRIBUTION 2: Cubic vertex w→θ (δβ_cubic)
    # Vertex: V = -Nβ/4 × s_P × Θ_P²
    # Fast w bubble corrects slow θ Hessian
    # δΣ_θ = V² × Σ_fast G_w(q) G_θ(k-q)
    # For rough estimate: δΣ_θ ~ (Nβ/4)² × <G_w> × <G_θ>_fast × n_fast
    # This INCREASES effective Nβ (positive correction)
    # ============================================
    
    # The bubble: one w propagator, one θ propagator
    # <G_w>_fast = mean of 1/λ_w over fast modes
    # <G_θ>_fast = mean of 1/λ_θ over fast non-zero modes
    
    valid_w = H_w_fast_inv[H_w_fast_inv > 0]
    valid_t = H_theta_fast_inv[H_theta_fast_inv > 0]
    
    if len(valid_w) == 0 or len(valid_t) == 0:
        return None
    
    avg_Gw = np.mean(valid_w)
    avg_Gt = np.mean(valid_t)
    
    # Vertex factor: (Nβ/4)² with plaquette structure factors
    # Average |γ|² ~ 2, |μ|² ~ 2 for typical fast modes
    V2 = (N*beta/4)**2
    
    # Number of fast modes contributing
    n_fast_modes = len(valid_t)
    
    # The bubble sum (per slow mode):
    # δΣ_θ = V² × (1/L²) × Σ_q G_w(q) G_θ(k-q)
    # ≈ V² × n_fast_modes/L² × avg_Gw × avg_Gt × (structure factor avg)
    # Structure factor average for fast modes: ~ O(1)
    
    bubble_wt = V2 * avg_Gw * avg_Gt * (n_fast_modes / L**2)
    
    # This corrects the θ Hessian: H_θ' = H_θ + δΣ_θ
    # H_θ ~ Nβ × 2(1-cos k), so δ(Nβ)/Nβ ~ δΣ_θ / H_θ_typical
    H_theta_typical = N*beta * 2  # typical value at k ~ π/2
    delta_Nbeta_cubic = bubble_wt  # absolute correction to Nβ coefficient
    delta_beta_cubic = delta_Nbeta_cubic / N  # correction to β
    
    # ============================================  
    # CONTRIBUTION 3: Cubic vertex θ→w (δκ_cubic)
    # Fast θ bubble corrects slow w Hessian
    # Same vertex, reverse direction
    # δΣ_w = V² × Σ_fast G_θ(q) G_w(k-q)
    # ≈ same magnitude as contribution 2
    # This INCREASES effective κ (positive correction)
    # ============================================
    
    bubble_tw = V2 * avg_Gt * avg_Gw * (n_fast_modes / L**2)
    delta_kappa_cubic = bubble_tw
    
    # ============================================
    # TOTAL
    # ============================================
    delta_beta_total = delta_beta_quad + delta_beta_cubic
    delta_kappa_total = delta_kappa_cubic  # quadratic level: no κ correction
    
    return {
        'beta': beta, 'kappa': kappa, 'N': N,
        'c': c, 'g': g,
        'n_slow': n_slow, 'n_fast': n_fast,
        'delta_beta_quad': delta_beta_quad,
        'delta_beta_cubic': delta_beta_cubic,
        'delta_beta_total': delta_beta_total,
        'delta_kappa_cubic': delta_kappa_cubic,
        'var_w_fast': var_w_fast,
        'avg_Gw': avg_Gw, 'avg_Gt': avg_Gt,
        'n_neg_w': n_neg_w, 'n_neg_t': n_neg_t,
    }


# Run systematic scan
print("="*70)
print("FULL 1-LOOP RG: GEOMETRY + GAUGE SECTORS")
print("="*70)
print()
print(f"{'β':>5} {'κ':>5} {'N':>3} {'δβ_quad':>10} {'δβ_cubic':>10} {'δβ_total':>10} {'δκ_cubic':>10} {'sign':>6}")
print("-"*70)

for kappa in [2.0, 3.0, 5.0, 10.0]:
    for beta in [0.5, 1.0, 1.5, 2.0, 3.0]:
        for N in [1, 3, 5]:
            r = compute_full_rg(beta, kappa, N)
            if r is None:
                print(f"{beta:5.1f} {kappa:5.1f} {N:3d} {'UNSTABLE':>10}")
                continue
            
            sign = "+" if r['delta_beta_total'] > 0 else "-"
            print(f"{beta:5.1f} {kappa:5.1f} {N:3d} "
                  f"{r['delta_beta_quad']:10.4f} "
                  f"{r['delta_beta_cubic']:10.4f} "
                  f"{r['delta_beta_total']:10.4f} "
                  f"{r['delta_kappa_cubic']:10.4f} "
                  f"{sign:>6}")

print()
print("="*70)
print("KEY QUESTION: Does δβ_total change sign depending on N?")
print("="*70)
print()

# Focus on β=2, κ=3 (our standard parameters)
print("β=2.0, κ=3.0:")
print(f"{'N':>3} {'δβ_quad':>12} {'δβ_cubic':>12} {'δβ_total':>12} {'δκ':>12} {'β_eff':>12} {'κ_eff':>12}")
for N in [1, 2, 3, 5, 8, 10, 12]:
    r = compute_full_rg(2.0, 3.0, N)
    if r:
        print(f"{N:3d} {r['delta_beta_quad']:12.6f} {r['delta_beta_cubic']:12.6f} "
              f"{r['delta_beta_total']:12.6f} {r['delta_kappa_cubic']:12.6f} "
              f"{2.0+r['delta_beta_total']:12.6f} {3.0+r['delta_kappa_cubic']:12.6f}")

print()
print("="*70)
print("RATIO TEST: δβ_cubic/δβ_quad as function of N")
print("(if cubic overwhelms quad at large N, net sign flips)")
print("="*70)
for N in [1, 2, 3, 5, 8, 10, 12]:
    r = compute_full_rg(2.0, 3.0, N)
    if r and abs(r['delta_beta_quad']) > 1e-10:
        ratio = r['delta_beta_cubic'] / abs(r['delta_beta_quad'])
        print(f"N={N:2d}: cubic/|quad| = {ratio:.4f}, "
              f"quad={r['delta_beta_quad']:.6f}, cubic={r['delta_beta_cubic']:.6f}")
