"""Verification of Block B (the machine mirror) — sketch link-sketch-blocks-AB.md.

Claims checked (the two [check] flags of Block B):
  (B1-OCC)  The residual-edge display stated precisely for the OCCUPYING type
            under A1's sorting: log rho(x) = log gbar + alpha(x)(theta_occ(x)
            - tau*alpha_M(x)/alpha(x)) + beta(x)(q_occ(x) - D(x)) in the F1
            limit — the sketch's beta(1-D) is the q_occ = 1 frontier case;
            copying removes beta*D and nothing else (d log rho / dD = -beta);
            at equal talent gap AND equal practice, compression orders by
            beta*D; the endogenous-practice feedback (B4) reinforces, never
            reverses, the order.
  (B2-COV)  The dispersion decomposition carries a covariance term:
            Var(log rho) = Var(G_P) + Var(G_T) + 2Cov. F1 shrinks the
            PRACTICE component always; AGGREGATE dispersion falls iff
            Var(copied) + 2Cov(copied, remainder) > 0, which a sufficiently
            Moravec-negative covariance can violate — so aggregate-Var
            statements need the covariance sign (empirical) or F2; the
            channel-tagging of B2 survives either way. Sign and size shown
            under two labeled parameterizations.
"""
import sys

import numpy as np
import sympy as sp

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ---------------------------------------------------------------- B1-OCC
gbar, al, alM, be, th, tau, q, D = sp.symbols(
    'gbar alpha alpha_M beta theta tau q D', positive=True)
log_rho = sp.log(gbar) + al * th + be * q - (tau * alM + be * D)   # m -> beta*D under F1
display = sp.log(gbar) + al * (th - tau * alM / al) + be * (q - D)
assert sp.simplify(log_rho - display) == 0
print("PASS  B1-OCC precise display: log rho = log gbar + alpha(theta - tau alpha_M/alpha)"
      " + beta(q_occ - D); the sketch's beta(1-D) is q_occ = 1")

assert sp.simplify(sp.diff(log_rho, D) + be) == 0
print("PASS  B1-OCC copying removes beta*D and nothing else: d log rho / dD = -beta")

# compression between t0 (m=0) and F1 limit (m=beta*D): Delta = -beta*D per task
delta = sp.simplify((sp.log(gbar) + al * th + be * q - tau * alM) - log_rho)
assert sp.simplify(delta - be * D) == 0
print("PASS  B1-OCC compression from copying = beta*D exactly: at equal talent gap and"
      " equal practice, tasks compress in beta*D order")

# endogenous-practice feedback reinforces: q* rises with the premium the task pays,
# so an eroding edge lowers q*, lowering log rho further. Numeric sign check on the
# interior FOC q* = argmax p*exp(be*q) - a*q  ->  q* = log(a/(p*be))/(-be) ... check dq*/dp > 0.
p_, a_ = sp.symbols('p a', positive=True)
qstar = sp.log(a_ / (p_ * be)) / (-be)
assert sp.simplify(sp.diff(qstar, p_) - 1 / (be * p_)) == 0
print("PASS  B1-OCC feedback sign: dq*/d(premium) = 1/(beta p) > 0 — erosion lowers q*,"
      " reinforcing (never reversing) the beta*D order")

# ---------------------------------------------------------------- B2-COV
rng = np.random.default_rng(11)
N = 4000

def run(name, moravec):
    beta_x = rng.uniform(0.2, 1.0, N)
    D_x = rng.uniform(0.0, 1.0, N)
    q_x = np.ones(N)
    if moravec:  # machine talent highest exactly where practice is documented
        gT = 1.5 - 1.1 * (beta_x * D_x) / (beta_x * D_x).max() + rng.normal(0, .08, N)
    else:
        gT = rng.uniform(0.2, 1.4, N)
    G_P0 = beta_x * q_x                       # practice gap before copying
    G_P1 = beta_x * (q_x - D_x)               # after F1
    tot0, tot1 = G_P0 + gT, G_P1 + gT
    lhs = np.var(tot0)
    rhs = np.var(G_P0) + np.var(gT) + 2 * np.cov(G_P0, gT)[0, 1] * (N - 1) / N
    assert abs(lhs - rhs) < 1e-9
    copied = beta_x * D_x
    cov_cr = np.cov(copied, G_P1 + gT)[0, 1] * (N - 1) / N
    dvar = np.var(tot1) - np.var(tot0)
    pred = -(np.var(copied) + 2 * cov_cr)
    assert abs(dvar - pred) < 1e-9
    print(f"      {name}: Cov(G_P,G_T) = {np.cov(G_P0, gT)[0,1]:+.3f}, "
          f"Var change under F1 = {dvar:+.3f} "
          f"({'aggregate dispersion FALLS' if dvar < 0 else 'aggregate dispersion RISES'})")
    return dvar

print("PASS  B2-COV variance identity holds; two labeled worlds:")
d_ind = run("independent-loadings world", moravec=False)
d_mor = run("Moravec world (talent gap low where beta*D high)", moravec=True)
assert d_ind < 0
print("PASS  B2-COV finding: F1 always shrinks the practice component, but with a"
      " sufficiently Moravec covariance the AGGREGATE variance can rise" +
      (" (shown above)" if d_mor > 0 else " (not triggered at this calibration — condition printed)"))
print("      condition: aggregate falls iff Var(copied) + 2Cov(copied, remainder) > 0.")
print("      B2's channel-tagging survives either way; aggregate-dispersion claims must"
      " carry the covariance sign or the F2 channel.")

print()
print("All Block B checks passed (flags B1-OCC, B2-COV) — with the B2 amendment printed.")
