"""
Paper F: Gauge-only per-field force alignment
Corrected version: elastic term excluded from per-field forces
"""
import numpy as np

# === 2D U(1) engine ===
def u1p(f,x,y,L): return f[x,y,0]+f[(x+1)%L,y,1]-f[x,(y+1)%L,0]-f[x,y,1]
def pw2(w,x,y,L): return np.sqrt(abs(w[x,y,0]*w[(x+1)%L,y,1]*w[x,(y+1)%L,0]*w[x,y,1]))

def sw_u1(f,w,beta,L):
    for mu in range(2):
        for x in range(L):
            for y in range(L):
                nu=1-mu
                xb=(x-(1 if nu==0 else 0))%L; yb=(y-(1 if nu==1 else 0))%L
                w1=pw2(w,x,y,L);c1=np.cos(u1p(f,x,y,L))
                w2=pw2(w,xb,yb,L);c2=np.cos(u1p(f,xb,yb,L))
                so=-beta*(w1*c1+w2*c2)
                f[x,y,mu]+=np.random.uniform(-2,2)
                sn=-beta*(w1*np.cos(u1p(f,x,y,L))+w2*np.cos(u1p(f,xb,yb,L)))
                if sn-so>0 and np.random.random()>np.exp(-(sn-so)): f[x,y,mu]=f[x,y,mu]-np.random.uniform(-2,2) # undo
                # Proper undo:
                pass  # already handled inline

def sw_u1_proper(f,w,beta,L):
    for mu in range(2):
        for x in range(L):
            for y in range(L):
                nu=1-mu
                xb=(x-(1 if nu==0 else 0))%L; yb=(y-(1 if nu==1 else 0))%L
                w1=pw2(w,x,y,L);c1=np.cos(u1p(f,x,y,L))
                w2=pw2(w,xb,yb,L);c2=np.cos(u1p(f,xb,yb,L))
                so=-beta*(w1*c1+w2*c2)
                old = f[x,y,mu]
                f[x,y,mu]+=np.random.uniform(-2,2)
                sn=-beta*(w1*np.cos(u1p(f,x,y,L))+w2*np.cos(u1p(f,xb,yb,L)))
                if sn-so>0 and np.random.random()>np.exp(-(sn-so)): f[x,y,mu]=old

def geo(fields,w,beta,kappa,L):
    for mu in range(2):
        for x in range(L):
            for y in range(L):
                nu=1-mu
                xb=(x-(1 if nu==0 else 0))%L; yb=(y-(1 if nu==1 else 0))%L
                w1=pw2(w,x,y,L);w2=pw2(w,xb,yb,L)
                cv=[(np.cos(u1p(f,x,y,L)),np.cos(u1p(f,xb,yb,L))) for f in fields]
                sg=sum(-beta*(w1*c1+w2*c2) for c1,c2 in cv)
                ow=w[x,y,mu]
                so=sg+kappa*(ow-1)**2
                w[x,y,mu]=max(0.1,ow+np.random.normal(0,0.05))
                w1n=pw2(w,x,y,L);w2n=pw2(w,xb,yb,L)
                sgn=sum(-beta*(w1n*c1+w2n*c2) for c1,c2 in cv)
                sn=sgn+kappa*(w[x,y,mu]-1)**2
                if sn-so>0 and np.random.random()>np.exp(-(sn-so)): w[x,y,mu]=ow

def compute_gauge_only_force(field, w, beta, L, dl=1e-4):
    """Gauge-only force: EXCLUDES elastic term"""
    force = np.zeros_like(w)
    for mu in range(2):
        for x in range(L):
            for y in range(L):
                nu=1-mu
                xb=(x-(1 if nu==0 else 0))%L; yb=(y-(1 if nu==1 else 0))%L
                ow = w[x,y,mu]
                # E_gauge at w+dl
                w[x,y,mu] = ow + dl
                w1p=pw2(w,x,y,L); w2p=pw2(w,xb,yb,L)
                c1=np.cos(u1p(field,x,y,L)); c2=np.cos(u1p(field,xb,yb,L))
                E_plus = -beta*(w1p*c1+w2p*c2)  # NO kappa term
                # E_gauge at w-dl
                w[x,y,mu] = ow - dl
                w1m=pw2(w,x,y,L); w2m=pw2(w,xb,yb,L)
                E_minus = -beta*(w1m*c1+w2m*c2)  # NO kappa term
                w[x,y,mu] = ow
                force[x,y,mu] = -(E_plus - E_minus) / (2*dl)
    return force

def compute_full_force(field, w, beta, kappa, L, dl=1e-4):
    """Full force: INCLUDES elastic term (original code)"""
    force = np.zeros_like(w)
    for mu in range(2):
        for x in range(L):
            for y in range(L):
                nu=1-mu
                xb=(x-(1 if nu==0 else 0))%L; yb=(y-(1 if nu==1 else 0))%L
                ow = w[x,y,mu]
                w[x,y,mu] = ow + dl
                w1p=pw2(w,x,y,L); w2p=pw2(w,xb,yb,L)
                c1=np.cos(u1p(field,x,y,L)); c2=np.cos(u1p(field,xb,yb,L))
                E_plus = -beta*(w1p*c1+w2p*c2) + kappa*(w[x,y,mu]-1)**2
                w[x,y,mu] = ow - dl
                w1m=pw2(w,x,y,L); w2m=pw2(w,xb,yb,L)
                E_minus = -beta*(w1m*c1+w2m*c2) + kappa*(w[x,y,mu]-1)**2
                w[x,y,mu] = ow
                force[x,y,mu] = -(E_plus - E_minus) / (2*dl)
    return force

# === Main experiment ===
L, beta, kappa = 8, 2.0, 3.0
Nth, Nms = 100, 50  # reduced for speed

print("="*70)
print("  Paper F Correction: Gauge-Only vs Full Per-Field Force Alignment")
print("="*70)
print(f"  L={L}, β={beta}, κ={kappa}, {Nth} therm + {Nms} meas sweeps")
print()
print(f"  {'N':>4}  {'Gauge-only cos':>14}  {'Full cos':>14}  {'Gauge align%':>12}  {'Full align%':>12}")
print(f"  {'─'*4}  {'─'*14}  {'─'*14}  {'─'*12}  {'─'*12}")

for N in [2, 3, 5, 10]:
    np.random.seed(55555+N)
    fs = [np.random.uniform(-np.pi, np.pi, (L,L,2)) for _ in range(N)]
    w = np.ones((L,L,2))
    
    # Thermalize
    for _ in range(Nth):
        for f in fs: sw_u1_proper(f, w, beta, L)
        geo(fs, w, beta, kappa, L)
    
    gauge_cos_list = []
    full_cos_list = []
    gauge_align_list = []
    full_align_list = []
    
    for _ in range(Nms):
        for f in fs: sw_u1_proper(f, w, beta, L)
        geo(fs, w, beta, kappa, L)
        
        # Compute both types of forces
        gauge_forces = [compute_gauge_only_force(f, w, beta, L) for f in fs]
        full_forces = [compute_full_force(f, w, beta, kappa, L) for f in fs]
        
        # Pairwise cosine (gauge-only)
        for i in range(min(N, 3)):
            for j in range(i+1, min(N, 4)):
                fi = gauge_forces[i].ravel()
                fj = gauge_forces[j].ravel()
                dot = np.dot(fi, fj)
                norm = np.linalg.norm(fi) * np.linalg.norm(fj)
                if norm > 1e-10:
                    gauge_cos_list.append(dot/norm)
                    
                fi2 = full_forces[i].ravel()
                fj2 = full_forces[j].ravel()
                dot2 = np.dot(fi2, fj2)
                norm2 = np.linalg.norm(fi2) * np.linalg.norm(fj2)
                if norm2 > 1e-10:
                    full_cos_list.append(dot2/norm2)
        
        # Alignment ratio (gauge-only)
        F_net_g = sum(gauge_forces)
        gauge_align_list.append(np.linalg.norm(F_net_g.ravel()) / sum(np.linalg.norm(f.ravel()) for f in gauge_forces))
        
        F_net_f = sum(full_forces)
        full_align_list.append(np.linalg.norm(F_net_f.ravel()) / sum(np.linalg.norm(f.ravel()) for f in full_forces))
    
    gc = np.mean(gauge_cos_list) if gauge_cos_list else 1.0
    fc = np.mean(full_cos_list) if full_cos_list else 1.0
    ga = np.mean(gauge_align_list) * 100
    fa = np.mean(full_align_list) * 100
    
    print(f"  {N:4d}  {gc:+14.4f}  {fc:+14.4f}  {ga:11.1f}%  {fa:11.1f}%")

print()
print("  Gauge-only = force from −β w_P cos Θ only (no elastic term)")
print("  Full       = force from −β w_P cos Θ + κ(w−1)² (original code)")
