"""
╔═══════════════════════════════════════════════════════════════════════╗
║  Hadamard Photonic Neural Network: Improved Simulation (v2)           ║
║  Fixes: LayerNorm, gradient clipping, realistic optical noise         ║
║                                                                       ║
║  Hyeokjun Kwon — April 2026                                          ║
╚═══════════════════════════════════════════════════════════════════════╝
"""

import numpy as np
import json, time

# ================================================================
# Data
# ================================================================

def make_circles(n=1000, noise=0.1, seed=42):
    rng = np.random.RandomState(seed)
    n_per = n // 2
    r_inner = rng.uniform(0, 0.5, n_per) + rng.randn(n_per) * noise * 0.1
    t_inner = rng.uniform(0, 2*np.pi, n_per)
    x_inner = np.column_stack([r_inner * np.cos(t_inner), r_inner * np.sin(t_inner)])
    r_outer = rng.uniform(0.7, 1.0, n_per) + rng.randn(n_per) * noise * 0.1
    t_outer = rng.uniform(0, 2*np.pi, n_per)
    x_outer = np.column_stack([r_outer * np.cos(t_outer), r_outer * np.sin(t_outer)])
    X = np.vstack([x_inner, x_outer])
    y = np.concatenate([np.zeros(n_per), np.ones(n_per)])
    idx = rng.permutation(n)
    return X[idx], y[idx]

def make_spiral(n=1000, noise=0.1, seed=42):
    rng = np.random.RandomState(seed)
    n_per = n // 2
    t = np.linspace(0, 3*np.pi, n_per)
    r = t / (3*np.pi)
    x1 = np.column_stack([r*np.cos(t), r*np.sin(t)]) + rng.randn(n_per, 2)*noise*0.05
    x2 = np.column_stack([r*np.cos(t+np.pi), r*np.sin(t+np.pi)]) + rng.randn(n_per, 2)*noise*0.05
    X = np.vstack([x1, x2])
    y = np.concatenate([np.zeros(n_per), np.ones(n_per)])
    idx = rng.permutation(n)
    return X[idx], y[idx]

# ================================================================
# Optical noise models
# ================================================================

def gaussian_noise(shape, rng, sigma):
    """Additive Gaussian noise (thermal/electronic)."""
    return rng.randn(*shape) * sigma

def shot_noise(signal, rng, scale=0.1):
    """Shot noise: proportional to sqrt(|signal|). Photon counting statistics."""
    return rng.randn(*signal.shape) * np.sqrt(np.abs(signal) + 1e-10) * scale

def phase_noise(signal, rng, sigma=0.1):
    """Phase noise: random phase rotation. Common in coherent optics."""
    phase = rng.randn(*signal.shape) * sigma
    # For real-valued signals, phase noise manifests as multiplicative noise
    return signal * (1 + phase) - signal  # Returns the noise component

def insertion_loss(signal, loss_per_layer=0.05):
    """Insertion loss: signal attenuation per layer."""
    return signal * (1 - loss_per_layer)

def apply_optical_noise(signal, rng, noise_cfg):
    """Apply combined optical noise model."""
    noisy = signal.copy()
    
    if noise_cfg.get('gaussian', 0) > 0:
        noisy += gaussian_noise(signal.shape, rng, noise_cfg['gaussian'])
    
    if noise_cfg.get('shot', 0) > 0:
        noisy += shot_noise(signal, rng, noise_cfg['shot'])
    
    if noise_cfg.get('phase', 0) > 0:
        noisy += phase_noise(signal, rng, noise_cfg['phase'])
    
    if noise_cfg.get('loss', 0) > 0:
        noisy = insertion_loss(noisy, noise_cfg['loss'])
    
    return noisy

# ================================================================
# Utilities
# ================================================================

def sigmoid(x):
    x = np.clip(x, -500, 500)
    return 1.0 / (1.0 + np.exp(-x))

def init_w(shape, rng, scale=0.5):
    return rng.randn(*shape) * scale / np.sqrt(shape[0])

def layer_norm(x, eps=1e-5):
    """Layer normalization — physically corresponds to energy-preserving gain control."""
    mu = np.mean(x, axis=-1, keepdims=True)
    var = np.var(x, axis=-1, keepdims=True)
    return (x - mu) / np.sqrt(var + eps)

def clip_grad(g, max_norm=5.0):
    """Gradient clipping."""
    norm = np.linalg.norm(g)
    if norm > max_norm:
        g = g * max_norm / norm
    return g

# ================================================================
# Networks
# ================================================================

class HadamardNetV2:
    """
    Hadamard network with LayerNorm and gradient clipping.
    
    Layer: h = LayerNorm( (Wx + b1) ⊙ (Vx + b2) )
    
    LayerNorm = energy-preserving normalization (physical: optical gain control)
    """
    def __init__(self, layer_sizes, seed=42):
        self.rng = np.random.RandomState(seed)
        self.W, self.V, self.b1, self.b2 = [], [], [], []
        self.gamma, self.beta_ln = [], []  # LayerNorm params
        
        for i in range(len(layer_sizes) - 1):
            n_in, n_out = layer_sizes[i], layer_sizes[i+1]
            if i < len(layer_sizes) - 2:
                self.W.append(init_w((n_in, n_out), self.rng, 0.3))
                self.V.append(init_w((n_in, n_out), self.rng, 0.3))
                self.b1.append(np.zeros(n_out))
                self.b2.append(np.ones(n_out) * 0.5)
                self.gamma.append(np.ones(n_out))
                self.beta_ln.append(np.zeros(n_out))
            else:
                self.W.append(init_w((n_in, n_out), self.rng, 0.3))
                self.V.append(None)
                self.b1.append(np.zeros(n_out))
                self.b2.append(None)
    
    def forward(self, x, noise_cfg=None):
        self.cache_x, self.cache_c, self.cache_s, self.cache_h = [x], [], [], []
        self.cache_h_pre_norm = []
        h = x
        
        for i in range(len(self.W) - 1):
            c = h @ self.W[i] + self.b1[i]
            s = h @ self.V[i] + self.b2[i]
            
            if noise_cfg:
                c = apply_optical_noise(c, self.rng, noise_cfg)
                s = apply_optical_noise(s, self.rng, noise_cfg)
            
            h_raw = c * s  # Hadamard product
            
            # LayerNorm (energy-preserving normalization)
            h = layer_norm(h_raw) * self.gamma[i] + self.beta_ln[i]
            
            self.cache_c.append(c)
            self.cache_s.append(s)
            self.cache_h_pre_norm.append(h_raw)
            self.cache_x.append(h)
        
        z = h @ self.W[-1] + self.b1[-1]
        return sigmoid(z)
    
    def train_step(self, x, y, lr=0.01):
        out = self.forward(x)
        batch = x.shape[0]
        delta = (out - y.reshape(-1, 1)) / batch
        
        g_W_out = clip_grad(self.cache_x[-1].T @ delta)
        g_b_out = np.sum(delta, axis=0)
        
        delta = delta @ self.W[-1].T
        
        for i in range(len(self.W) - 2, -1, -1):
            c, s = self.cache_c[i], self.cache_s[i]
            x_in = self.cache_x[i]
            
            # Approximate LN gradient (simplified)
            delta_c = delta * self.gamma[i].reshape(1, -1) * s
            delta_s = delta * self.gamma[i].reshape(1, -1) * c
            
            h_raw = self.cache_h_pre_norm[i]
            mu = np.mean(h_raw, axis=-1, keepdims=True)
            var = np.var(h_raw, axis=-1, keepdims=True)
            inv_std = 1.0 / np.sqrt(var + 1e-5)
            
            self.W[i] -= lr * clip_grad(x_in.T @ delta_c)
            self.V[i] -= lr * clip_grad(x_in.T @ delta_s)
            self.b1[i] -= lr * np.sum(delta_c, axis=0)
            self.b2[i] -= lr * np.sum(delta_s, axis=0)
            
            delta = delta_c @ self.W[i].T + delta_s @ self.V[i].T
        
        self.W[-1] -= lr * g_W_out
        self.b1[-1] -= lr * g_b_out
        return out


class StandardMLPV2:
    """Standard MLP with LayerNorm."""
    def __init__(self, layer_sizes, activation='relu', seed=42):
        self.rng = np.random.RandomState(seed)
        self.activation = activation
        self.weights, self.biases = [], []
        for i in range(len(layer_sizes) - 1):
            self.weights.append(init_w((layer_sizes[i], layer_sizes[i+1]), self.rng))
            self.biases.append(np.zeros(layer_sizes[i+1]))
    
    def forward(self, x, noise_cfg=None):
        self.cache = [x]
        h = x
        for i in range(len(self.weights) - 1):
            z = h @ self.weights[i] + self.biases[i]
            if noise_cfg:
                z = apply_optical_noise(z, self.rng, noise_cfg)
            z = layer_norm(z)
            if self.activation == 'relu':
                h = np.maximum(0, z)
            else:
                h = sigmoid(z)
            self.cache.append(h)
        z = h @ self.weights[-1] + self.biases[-1]
        return sigmoid(z)
    
    def train_step(self, x, y, lr=0.01):
        out = self.forward(x)
        batch = x.shape[0]
        delta = (out - y.reshape(-1, 1)) / batch
        for i in range(len(self.weights) - 1, -1, -1):
            g_w = clip_grad(self.cache[i].T @ delta)
            g_b = np.sum(delta, axis=0)
            if i > 0:
                delta = delta @ self.weights[i].T
                if self.activation == 'relu':
                    delta *= (self.cache[i] > 0).astype(float)
                else:
                    delta *= self.cache[i] * (1 - self.cache[i])
            self.weights[i] -= lr * g_w
            self.biases[i] -= lr * g_b
        return out


# ================================================================
# Experiments
# ================================================================

def accuracy(model, X, y, noise_cfg=None):
    pred = model.forward(X, noise_cfg=noise_cfg)
    return float(np.mean((pred.flatten() > 0.5) == y))

def run_experiment(title, X_train, y_train, X_test, y_test,
                   layer_sizes, noise_configs, epochs=500, lr=0.05, n_avg=20):
    """Run full comparison experiment."""
    print(f"\n  {title}")
    print(f"  {'─'*60}")
    
    results = {}
    
    for name, make_model in [
        ('Hadamard', lambda s: HadamardNetV2(layer_sizes, seed=s)),
        ('ReLU', lambda s: StandardMLPV2(layer_sizes, 'relu', seed=s)),
        ('Sigmoid', lambda s: StandardMLPV2(layer_sizes, 'sigmoid', seed=s)),
    ]:
        print(f"    {name:12s}...", end='', flush=True)
        t0 = time.time()
        
        model = make_model(42)
        n = X_train.shape[0]
        for ep in range(epochs):
            idx = np.random.permutation(n)
            for start in range(0, n, 64):
                end = min(start+64, n)
                model.train_step(X_train[idx[start:end]], y_train[idx[start:end]], lr=lr)
        
        clean = accuracy(model, X_test, y_test)
        noisy_accs = {}
        for label, cfg in noise_configs.items():
            accs = [accuracy(model, X_test, y_test, noise_cfg=cfg) for _ in range(n_avg)]
            noisy_accs[label] = float(np.mean(accs))
        
        results[name] = {'clean': clean, 'noisy': noisy_accs}
        dt = time.time() - t0
        
        noise_str = ' | '.join(f'{k}={v:.3f}' for k, v in noisy_accs.items())
        print(f" clean={clean:.3f} | {noise_str} ({dt:.0f}s)")
    
    return results


def depth_test(X_train, y_train, X_test, y_test,
               depths, noise_cfg, hidden=32, epochs=500, lr=0.05, n_trials=3, n_avg=10):
    """Depth scaling with LayerNorm."""
    print(f"\n  Depth scaling test (with LayerNorm)")
    print(f"  {'─'*60}")
    
    results = {'depths': depths, 'hadamard': [], 'relu': []}
    
    for d in depths:
        print(f"    depth={d}...", end='', flush=True)
        sizes = [2] + [hidden]*d + [1]
        
        had_list, relu_list = [], []
        for trial in range(n_trials):
            seed = 42 + trial
            
            m_h = HadamardNetV2(sizes, seed=seed)
            m_r = StandardMLPV2(sizes, 'relu', seed=seed)
            
            n = X_train.shape[0]
            for ep in range(epochs):
                idx = np.random.permutation(n)
                for s in range(0, n, 64):
                    e = min(s+64, n)
                    m_h.train_step(X_train[idx[s:e]], y_train[idx[s:e]], lr=lr)
                    m_r.train_step(X_train[idx[s:e]], y_train[idx[s:e]], lr=lr)
            
            a_h = np.mean([accuracy(m_h, X_test, y_test, noise_cfg=noise_cfg) for _ in range(n_avg)])
            a_r = np.mean([accuracy(m_r, X_test, y_test, noise_cfg=noise_cfg) for _ in range(n_avg)])
            had_list.append(a_h)
            relu_list.append(a_r)
        
        results['hadamard'].append(float(np.mean(had_list)))
        results['relu'].append(float(np.mean(relu_list)))
        print(f" Had={np.mean(had_list):.3f} ReLU={np.mean(relu_list):.3f}")
    
    return results


# ================================================================
# Main
# ================================================================

if __name__ == '__main__':
    print("\n" + "="*70)
    print("  HADAMARD PHOTONIC NN v2: LayerNorm + Realistic Optical Noise")
    print("="*70)
    
    X_tr, y_tr = make_circles(800, 0.1, 42)
    X_te, y_te = make_circles(200, 0.1, 123)
    X_tr_s, y_tr_s = make_spiral(800, 0.1, 42)
    X_te_s, y_te_s = make_spiral(200, 0.1, 123)
    
    # Noise configurations
    noise_cfgs = {
        'gauss_0.3': {'gaussian': 0.3},
        'gauss_0.5': {'gaussian': 0.5},
        'shot_0.3': {'shot': 0.3},
        'phase_0.3': {'phase': 0.3},
        'combined': {'gaussian': 0.2, 'shot': 0.2, 'phase': 0.1, 'loss': 0.03},
    }
    
    # Exp 1: Circles with realistic noise
    r1 = run_experiment("Circles — Gaussian + Shot + Phase + Loss noise",
                        X_tr, y_tr, X_te, y_te,
                        [2, 32, 32, 1], noise_cfgs, epochs=500, lr=0.05)
    
    # Exp 2: Spiral (harder task, was failing before)
    r2 = run_experiment("Spiral — with LayerNorm + grad clipping (previously failing)",
                        X_tr_s, y_tr_s, X_te_s, y_te_s,
                        [2, 64, 64, 32, 1], noise_cfgs, epochs=800, lr=0.03)
    
    # Exp 3: Depth scaling (was collapsing at depth 6+)
    combined_noise = {'gaussian': 0.2, 'shot': 0.1, 'phase': 0.1}
    r3 = depth_test(X_tr, y_tr, X_te, y_te,
                    depths=[1, 2, 3, 4, 6, 8, 10],
                    noise_cfg=combined_noise, hidden=32, epochs=500, lr=0.05, n_trials=3)
    
    # Save
    all_res = {'circles': r1, 'spiral': r2, 'depth': r3}
    with open('photonic_nn_v2_results.json', 'w') as f:
        json.dump(all_res, f, indent=2)
    
    # Summary
    print(f"\n{'='*70}")
    print(f"  SUMMARY v2")
    print(f"{'='*70}")
    
    print(f"\n  Circles — Noise tolerance:")
    print(f"  {'Noise type':>15} | {'Hadamard':>10} | {'ReLU':>10} | {'Advantage':>10}")
    print(f"  {'-'*15}-+-{'-'*10}-+-{'-'*10}-+-{'-'*10}")
    for k in noise_cfgs:
        h = r1['Hadamard']['noisy'][k]
        r = r1['ReLU']['noisy'][k]
        print(f"  {k:>15} | {h:10.3f} | {r:10.3f} | {h-r:+10.3f}")
    
    print(f"\n  Spiral — Previously failing, now:")
    print(f"    Hadamard clean = {r2['Hadamard']['clean']:.3f}")
    print(f"    ReLU clean     = {r2['ReLU']['clean']:.3f}")
    
    print(f"\n  Depth scaling (combined noise):")
    print(f"  {'Depth':>6} | {'Hadamard':>10} | {'ReLU':>10}")
    print(f"  {'-'*6}-+-{'-'*10}-+-{'-'*10}")
    for i, d in enumerate(r3['depths']):
        h = r3['hadamard'][i]
        r = r3['relu'][i]
        marker = ' *' if h > r else ''
        print(f"  {d:6d} | {h:10.3f} | {r:10.3f}{marker}")
    
    print(f"\n  * = Hadamard wins")
    print(f"  Results saved to photonic_nn_v2_results.json")
    print(f"{'='*70}\n")
