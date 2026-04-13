"""
╔══════════════════════════════════════════════════════════════════╗
║  Hadamard Gauge-Geometry Coupling: Complete Monte Carlo Suite   ║
║  T = C ⊙ S — Necessity Theorem Verification                   ║
║                                                                 ║
║  Companion code for:                                            ║
║  [A] "The Hadamard structure of self-referential graphs"        ║
║  [B] "Gauge-geometry coupling is a necessary consequence        ║
║       of self-referential dynamics on graphs"                   ║
║                                                                 ║
║  K — April 2026                                                ║
╚══════════════════════════════════════════════════════════════════╝

Configurations tested:
  1. 2D U(1) — fixed lattice validation + dynamical Regge
  2. 2D SU(2) — non-abelian gauge group test
  3. 3D U(1) — dimensional robustness
  4. 4D U(1) — 4D abelian (pure Python, L=3)
  5. 4D SU(2) — the critical test (Numba JIT, L=4,6,8)

Requirements:
  pip install numpy scipy numba

Usage:
  python hadamard_mc_suite.py              # Run all tests
  python hadamard_mc_suite.py --quick      # Quick validation (2 min)
  python hadamard_mc_suite.py --4d-only    # 4D SU(2) only
"""

import numpy as np
from scipy.special import i0, i1
import json, time, sys

# ================================================================
# PART 1: 2D U(1) — Fixed lattice + Dynamical Regge
# ================================================================

def u1_2d_plaq(theta, L):
    return theta[:,:,0] + np.roll(theta[:,:,1],-1,0) - np.roll(theta[:,:,0],-1,1) - theta[:,:,1]

def u1_2d_sweep_fixed(theta, beta, L):
    for d in range(2):
        for x in range(L):
            for y in range(L):
                old = theta[x,y,d]
                p_old = u1_2d_plaq(theta, L)
                if d==0: s1 = -beta*(np.cos(p_old[x,y]) + np.cos(p_old[x,(y-1)%L]))
                else: s1 = -beta*(np.cos(p_old[x,y]) + np.cos(p_old[(x-1)%L,y]))
                theta[x,y,d] += np.random.uniform(-2,2)
                p_new = u1_2d_plaq(theta, L)
                if d==0: s2 = -beta*(np.cos(p_new[x,y]) + np.cos(p_new[x,(y-1)%L]))
                else: s2 = -beta*(np.cos(p_new[x,y]) + np.cos(p_new[(x-1)%L,y]))
                if s2-s1 > 0 and np.random.random() > np.exp(-(s2-s1)):
                    theta[x,y,d] = old

def u1_2d_weighted_plaq(theta, w, L):
    pa = u1_2d_plaq(theta, L)
    wp = np.sqrt(w[:,:,0]*np.roll(w[:,:,1],-1,0)*np.roll(w[:,:,0],-1,1)*w[:,:,1])
    return pa, wp

def u1_2d_sweep_dyn(theta, w, beta, kappa, L):
    for d in range(2):
        for x in range(L):
            for y in range(L):
                old = theta[x,y,d]
                pa_old, wp_old = u1_2d_weighted_plaq(theta, w, L)
                s_old = -beta*np.sum(wp_old*np.cos(pa_old))
                theta[x,y,d] += np.random.uniform(-2,2)
                pa_new, wp_new = u1_2d_weighted_plaq(theta, w, L)
                s_new = -beta*np.sum(wp_new*np.cos(pa_new))
                if s_new-s_old > 0 and np.random.random() > np.exp(-(s_new-s_old)):
                    theta[x,y,d] = old
    for d in range(2):
        for x in range(L):
            for y in range(L):
                old_w = w[x,y,d]
                pa, wp = u1_2d_weighted_plaq(theta, w, L)
                s_old = -beta*np.sum(wp*np.cos(pa)) + kappa*np.sum((w-1)**2)
                w[x,y,d] = max(0.1, old_w + np.random.normal(0, 0.05))
                pa2, wp2 = u1_2d_weighted_plaq(theta, w, L)
                s_new = -beta*np.sum(wp2*np.cos(pa2)) + kappa*np.sum((w-1)**2)
                if s_new-s_old > 0 and np.random.random() > np.exp(-(s_new-s_old)):
                    w[x,y,d] = old_w

def run_2d_u1(L=8, kappa=1.0, N_th=200, N_ms=300):
    print("\n" + "="*60)
    print("  2D U(1): Fixed lattice + Dynamical Regge")
    print("="*60)
    
    # Fixed lattice validation
    print("  Fixed lattice vs exact I₁(β)/I₀(β):")
    print(f"    {'β':>5}  {'MC':>8}  {'Exact':>8}  {'|Δ|':>8}")
    for beta in [0.5, 1.0, 2.0, 3.0, 5.0]:
        np.random.seed(42+int(beta*10))
        theta = np.random.uniform(-np.pi, np.pi, (L,L,2))
        for _ in range(300): u1_2d_sweep_fixed(theta, beta, L)
        vals = [np.mean(np.cos(u1_2d_plaq(theta,L))) for _ in range(500) if not u1_2d_sweep_fixed(theta,beta,L)]
        # Recompute properly
        vals = []
        for _ in range(500):
            u1_2d_sweep_fixed(theta, beta, L)
            vals.append(np.mean(np.cos(u1_2d_plaq(theta, L))))
        mc = np.mean(vals); ex = float(i1(beta)/i0(beta))
        print(f"    {beta:5.1f}  {mc:8.4f}  {ex:8.4f}  {abs(mc-ex):8.4f}")
    
    # Dynamical lattice
    print(f"\n  Dynamical lattice r(β):")
    print(f"    {'β':>5}  {'r':>8}  {'±':>8}  {'σ':>6}")
    results = []
    for beta in [0.5, 1.0, 1.5, 2.0, 3.0, 5.0]:
        np.random.seed(42+int(beta*100))
        theta = np.random.uniform(-np.pi, np.pi, (L,L,2))
        w = np.ones((L,L,2))
        for _ in range(N_th): u1_2d_sweep_dyn(theta, w, beta, kappa, L)
        corrs = []
        for _ in range(N_ms):
            u1_2d_sweep_dyn(theta, w, beta, kappa, L)
            pa, wp = u1_2d_weighted_plaq(theta, w, L)
            corrs.append(np.corrcoef(wp.flatten(), np.cos(pa).flatten())[0,1])
        r=np.mean(corrs); e=np.std(corrs)/np.sqrt(len(corrs))
        sig=abs(r)/e if e>0 else 0
        print(f"    {beta:5.1f}  {r:8.4f}  {e:8.4f}  {sig:6.1f}")
        results.append({'beta':beta,'r':round(float(r),4),'err':round(float(e),4),'sigma':round(float(sig),1)})
    return results

# ================================================================
# PART 2: 2D SU(2) — Non-abelian gauge group
# ================================================================

def su2_mul(a, b):
    return np.array([a[0]*b[0]-a[1]*b[1]-a[2]*b[2]-a[3]*b[3],
                     a[0]*b[1]+a[1]*b[0]+a[2]*b[3]-a[3]*b[2],
                     a[0]*b[2]-a[1]*b[3]+a[2]*b[0]+a[3]*b[1],
                     a[0]*b[3]+a[1]*b[2]-a[2]*b[1]+a[3]*b[0]])
def su2_dag(a): return np.array([a[0],-a[1],-a[2],-a[3]])

def su2_2d_plaq(U, x, y, L):
    p = su2_mul(U[x,y,0], U[(x+1)%L,y,1])
    p = su2_mul(p, su2_dag(U[x,(y+1)%L,0]))
    p = su2_mul(p, su2_dag(U[x,y,1]))
    return p[0]

def su2_2d_pw(w, x, y, L):
    return np.sqrt(w[x,y,0]*w[(x+1)%L,y,1]*w[x,(y+1)%L,0]*w[x,y,1])

def su2_2d_sweep(U, w, beta, kappa, L):
    for mu in range(2):
        for x in range(L):
            for y in range(L):
                old = U[x,y,mu].copy(); nu=1-mu
                xb=(x-(1 if nu==0 else 0))%L; yb=(y-(1 if nu==1 else 0))%L
                wp1=su2_2d_pw(w,x,y,L); cp1=su2_2d_plaq(U,x,y,L)
                wp2=su2_2d_pw(w,xb,yb,L); cp2=su2_2d_plaq(U,xb,yb,L)
                s_old=-beta*(wp1*cp1+wp2*cp2)
                r=np.random.randn(4)*np.array([0.1,0.5,0.5,0.5]); r[0]+=1; r/=np.linalg.norm(r)
                U[x,y,mu]=su2_mul(r, old)
                cp1n=su2_2d_plaq(U,x,y,L); cp2n=su2_2d_plaq(U,xb,yb,L)
                s_new=-beta*(wp1*cp1n+wp2*cp2n)
                if s_new-s_old>0 and np.random.random()>np.exp(-(s_new-s_old)): U[x,y,mu]=old
    for mu in range(2):
        for x in range(L):
            for y in range(L):
                ow=w[x,y,mu]; nu=1-mu
                xb=(x-(1 if nu==0 else 0))%L; yb=(y-(1 if nu==1 else 0))%L
                cp1=su2_2d_plaq(U,x,y,L); cp2=su2_2d_plaq(U,xb,yb,L)
                wp1=su2_2d_pw(w,x,y,L); wp2=su2_2d_pw(w,xb,yb,L)
                s_old=-beta*(wp1*cp1+wp2*cp2)+kappa*(ow-1)**2
                w[x,y,mu]=max(0.1,ow+np.random.normal(0,0.05))
                wp1n=su2_2d_pw(w,x,y,L); wp2n=su2_2d_pw(w,xb,yb,L)
                s_new=-beta*(wp1n*cp1+wp2n*cp2)+kappa*(w[x,y,mu]-1)**2
                if s_new-s_old>0 and np.random.random()>np.exp(-(s_new-s_old)): w[x,y,mu]=ow

def run_2d_su2(L=8, kappa=1.0, N_th=150, N_ms=200):
    print("\n" + "="*60)
    print("  2D SU(2): Non-abelian gauge group")
    print("="*60)
    print(f"    {'β':>5}  {'r':>8}  {'±':>8}  {'σ':>6}")
    results = []
    for beta in [0.5, 1.0, 1.5, 2.0, 3.0, 5.0]:
        np.random.seed(200+int(beta*10))
        U=np.zeros((L,L,2,4))
        for x in range(L):
            for y in range(L):
                for mu in range(2):
                    r=np.random.randn(4); U[x,y,mu]=r/np.linalg.norm(r)
        w=np.ones((L,L,2))
        for _ in range(N_th): su2_2d_sweep(U,w,beta,kappa,L)
        corrs=[]
        for _ in range(N_ms):
            su2_2d_sweep(U,w,beta,kappa,L)
            cp=[su2_2d_plaq(U,x,y,L) for x in range(L) for y in range(L)]
            wp=[su2_2d_pw(w,x,y,L) for x in range(L) for y in range(L)]
            corrs.append(np.corrcoef(wp,cp)[0,1])
        r=np.mean(corrs); e=np.std(corrs)/np.sqrt(len(corrs)); sig=abs(r)/e
        print(f"    {beta:5.1f}  {r:8.4f}  {e:8.4f}  {sig:6.1f}")
        results.append({'beta':beta,'r':round(float(r),4),'err':round(float(e),4),'sigma':round(float(sig),1)})
    return results

# ================================================================
# PART 3: 3D U(1) — Dimensional robustness
# ================================================================

def run_3d_u1(L=5, kappa=1.0, N_th=100, N_ms=150):
    print("\n" + "="*60)
    print("  3D U(1): Dimensional robustness")
    print("="*60)
    
    def aff(theta,w,x,y,z,d,L):
        coords=np.array([x,y,z]); s=0.0
        for nu in range(3):
            if nu==d: continue
            mu=d
            for sign in [+1,-1]:
                c=list(coords) if sign==1 else list(coords)
                if sign==-1: c[nu]=(c[nu]-1)%L
                cm=list(c); cm[mu]=(cm[mu]+1)%L
                cn=list(c); cn[nu]=(cn[nu]+1)%L
                pa=(theta[c[0],c[1],c[2],mu]+theta[cm[0],cm[1],cm[2],nu]
                    -theta[cn[0],cn[1],cn[2],mu]-theta[c[0],c[1],c[2],nu])
                wp=np.sqrt(w[c[0],c[1],c[2],mu]*w[cm[0],cm[1],cm[2],nu]*
                           w[cn[0],cn[1],cn[2],mu]*w[c[0],c[1],c[2],nu])
                s+=wp*np.cos(pa)
        return s
    
    def sweep3(theta,w,beta,kappa,L):
        for d in range(3):
            for x in range(L):
                for y in range(L):
                    for z in range(L):
                        old=theta[x,y,z,d]; s1=aff(theta,w,x,y,z,d,L)
                        theta[x,y,z,d]+=np.random.uniform(-2,2); s2=aff(theta,w,x,y,z,d,L)
                        dS=-beta*(s2-s1)
                        if dS>0 and np.random.random()>np.exp(-dS): theta[x,y,z,d]=old
        for d in range(3):
            for x in range(L):
                for y in range(L):
                    for z in range(L):
                        ow=w[x,y,z,d]
                        s1=-beta*aff(theta,w,x,y,z,d,L)+kappa*(ow-1)**2
                        w[x,y,z,d]=max(0.1,ow+np.random.normal(0,0.05))
                        s2=-beta*aff(theta,w,x,y,z,d,L)+kappa*(w[x,y,z,d]-1)**2
                        if s2-s1>0 and np.random.random()>np.exp(-(s2-s1)): w[x,y,z,d]=ow
    
    def meas3(theta,w,L):
        ca=[]; wa=[]
        for mu in range(3):
            for nu in range(mu+1,3):
                for x in range(L):
                    for y in range(L):
                        for z in range(L):
                            c=[x,y,z]; cm=list(c); cm[mu]=(cm[mu]+1)%L
                            cn=list(c); cn[nu]=(cn[nu]+1)%L
                            pa=(theta[c[0],c[1],c[2],mu]+theta[cm[0],cm[1],cm[2],nu]
                                -theta[cn[0],cn[1],cn[2],mu]-theta[c[0],c[1],c[2],nu])
                            wp=np.sqrt(w[c[0],c[1],c[2],mu]*w[cm[0],cm[1],cm[2],nu]*
                                       w[cn[0],cn[1],cn[2],mu]*w[c[0],c[1],c[2],nu])
                            ca.append(np.cos(pa)); wa.append(wp)
        return np.corrcoef(wa,ca)[0,1]
    
    print(f"    {'β':>5}  {'r':>8}  {'±':>8}  {'σ':>6}")
    results=[]
    for beta in [0.5,1.0,1.5,2.0,3.0,5.0]:
        np.random.seed(300+int(beta*10))
        theta=np.random.uniform(-np.pi,np.pi,(L,L,L,3)); w=np.ones((L,L,L,3))
        for _ in range(N_th): sweep3(theta,w,beta,kappa,L)
        corrs=[]
        for _ in range(N_ms):
            sweep3(theta,w,beta,kappa,L); corrs.append(meas3(theta,w,L))
        r=np.mean(corrs); e=np.std(corrs)/np.sqrt(len(corrs)); sig=abs(r)/e
        print(f"    {beta:5.1f}  {r:8.4f}  {e:8.4f}  {sig:6.1f}")
        results.append({'beta':beta,'r':round(float(r),4),'err':round(float(e),4),'sigma':round(float(sig),1)})
    return results

# ================================================================
# PART 3.5: 4D U(1) — 4D abelian (pure Python, small lattice)
# ================================================================

def run_4d_u1(L=3, kappa=1.0, N_th=80, N_ms=100):
    print("\n" + "="*60)
    print("  4D U(1): 4D abelian gauge theory")
    print("="*60)
    
    def aff4(theta,w,coords,d,L):
        s=0.0
        for nu in range(4):
            if nu==d: continue
            for sign in [+1,-1]:
                c=list(coords) if sign==1 else list(coords)
                if sign==-1: c[nu]=(c[nu]-1)%L
                cm=list(c); cm[d]=(cm[d]+1)%L
                cn=list(c); cn[nu]=(cn[nu]+1)%L
                pa=(theta[c[0],c[1],c[2],c[3],d]+theta[cm[0],cm[1],cm[2],cm[3],nu]
                    -theta[cn[0],cn[1],cn[2],cn[3],d]-theta[c[0],c[1],c[2],c[3],nu])
                wp=np.sqrt(w[c[0],c[1],c[2],c[3],d]*w[cm[0],cm[1],cm[2],cm[3],nu]*
                           w[cn[0],cn[1],cn[2],cn[3],d]*w[c[0],c[1],c[2],c[3],nu])
                s+=wp*np.cos(pa)
        return s
    
    def sweep4(theta,w,beta,kappa,L):
        for d in range(4):
            for x in range(L):
                for y in range(L):
                    for z in range(L):
                        for t in range(L):
                            coords=[x,y,z,t]; old=theta[x,y,z,t,d]
                            s1=aff4(theta,w,coords,d,L)
                            theta[x,y,z,t,d]+=np.random.uniform(-2,2)
                            s2=aff4(theta,w,coords,d,L); dS=-beta*(s2-s1)
                            if dS>0 and np.random.random()>np.exp(-dS): theta[x,y,z,t,d]=old
        for d in range(4):
            for x in range(L):
                for y in range(L):
                    for z in range(L):
                        for t in range(L):
                            coords=[x,y,z,t]; ow=w[x,y,z,t,d]
                            s1=-beta*aff4(theta,w,coords,d,L)+kappa*(ow-1)**2
                            w[x,y,z,t,d]=max(0.1,ow+np.random.normal(0,0.05))
                            s2=-beta*aff4(theta,w,coords,d,L)+kappa*(w[x,y,z,t,d]-1)**2
                            if s2-s1>0 and np.random.random()>np.exp(-(s2-s1)): w[x,y,z,t,d]=ow
    
    def meas4(theta,w,L):
        ca=[]; wa=[]
        for mu in range(4):
            for nu in range(mu+1,4):
                for x in range(L):
                    for y in range(L):
                        for z in range(L):
                            for t in range(L):
                                c=[x,y,z,t]; cm=list(c); cm[mu]=(cm[mu]+1)%L
                                cn=list(c); cn[nu]=(cn[nu]+1)%L
                                pa=(theta[c[0],c[1],c[2],c[3],mu]+theta[cm[0],cm[1],cm[2],cm[3],nu]
                                    -theta[cn[0],cn[1],cn[2],cn[3],mu]-theta[c[0],c[1],c[2],c[3],nu])
                                wp=np.sqrt(w[c[0],c[1],c[2],c[3],mu]*w[cm[0],cm[1],cm[2],cm[3],nu]*
                                           w[cn[0],cn[1],cn[2],cn[3],mu]*w[c[0],c[1],c[2],c[3],nu])
                                ca.append(np.cos(pa)); wa.append(wp)
        return np.corrcoef(wa,ca)[0,1]
    
    print(f"    {'β':>5}  {'r':>8}  {'±':>8}  {'σ':>6}")
    results=[]
    for beta in [0.5,1.0,1.5,2.0,3.0,5.0]:
        np.random.seed(400+int(beta*10))
        theta=np.random.uniform(-np.pi,np.pi,(L,L,L,L,4)); w=np.ones((L,L,L,L,4))
        for _ in range(N_th): sweep4(theta,w,beta,kappa,L)
        corrs=[]
        for _ in range(N_ms):
            sweep4(theta,w,beta,kappa,L); corrs.append(meas4(theta,w,L))
        r=np.mean(corrs); e=np.std(corrs)/np.sqrt(len(corrs)); sig=abs(r)/e
        print(f"    {beta:5.1f}  {r:8.4f}  {e:8.4f}  {sig:6.1f}")
        results.append({'beta':beta,'r':round(float(r),4),'err':round(float(e),4),'sigma':round(float(sig),1)})
    return results

# ================================================================
# PART 4: 4D SU(2) — Critical test (Numba JIT)
# ================================================================

def run_4d_su2(Ls=[4,6,8], kappa=1.0, N_th=200, N_ms=300):
    """4D SU(2) with Numba JIT. See su2_4d_colab.py for standalone version."""
    from numba import njit
    
    @njit(cache=True)
    def sm(a,b,o):
        o[0]=a[0]*b[0]-a[1]*b[1]-a[2]*b[2]-a[3]*b[3]
        o[1]=a[0]*b[1]+a[1]*b[0]+a[2]*b[3]-a[3]*b[2]
        o[2]=a[0]*b[2]-a[1]*b[3]+a[2]*b[0]+a[3]*b[1]
        o[3]=a[0]*b[3]+a[1]*b[2]-a[2]*b[1]+a[3]*b[0]
    @njit(cache=True)
    def smd(a,b,o):
        o[0]=a[0]*b[0]+a[1]*b[1]+a[2]*b[2]+a[3]*b[3]
        o[1]=-a[0]*b[1]+a[1]*b[0]-a[2]*b[3]+a[3]*b[2]
        o[2]=-a[0]*b[2]+a[1]*b[3]+a[2]*b[0]-a[3]*b[1]
        o[3]=-a[0]*b[3]-a[1]*b[2]+a[2]*b[1]+a[3]*b[0]
    @njit(cache=True)
    def sni(e):
        r=np.empty(4);r[0]=1.0+e*np.random.randn()*0.1
        r[1]=e*np.random.randn();r[2]=e*np.random.randn();r[3]=e*np.random.randn()
        n=np.sqrt(r[0]**2+r[1]**2+r[2]**2+r[3]**2);r/=n;return r
    @njit(cache=True)
    def i4(x,y,z,t,L):return(x%L)*L*L*L+(y%L)*L*L+(z%L)*L+(t%L)
    @njit(cache=True)
    def c4(i,L):return i//(L*L*L)%L,(i//(L*L))%L,(i//L)%L,i%L
    @njit(cache=True)
    def np4(x,y,z,t,m,L):
        if m==0:return(x+1)%L,y,z,t
        elif m==1:return x,(y+1)%L,z,t
        elif m==2:return x,y,(z+1)%L,t
        else:return x,y,z,(t+1)%L
    @njit(cache=True)
    def nm4(x,y,z,t,m,L):
        if m==0:return(x-1)%L,y,z,t
        elif m==1:return x,(y-1)%L,z,t
        elif m==2:return x,y,(z-1)%L,t
        else:return x,y,z,(t-1)%L
    @njit(cache=True)
    def pq(U,x,y,z,t,u,v,L):
        s=i4(x,y,z,t,L);xm,ym,zm,tm=np4(x,y,z,t,u,L);smu=i4(xm,ym,zm,tm,L)
        xn,yn,zn,tn=np4(x,y,z,t,v,L);snu=i4(xn,yn,zn,tn,L)
        t1=np.empty(4);t2=np.empty(4);t3=np.empty(4)
        sm(U[s,u],U[smu,v],t1);smd(t1,U[snu,u],t2);smd(t2,U[s,v],t3);return t3[0]
    @njit(cache=True)
    def pw(w,x,y,z,t,u,v,L):
        s=i4(x,y,z,t,L);xm,ym,zm,tm=np4(x,y,z,t,u,L);smu=i4(xm,ym,zm,tm,L)
        xn,yn,zn,tn=np4(x,y,z,t,v,L);snu=i4(xn,yn,zn,tn,L)
        return np.sqrt(w[s,u]*w[smu,v]*w[snu,u]*w[s,v])
    @njit(cache=True)
    def la(U,w,x,y,z,t,m,b,L):
        s=0.0
        for v in range(4):
            if v==m:continue
            s+=-b*pw(w,x,y,z,t,m,v,L)*pq(U,x,y,z,t,m,v,L)
            xb,yb,zb,tb=nm4(x,y,z,t,v,L)
            s+=-b*pw(w,xb,yb,zb,tb,m,v,L)*pq(U,xb,yb,zb,tb,m,v,L)
        return s
    @njit(cache=True)
    def sg(U,w,b,L,e):
        V=L**4
        for i in range(V):
            x,y,z,t=c4(i,L)
            for m in range(4):
                s=i4(x,y,z,t,L);o=U[s,m].copy()
                sb=la(U,w,x,y,z,t,m,b,L);R=sni(e);n=np.empty(4);sm(R,o,n);U[s,m]=n
                sa=la(U,w,x,y,z,t,m,b,L);d=sa-sb
                if d>0 and np.random.random()>=np.exp(-d):U[s,m]=o
    @njit(cache=True)
    def swp(U,w,b,k,L,d):
        V=L**4
        for i in range(V):
            x,y,z,t=c4(i,L)
            for m in range(4):
                s=i4(x,y,z,t,L);ow=w[s,m]
                sb=la(U,w,x,y,z,t,m,b,L)+k*(ow-1)**2
                nw=max(0.1,ow+d*np.random.randn());w[s,m]=nw
                sa=la(U,w,x,y,z,t,m,b,L)+k*(nw-1)**2;ds=sa-sb
                if ds>0 and np.random.random()>=np.exp(-ds):w[s,m]=ow
    @njit(cache=True)
    def mc(U,w,L):
        V=L**4;n=V*6;cv=np.empty(n);wv=np.empty(n);k=0
        for i in range(V):
            x,y,z,t=c4(i,L)
            for u in range(4):
                for v in range(u+1,4):
                    cv[k]=pq(U,x,y,z,t,u,v,L);wv[k]=pw(w,x,y,z,t,u,v,L);k+=1
        m1=np.mean(cv);m2=np.mean(wv);s1=np.std(cv);s2=np.std(wv)
        if s1<1e-15 or s2<1e-15:return 0.0
        return np.mean((cv-m1)*(wv-m2))/(s1*s2)
    @njit(cache=True)
    def ini(V,nd):
        U=np.empty((V,nd,4))
        for i in range(V):
            for m in range(nd):
                r=np.random.randn(4);r/=np.sqrt(r[0]**2+r[1]**2+r[2]**2+r[3]**2);U[i,m]=r
        return U
    
    # JIT warmup
    print("\n" + "="*60)
    print("  4D SU(2): Critical test with finite-size scaling")
    print("="*60)
    print("  JIT compiling...", flush=True)
    np.random.seed(0);Ut=ini(16,4);wt=np.ones((16,4))
    sg(Ut,wt,1.0,2,0.5);swp(Ut,wt,1.0,1.0,2,0.05);mc(Ut,wt,2)
    
    all_results = {}
    for L in Ls:
        V=L**4; betas=[0.5,1.0,1.5,2.0,3.0,5.0]
        print(f"\n  L={L}, V={V}:")
        print(f"    {'β':>5}  {'r':>8}  {'±':>8}  {'σ':>6}  {'t':>5}")
        results=[]
        for beta in betas:
            np.random.seed(42+int(beta*100)+L*7); t0=time.time()
            U=ini(V,4); w=np.ones((V,4))
            for _ in range(N_th): sg(U,w,beta,L,0.5); swp(U,w,beta,kappa,L,0.05)
            cs=[]
            for _ in range(N_ms):
                sg(U,w,beta,L,0.5); swp(U,w,beta,kappa,L,0.05); cs.append(mc(U,w,L))
            r=np.mean(cs);e=np.std(cs)/np.sqrt(len(cs));si=abs(r)/e if e>0 else 0
            dt=time.time()-t0
            print(f"    {beta:5.1f}  {r:8.4f}  {e:8.4f}  {si:6.1f}  {dt:5.0f}s")
            results.append({'beta':beta,'r':round(float(r),4),'err':round(float(e),4),'sigma':round(float(si),1)})
        all_results[f'L{L}'] = results
    return all_results

# ================================================================
# MAIN
# ================================================================

if __name__ == '__main__':
    quick = '--quick' in sys.argv
    only4d = '--4d-only' in sys.argv
    
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  Hadamard Gauge-Geometry Coupling: Monte Carlo Suite    ║")
    print("║  T = C ⊙ S                                            ║")
    print("╚══════════════════════════════════════════════════════════╝")
    
    all_results = {}
    
    if not only4d:
        all_results['2d_u1'] = run_2d_u1(N_th=50 if quick else 200, N_ms=80 if quick else 300)
        all_results['2d_su2'] = run_2d_su2(N_th=50 if quick else 150, N_ms=80 if quick else 200)
        all_results['3d_u1'] = run_3d_u1(N_th=30 if quick else 100, N_ms=50 if quick else 150)
        all_results['4d_u1'] = run_4d_u1(N_th=30 if quick else 80, N_ms=40 if quick else 100)
    
    all_results['4d_su2'] = run_4d_su2(
        Ls=[4] if quick else [4,6,8],
        N_th=50 if quick else 200, N_ms=80 if quick else 300)
    
    with open('hadamard_mc_complete_results.json', 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print("\n" + "="*60)
    print("  COMPLETE. Results saved to hadamard_mc_complete_results.json")
    print("="*60)
