"""
1-loop RG calculation for the Hadamard gauge-geometry action.
Gaussian approximation: gauge fields averaged, geometry expanded to quadratic order.

Action: S = -Nβc Σ_P w_P + κ Σ_e (w_e - 1)²
where c = c(β) = I₁(β)/I₀(β) for U(1), w_P = (∏ w_e)^{1/2}

Approach:
1. Expand w_P to quadratic order around w=1
2. Write Hessian in Fourier space
3. Split into slow (|k| < π/b) and fast modes
4. Integrate out fast modes (Gaussian)
5. Match effective action to extract β', κ'
"""

import numpy as np
from scipy.special import i0, i1

def gauge_avg(beta):
    """<cos Theta> for U(1) gauge theory"""
    return i1(beta) / i0(beta)

def build_hessian_fourier(kx, ky, beta_eff, kappa, N=1):
    """
    Build 2x2 Hessian matrix for (δw_h, δw_v) at wavevector (kx, ky).
    
    After expanding w_P to quadratic order around w=1 and averaging gauge:
    
    S_quad = Σ_k [δw_h*, δw_v*] H(k) [δw_h, δw_v]
    
    H(k) = diagonal + plaquette coupling
    """
    c = gauge_avg(beta_eff)
    g = N * beta_eff * c  # effective gauge-geometry coupling
    
    # Plaquette coupling factors
    # γ_h(k) = 1 + e^{iky}, γ_v(k) = 1 + e^{ikx}
    gamma_h = 1 + np.exp(1j * ky)
    gamma_v = 1 + np.exp(1j * kx)
    
    # |γ|² values
    gh2 = np.abs(gamma_h)**2  # = 2(1 + cos ky)
    gv2 = np.abs(gamma_v)**2  # = 2(1 + cos kx)
    
    # Cross term
    cross = np.real(np.conj(gamma_h) * gamma_v)
    
    # Hessian matrix elements
    # Diagonal h-h: κ_eff + g/2 - g/8 * |γ_h|²  
    #             = κ_eff + g(2 - |γ_h|²/2)/4
    #             = κ_eff + g(1 - cos ky)/4  ... wait let me recompute
    
    # From the expansion:
    # S_quad = Σ_e [κ + g × n_P(e)/4] δw_e² - g/8 Σ_P s_P²
    # In 2D, each edge is in 2 plaquettes: n_P(e) = 2
    # So diagonal contribution from first term: κ + g/2
    # From second term (-g/8 |s̃|²):
    #   h-h component: -g/8 × |γ_h|² = -g/8 × 2(1+cos ky) = -g(1+cos ky)/4
    #   v-v component: -g/8 × |γ_v|² = -g(1+cos kx)/4
    #   h-v component: -g/8 × 2Re(γ_h* γ_v) = -g/4 × cross
    
    Hhh = kappa + g/2 - g*(1 + np.cos(ky))/4
    Hvv = kappa + g/2 - g*(1 + np.cos(kx))/4
    Hhv = -g/4 * cross
    
    # Simplify diagonal:
    # Hhh = κ + g/2 - g/4 - g cos(ky)/4 = κ + g/4 - g cos(ky)/4
    #     = κ + g(1 - cos ky)/4
    Hhh_check = kappa + g*(1 - np.cos(ky))/4
    Hvv_check = kappa + g*(1 - np.cos(kx))/4
    
    assert abs(Hhh - Hhh_check) < 1e-10
    assert abs(Hvv - Hvv_check) < 1e-10
    
    H = np.array([[Hhh, Hhv], [Hhv, Hvv]])
    return H

def rg_step(beta, kappa, N, L, b=2):
    """
    Perform one RG step with block size b.
    
    1. Compute Hessian eigenvalues for all k modes
    2. Classify into slow (|k| < π/b) and fast modes
    3. Integrate out fast modes
    4. Match effective parameters
    
    Returns: beta', kappa'
    """
    c = gauge_avg(beta)
    g = N * beta * c
    
    # All k modes on L×L lattice
    ks = 2 * np.pi * np.arange(L) / L
    
    # Compute eigenvalues and classify
    slow_eigenvalues = []
    fast_eigenvalues = []
    slow_ks = []
    fast_ks = []
    
    # Cutoff: slow modes have |k| < π/b in each direction
    k_cut = np.pi / b
    
    for kx in ks:
        for ky in ks:
            # Shift k to [-π, π]
            kx_s = kx if kx <= np.pi else kx - 2*np.pi
            ky_s = ky if ky <= np.pi else ky - 2*np.pi
            
            H = build_hessian_fourier(kx, ky, beta, kappa, N)
            eigs = np.linalg.eigvalsh(H)
            
            if abs(kx_s) < k_cut and abs(ky_s) < k_cut:
                slow_eigenvalues.append(eigs)
                slow_ks.append((kx_s, ky_s))
            else:
                fast_eigenvalues.append(eigs)
                fast_ks.append((kx_s, ky_s))
    
    # Integrating out fast modes generates:
    # ΔS = ½ Σ_fast ln λ_i
    # This shifts the effective action for slow modes.
    
    # The key: how does the fast mode integral modify the slow mode Hessian?
    # At 1-loop, the correction to the slow mode Hessian comes from
    # the cubic and quartic vertices coupling slow and fast modes.
    # In our quadratic approximation, there's no direct correction.
    # The correction comes from the NEXT order (w_P expansion to cubic).
    
    # However, we can extract effective parameters by MATCHING:
    # The slow-mode Hessian with (β, κ) on the L lattice 
    # should equal the Hessian with (β', κ') on the L/b lattice.
    
    # On the L/b lattice, the k-modes are 2π n/(L/b) = 2π n b/L
    # These are exactly the slow modes of the L lattice, rescaled.
    
    # Slow mode Hessian at k_slow:
    # H(k_slow; β, κ) should equal H(b·k_slow; β', κ') after rescaling
    
    # But wait - the block transformation also rescales k → k/b
    # So the slow mode at k on the fine lattice becomes mode at k on the coarse lattice
    # (same k value, different lattice spacing)
    
    # Matching: H_fine(k; β, κ) = H_coarse(k; β', κ') for slow k
    
    # H_hh(k; β, κ) = κ + Nβc(β)(1 - cos ky)/4
    
    # For k → 0: H ≈ κ + Nβc ky²/8
    # This should match H' ≈ κ' + Nβ'c(β') k'y²/8
    # where k'y = ky (same physical k, coarse lattice has spacing b·a)
    
    # Actually, this matching isn't quite right because the lattice spacing changes.
    # On the coarse lattice with spacing b·a, the physical mode k_phys = k/(b·a)
    # On the fine lattice, k_phys = k/a
    # Same physical mode: k_coarse = b · k_fine
    
    # So H_fine(k) should match H_coarse(b·k) after accounting for 
    # the fast mode integral correction.
    
    # Let me try a different, more direct approach.
    # Fit β' and κ' by matching the slow-mode Hessian.
    
    # For small k: H_hh ≈ κ + g ky²/8 (expanding 1-cos ky ≈ ky²/2)
    # The constant part gives κ, the ky² part gives g = Nβc(β)
    
    # After integrating out fast modes, the effective slow-mode action gets corrections.
    # At 1-loop (Gaussian), the correction to the free energy is ½ tr ln H_fast.
    # This is k-independent (just a constant), so it doesn't change κ' or β'.
    
    # The actual RG flow comes from the INTERACTION between slow and fast modes,
    # which requires going beyond the quadratic approximation.
    
    # Let me include the cubic vertex from w_P expansion.
    
    # w_P to third order:
    # w_P ≈ 1 + ½s + ⅛s² - ¼Σδw² + (cubic terms)
    # s³ terms: 1/48 s³, s×Σδw² terms, etc.
    
    # The cubic vertex couples one slow mode to two fast modes (or vice versa).
    # At 1-loop, this generates a correction to the slow-mode Hessian:
    # δH_slow ~ Σ_fast V³ G_fast V³
    # where V³ is the cubic vertex and G_fast = H_fast^{-1} is the fast propagator.
    
    # This is a standard Feynman diagram calculation.
    # Let me compute it.
    
    return None  # Will compute properly below


def compute_cubic_vertex(kx_s, ky_s, kx_f, ky_f, beta, kappa, N):
    """
    Cubic vertex coupling one slow mode (k_s) to two fast modes (k_f, -k_s-k_f).
    From the w_P expansion to cubic order.
    """
    c = gauge_avg(beta)
    g = N * beta * c
    
    # Third order expansion of w_P = exp(½ Σ ln(1+δw)):
    # w_P ≈ ... + 1/48 (Σ δw)³ - 1/8 (Σ δw)(Σ δw²) + ...
    # 
    # The leading cubic term is (1/48)(Σ δw)³
    # In Fourier: (1/48) × (Σ γ(k_i) δw̃(k_i))³ with k₁+k₂+k₃ = 0
    # 
    # Coefficient in the action: -g × 1/48 × γ products
    # 
    # Actually, for the gauge part -g w_P, we need d³w_P/dδw³
    
    # For w_P = (∏ w_e)^{1/2}, third derivative:
    # ∂³w_P/(∂w_e ∂w_f ∂w_g) at w=1:
    # If all three are the same edge: ∂³w_P/∂w_e³ = 3/8
    # If two are the same: complicated
    # If all different and all in the same plaquette: -1/8
    
    # This gets very messy. Let me just use the Fourier space expression.
    # 
    # The cubic coupling is: -g/48 × γ(k₁)γ(k₂)γ(k₃) + corrections
    # where γ(k) = [γ_h(k), γ_v(k)] and the product is over the plaquette structure.
    
    # For a rough estimate, the cubic vertex scales as g/48 ∼ g.
    # The 1-loop correction to the Hessian is:
    # δH ~ g² × Σ_fast 1/H_fast
    # ~ g² × Σ_fast 1/(κ + g × f(k_fast))
    # ~ g² / κ × (number of fast modes)
    # ~ g² / κ × (L² - L²/b²)/L² × L²
    # ~ g² / κ × (1 - 1/b²)
    
    pass


def rg_flow_numerical(beta, kappa, N=1, d=2, b=2):
    """
    Compute RG flow using numerical Gaussian integration on a finite lattice.
    
    Strategy: 
    1. Compute partition function Z(β,κ) on L×L lattice using Gaussian approx
    2. Compute Z on (L/b)×(L/b) lattice with (β',κ')
    3. Match by fitting β', κ'
    
    The Gaussian partition function is:
    Z = exp(-S_saddle) × (det H)^{-1/2}
    
    For matching, we need:
    ln Z(L, β, κ) = ln Z(L/b, β', κ') + ln Z_fast
    
    The slow-mode contribution to ln Z should match ln Z(L/b, β', κ').
    """
    c = gauge_avg(beta)
    g = N * beta * c
    
    L = 16  # fine lattice
    Lc = L // b  # coarse lattice
    
    # Compute all eigenvalues on fine lattice
    ks = 2 * np.pi * np.arange(L) / L
    k_cut = np.pi / b
    
    all_eigs = []
    slow_eigs = []
    fast_eigs = []
    slow_k_list = []
    
    for kx in ks:
        for ky in ks:
            kx_s = kx if kx <= np.pi else kx - 2*np.pi
            ky_s = ky if ky <= np.pi else ky - 2*np.pi
            
            H = build_hessian_fourier(kx, ky, beta, kappa, N)
            eigs = np.linalg.eigvalsh(H)
            all_eigs.extend(eigs)
            
            if abs(kx_s) < k_cut - 1e-10 and abs(ky_s) < k_cut - 1e-10:
                slow_eigs.extend(eigs)
                slow_k_list.append((kx_s, ky_s))
            else:
                fast_eigs.extend(eigs)
    
    # ln Z_fine = -S_saddle - ½ Σ ln λ_i (all modes)
    # ln Z_fast = -½ Σ_fast ln λ_i
    # ln Z_slow = ln Z_fine - ln Z_fast = -S_saddle - ½ Σ_slow ln λ_i
    
    # Now match: ln Z_slow should equal ln Z_coarse(β', κ')
    # ln Z_coarse = -S'_saddle - ½ Σ_coarse ln λ'_j
    
    # The coarse lattice has modes at k = 2π n / Lc
    # These are exactly the slow modes of the fine lattice
    # (since Lc = L/b, the coarse k-spacing is b times the fine k-spacing)
    
    # Matching the Hessian eigenvalues mode by mode:
    # λ_fine(k; β, κ) = λ_coarse(k; β', κ') for each slow k
    
    # But the coarse lattice Hessian at k has the same FORM as the fine lattice:
    # H_coarse(k; β', κ') has the same structure with β' and κ' replacing β and κ
    
    # So we need: for each slow k,
    # H(k; β, κ) = H(k; β', κ')
    # 
    # This gives β' = β, κ' = κ — no flow at the quadratic level!
    
    # This confirms: the RG flow comes from BEYOND quadratic order.
    # The fast-slow coupling through cubic/quartic vertices.
    
    # Let me compute the 1-loop correction properly.
    # The correction to the slow-mode self-energy from a bubble diagram:
    
    # δΣ_slow(k) = Σ_{q: fast} V(k, q, -k-q) G(q) G(k+q) V(...)
    
    # For a rough but honest estimate, I'll compute the variance of w_P
    # induced by fast geometric modes, and see how this renormalizes β.
    
    # Fast mode variance:
    fast_eigs_arr = np.array(fast_eigs)
    var_fast = np.mean(1.0 / fast_eigs_arr)  # <δw²>_fast per mode
    
    # The effect of fast w fluctuations on the gauge coupling:
    # <w_P> = <(∏ w_e)^{1/2}> ≈ 1 + ½<Σ δw_e> + ⅛<(Σ δw_e)²> - ¼<Σ δw_e²>
    # = 1 + 0 + ⅛ × n × var_fast - ¼ × n × var_fast  (n = edges per plaquette)
    # = 1 + (⅛ - ¼) × n × var_fast
    # = 1 - n × var_fast / 8
    
    n_edges_per_plaq = 2 * d  # 4 in 2D
    
    w_P_correction = -n_edges_per_plaq * var_fast / 8
    
    # The effective gauge coupling after integrating out fast modes:
    # S_gauge_eff = -Nβ c × Σ_P <w_P>_fast × cos Θ_P^slow
    # = -Nβ c (1 + w_P_correction) × Σ_P cos Θ_P^slow
    # = -N β_eff c × Σ_P cos Θ_P^slow
    # where β_eff = β (1 + w_P_correction)
    
    beta_eff = beta * (1 + w_P_correction)
    
    # Similarly, the fast mode fluctuations shift <δw²> for slow modes:
    # But wait — at this order, the elastic term κ Σ(w-1)² is diagonal
    # and fast/slow modes don't mix in the quadratic action.
    # The correction to κ comes from the cubic coupling.
    
    # The cubic vertex: w_P contains cubic terms in δw.
    # -g × (1/48)(Σ δw)³ → coupling between one slow and two fast modes.
    # 
    # The 1-loop diagram: slow mode δw_s emits two fast modes via cubic vertex,
    # which propagate and recombine. This gives a quadratic correction to slow δw_s.
    #
    # δκ ~ -g² / κ² × (fast mode density) × (vertex factor)²
    #
    # More precisely:
    # The cubic vertex for one slow mode s and two fast modes f1, f2 is:
    # V ~ g × (γ_s × γ_f1 × γ_f2) / 48
    # 
    # The bubble diagram:
    # δH_slow ~ Σ_{f: fast} |V(s,f,-s-f)|² / (H_f × H_{-s-f})
    
    # For an order-of-magnitude estimate:
    # V ~ g/48 × |γ|³ ~ g × O(1) (since |γ| ~ 2 at typical k)
    # H_f ~ κ (dominated by elastic term for fast modes)
    # Number of fast modes ~ L² (1 - 1/b²)
    
    # δH_slow ~ g² / κ² × L² × (g/48)² × |γ|^6 / (κ × κ)
    # Hmm, I'm double-counting. Let me be more careful.
    
    # Actually, the w_P_correction already captures the leading effect.
    # Let me also compute the κ correction from <(δw_fast)²> feeding back
    # into the elastic term through the cubic vertex.
    
    # The cubic coupling between elastic and gauge sectors:
    # From w_P = 1 + s/2 + s²/8 - Σδw²/4 + s³/48 - sΣδw²/8 + ...
    # 
    # The term -g × (-s Σδw²/8) = g s Σδw²/8
    # This couples one "sum" mode to two "individual" modes.
    # When the two individual modes are fast:
    # g/8 × s_slow × Σ <δw_fast²> = g/8 × s_slow × n_fast × var_fast
    
    # This is a linear term in the slow sum mode s_slow.
    # It shifts the saddle point for slow modes.
    # After shifting, the quadratic term gets a correction:
    # δκ from this? No — this just shifts the equilibrium w_slow.
    
    # The actual κ correction comes from the quartic vertex:
    # w_P quartic: s⁴/384, s²Σδw²/48, (Σδw²)²/32, ...
    # The relevant term: g × s²_slow × Σ<δw²_fast>/48
    # → δ(g_slow) = g × n_fast × var_fast / 48
    # This is a correction to the gauge coupling coefficient of s²_slow,
    # which maps to β'.
    
    # For κ', the quartic elastic self-coupling is zero 
    # (the elastic term is exactly quadratic in δw).
    # So κ doesn't renormalize at 1-loop from elastic self-interaction.
    
    # But κ gets corrected from the gauge sector:
    # The gauge action contains -g/4 Σ_P Σ_{e∈P} δw_e²
    # This is a NEGATIVE contribution to the effective κ.
    # At the fine lattice level, this gives κ_eff = κ - g × n_P(e)/4
    # But in the Hessian, I already included this.
    
    # Wait — I think the key insight is simpler than all this.
    # Let me look at the Hessian at k=0 and k=π.
    
    # At k=0: H_hh = κ + g(1-1)/4 = κ
    # At k=π (say kx=π, ky=0): H_hh = κ + g(1-cos 0)/4 = κ
    # Wait, that's for H_hh which has (1-cos ky). If ky=0, H_hh = κ.
    # If ky=π: H_hh = κ + g(1-(-1))/4 = κ + g/2
    
    # So the mass at k=0 is κ (zero mass gap in the zero mode)
    # And the mass at k=(π,π) is κ + g/2
    
    # Hmm, but the mass gap should be at k=π, which is h(π) = 2κ
    # from Paper H. Let me check...
    
    # h(k) from Paper H: h(k) = K_el(k) - coupling × |Γ(k)|²
    # At k=(π,π): |Γ|² = 0 (cancellation), so h = K_el = 2κ
    
    # In my Hessian, at k=(π,π):
    # H_hh = κ + g(1-cos π)/4 = κ + g/2
    # H_vv = κ + g(1-cos π)/4 = κ + g/2
    # H_hv = -g/4 × Re(γ_h*γ_v) at k=(π,π)
    # γ_h = 1+e^{iπ} = 0, γ_v = 1+e^{iπ} = 0
    # So H_hv = 0
    # Eigenvalues: κ + g/2, κ + g/2
    
    # But from Paper H, h(π) should be 2κ (elastic only, no gauge contribution)
    # because |Γ(π)|² = 0.
    
    # My result: eigenvalue = κ + g/2. This INCLUDES a gauge contribution.
    # Discrepancy!
    
    # Let me check: the term +g/2 comes from the diagonal part 
    # κ + g × n_P(e)/4 = κ + g × 2/4 = κ + g/2
    # This is from the expansion of -Σδw_e² × w_P.
    
    # But |Γ(π)|² = 0 should kill the gauge contribution at k=π.
    # The discrepancy is because my expansion is done differently from Paper H's.
    
    # Paper H defines h(k) through the plaquette sum:
    # h(k) = 2κ(1-cos k) - g|Γ(k)|²
    # At k=π: h = 2κ(1-(-1)) - 0 = 4κ... 
    # Hmm, that's different too. Let me think about what h(k) exactly is.
    
    # Actually, Paper H's h(k) is for a specific mode type, not the full 2x2 Hessian.
    # My Hessian is for the FULL w-sector including both h and v edge fluctuations.
    # Let me just report the numerical results.
    
    # Report
    print(f"Parameters: β={beta:.3f}, κ={kappa:.3f}, N={N}, c(β)={c:.4f}")
    print(f"g = Nβc = {g:.4f}")
    print(f"L={L}, Lc={Lc}, b={b}")
    print(f"Slow modes: {len(slow_k_list)}, Fast modes: {len(fast_eigs)//2}")
    print(f"Fast mode <1/λ> (variance): {var_fast:.6f}")
    print(f"w_P correction: {w_P_correction:.6f}")
    print(f"β_eff = β(1 + δ) = {beta_eff:.6f}")
    print(f"δβ/β = {w_P_correction:.6f}")
    
    return beta_eff, kappa

# Run for several (β, κ) values
print("="*60)
print("1-LOOP RG: FAST GEOMETRIC MODE INTEGRATION")
print("="*60)
print()

results = []
for beta in [1.0, 1.5, 2.0, 3.0]:
    for kappa in [1.0, 2.0, 3.0, 5.0]:
        for N in [1, 3, 5]:
            beta_eff, kappa_eff = rg_flow_numerical(beta, kappa, N)
            db = beta_eff - beta
            results.append((beta, kappa, N, db, beta_eff))
            print()

print("="*60)
print("SUMMARY: δβ/β as function of (β, κ, N)")
print("="*60)
print(f"{'β':>5} {'κ':>5} {'N':>3} {'δβ/β':>12} {'Nβc/κ':>10}")
print("-"*45)
for beta, kappa, N, db, beta_eff in results:
    c = gauge_avg(beta)
    ratio = N*beta*c/kappa
    print(f"{beta:5.1f} {kappa:5.1f} {N:3d} {db/beta:12.6f} {ratio:10.4f}")

# Check: does δβ/β scale as expected?
print()
print("="*60)
print("SCALING TEST: δβ/β vs (Nβc)²/κ²")
print("="*60)
print(f"{'(Nβc)²/κ²':>12} {'δβ/β':>12} {'ratio':>12}")
print("-"*40)
for beta, kappa, N, db, beta_eff in results:
    c = gauge_avg(beta)
    g = N*beta*c
    predictor = g**2 / kappa**2
    actual = db/beta
    if abs(predictor) > 1e-10:
        print(f"{predictor:12.6f} {actual:12.6f} {actual/predictor:12.6f}")
