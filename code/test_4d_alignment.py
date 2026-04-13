"""
4D U(1) force alignment test - minimal implementation
Tests whether force alignment >90% survives in 4D
"""
import numpy as np
import time

L = 3  # 3^4 = 81 sites, manageable
D = 4
V = L**D
n_links = D * V  # 4 * 81 = 324 links

def idx(coords, L):
    x,y,z,t = [c%L for c in coords]
    return x*L**3 + y*L**2 + z*L + t

def coords(i, L):
    t = i % L; z = (i//L) % L; y = (i//L**2) % L; x = (i//L**3) % L
    return [x,y,z,t]

# Plaquette: for each site and each pair of directions (mu, nu) with mu < nu
# there are 6 plaquettes per site in 4D
def get_plaquettes(L, D):
    """Return list of (site, mu, nu, [4 link indices])"""
    plaqs = []
    for i in range(L**D):
        c = coords(i, L)
        for mu in range(D):
            for nu in range(mu+1, D):
                # Forward plaquette: link(i,mu), link(i+mu,nu), link(i+nu,mu)^-1, link(i,nu)^-1
                c_mu = list(c); c_mu[mu] = (c_mu[mu]+1)%L
                c_nu = list(c); c_nu[nu] = (c_nu[nu]+1)%L
                l1 = i*D + mu                      # link (i, mu), forward
                l2 = idx(c_mu, L)*D + nu            # link (i+mu_hat, nu), forward  
                l3 = idx(c_nu, L)*D + mu            # link (i+nu_hat, mu), backward
                l4 = i*D + nu                      # link (i, nu), backward
                plaqs.append((i, mu, nu, l1, l2, l3, l4))
    return plaqs

plaqs = get_plaquettes(L, D)
n_plaqs = len(plaqs)
print(f"4D lattice: L={L}, V={V}, links={n_links}, plaquettes={n_plaqs}")

# Build link-to-plaquette map
link_plaqs = [[] for _ in range(n_links)]
for pi, (site, mu, nu, l1, l2, l3, l4) in enumerate(plaqs):
    for ll in [l1, l2, l3, l4]:
        link_plaqs[ll].append(pi)

def plaq_angle(theta, p):
    _, _, _, l1, l2, l3, l4 = p
    return theta[l1] + theta[l2] - theta[l3] - theta[l4]

def plaq_weight(w, p):
    _, _, _, l1, l2, l3, l4 = p
    return np.sqrt(abs(w[l1]*w[l2]*w[l3]*w[l4]))

def sweep_gauge(theta, w, beta, L, D):
    for e in range(n_links):
        old = theta[e]
        theta[e] += np.random.uniform(-2, 2)
        dS = 0
        for pi in link_plaqs[e]:
            p = plaqs[pi]
            wp = plaq_weight(w, p)
            dS += -beta * wp * (np.cos(plaq_angle(theta, p)) - np.cos(plaq_angle(theta[:], p)))
        # Recompute properly
        theta[e] = old
        old_E = sum(-beta * plaq_weight(w, plaqs[pi]) * np.cos(plaq_angle(theta, plaqs[pi])) for pi in link_plaqs[e])
        theta[e] += np.random.uniform(-2, 2)
        new_E = sum(-beta * plaq_weight(w, plaqs[pi]) * np.cos(plaq_angle(theta, plaqs[pi])) for pi in link_plaqs[e])
        dS = new_E - old_E
        if dS > 0 and np.random.random() > np.exp(-dS):
            theta[e] = old

def sweep_geo(fields, w, beta, kappa, L, D):
    for e in range(n_links):
        old_w = w[e]
        # Compute old energy contributions
        old_E = sum(
            sum(-beta * plaq_weight(w, plaqs[pi]) * np.cos(plaq_angle(f, plaqs[pi])) for pi in link_plaqs[e])
            for f in fields
        ) + kappa * (old_w - 1)**2
        
        w[e] = max(0.1, old_w + np.random.normal(0, 0.05))
        
        new_E = sum(
            sum(-beta * plaq_weight(w, plaqs[pi]) * np.cos(plaq_angle(f, plaqs[pi])) for pi in link_plaqs[e])
            for f in fields
        ) + kappa * (w[e] - 1)**2
        
        if new_E - old_E > 0 and np.random.random() > np.exp(-(new_E - old_E)):
            w[e] = old_w

def gauge_force(field, w, beta, L, D, dl=1e-4):
    """Gauge-only force per edge"""
    force = np.zeros(n_links)
    for e in range(n_links):
        old_w = w[e]
        w[e] = old_w + dl
        Ep = sum(-beta * plaq_weight(w, plaqs[pi]) * np.cos(plaq_angle(field, plaqs[pi])) for pi in link_plaqs[e])
        w[e] = old_w - dl
        Em = sum(-beta * plaq_weight(w, plaqs[pi]) * np.cos(plaq_angle(field, plaqs[pi])) for pi in link_plaqs[e])
        w[e] = old_w
        force[e] = -(Ep - Em) / (2*dl)
    return force

# Run experiment
beta, kappa = 2.0, 3.0
Nth, Nms = 60, 30
N_fields = 3

print(f"\nN={N_fields} U(1) fields, β={beta}, κ={kappa}")
print(f"Thermalization: {Nth}, Measurements: {Nms}")

np.random.seed(42)
fields = [np.random.uniform(-np.pi, np.pi, n_links) for _ in range(N_fields)]
w = np.ones(n_links)

t0 = time.time()
# Thermalize
for s in range(Nth):
    for f in fields: sweep_gauge(f, w, beta, L, D)
    sweep_geo(fields, w, beta, kappa, L, D)
    if (s+1) % 20 == 0:
        print(f"  Therm {s+1}/{Nth}, <w>={np.mean(w):.3f}, t={time.time()-t0:.1f}s")

# Measure
cos_list = []
align_list = []
k0_list = []

for s in range(Nms):
    for f in fields: sweep_gauge(f, w, beta, L, D)
    sweep_geo(fields, w, beta, kappa, L, D)
    
    # Force alignment (gauge-only)
    forces = [gauge_force(f, w, beta, L, D) for f in fields]
    
    for i in range(N_fields):
        for j in range(i+1, N_fields):
            fi, fj = forces[i], forces[j]
            dot = np.dot(fi, fj)
            norm = np.linalg.norm(fi) * np.linalg.norm(fj)
            if norm > 1e-10:
                cos_list.append(dot/norm)
    
    F_net = sum(forces)
    align_list.append(np.linalg.norm(F_net) / sum(np.linalg.norm(f) for f in forces))
    
    # k=0 fraction
    dw = w - np.mean(w)
    k0_power = np.mean(w)**2 * len(w)
    total_power = np.sum(w**2)
    k0_list.append(k0_power / total_power)
    
    if (s+1) % 10 == 0:
        print(f"  Meas {s+1}/{Nms}, cos={np.mean(cos_list[-3:]):.4f}, align={align_list[-1]*100:.1f}%, <w>={np.mean(w):.3f}")

print(f"\n{'='*60}")
print(f"  4D U(1) RESULTS (N={N_fields})")
print(f"{'='*60}")
print(f"  Gauge-only cosine:  {np.mean(cos_list):+.4f} ± {np.std(cos_list)/np.sqrt(len(cos_list)):.4f}")
print(f"  Alignment ratio:    {np.mean(align_list)*100:.1f}%")
print(f"  k=0 fraction:       {np.mean(k0_list)*100:.1f}%")
print(f"  <w> final:          {np.mean(w):.3f}")
print(f"  Total time:         {time.time()-t0:.1f}s")
