"""Checks for the interior revision; run with numpy and scipy.
Numerical checks complement the stated proofs and do not re-estimate the data.
"""
import json
import numpy as np
from scipy.optimize import brentq, linprog
from scipy.sparse import coo_matrix


def cost_and_accounting_checks():
    rng = np.random.default_rng(20260905)
    max_error = 0.0
    for _ in range(80):
        a, lam, b = rng.uniform(.05, .65), rng.uniform(0, .3), rng.uniform(.1, 1)
        v = 10 ** rng.uniform(-5, 1)
        k = (lam * v + b) / (1 - a)
        r = rng.uniform(.1, 3)
        w, c = r * v, r * k
        D = M = direct_land = final_bill = 0.0
        for j in range(4):
            human_productivity = rng.lognormal(0, .7, 193)
            machine_productivity = rng.lognormal(0, 1, 193)
            machine_productivity[rng.random(193) < .09] = 0.0
            machine_cost = np.full(193, np.inf)
            np.divide(k, machine_productivity, out=machine_cost, where=machine_productivity > 0)
            human_cost = v / human_productivity
            use_human = human_cost <= machine_cost
            land = 0.0 if j == 0 else rng.uniform(.1, 2)
            L = np.mean(1 / human_productivity)
            price = land + np.mean(np.minimum(human_cost, machine_cost))
            assert land - 1e-13 <= price <= land + v * L + 1e-12
            if land:
                assert v / (land + v * L) - 1e-12 <= v / price <= v / land + 1e-12
            else:
                assert v / price >= 1 / L - 1e-12
            y = rng.uniform(.1, 5)
            D += y * np.sum(1 / human_productivity[use_human]) / 193
            M += y * np.sum(1 / machine_productivity[~use_human]) / 193
            direct_land += land * y
            final_bill += r * price * y
        X = M / (1 - a)
        hours = D + lam * X
        housing = rng.uniform(.2, 3)
        stock = housing + direct_land + b * X
        income = final_bill + r * housing
        error = abs(income - (w * hours + r * stock)) / income
        max_error = max(max_error, error)
        assert error < 5e-13
        assert abs(r * stock / income - 1 / (1 + v * hours / stock)) < 5e-13
    # Exact parity with nonconstant absolute human productivity.
    human = np.linspace(.2, 2.8, 321)
    relative = .35
    a, lam, b = .2, .1, .4
    v = b * relative / (1 - a - lam * relative)
    k = (lam * v + b) / (1 - a)
    for land in (0, .1, .5, 2):
        cost = land + np.mean(np.minimum(v / human, k / (human / relative)))
        assert abs(cost - (land + v * np.mean(1 / human))) < 1e-13
    return {'nonflat_assignments': 80, 'max_income_relative_error': max_error}

def equilibrium(N=4., T=10., h=1., a=.3, b=.4, lam=.05, intercept=.2, slope=.8):
    S = T - N * h
    A = S / N
    assert S > 0 and 1 - a - lam * (intercept + slope) > 0
    def gamma(x):
        return intercept + slope * x
    def J(x):
        return intercept * x + slope * x*x/2
    def v_at(x):
        return b * gamma(x) / (1 - a - lam * gamma(x))
    def ns(x):
        return N * min(np.log1p(v_at(x) / A), 1.)
    def nd(x):
        return S / b * (lam + (1 - a) * (1 - x) / J(x))
    assert ns(1) > lam * S / b
    x = brentq(lambda xx: nd(xx) - ns(xx), 1e-12, 1., xtol=1e-14)
    v = v_at(x)
    k = b / (1 - a - lam * gamma(x))
    X = S / b
    Y = (1 - a) * S / (b * J(x))
    direct_hours = Y * (1 - x)
    n = direct_hours + lam * X
    p = v * (1 - x) + k * J(x)
    residuals = [n - ns(x), p*Y - (S + v*n), (1-a)*X - Y*J(x), b*X - S]
    assert max(abs(z) for z in residuals) < 1e-10
    return dict(x=x, v=v, c_over_r=k, p_over_r=p, Y=Y, X=X, hours=n,
                final_task_hours=direct_hours, machine_sector_hours=lam*X,
                land_share=T/(T+v*n), max_market_residual=max(abs(z) for z in residuals))

def independent_production_lp(eq, task_count=2048):
    """Maximize output using hours and land, without imposing a task threshold."""
    n = task_count
    # Variables: output Y, n human-hour choices, n machine-service choices, X.
    Xcol = 2*n + 1
    xmid = (np.arange(n) + .5) / n
    gamma_m = 1 / (.2 + .8 * xmid)
    row, col, val = [], [], []
    for i in range(n):
        row.extend((i, i, i))
        col.extend((0, 1+i, 1+n+i))
        val.extend((1/n, -1., -gamma_m[i]))
    # Hours, land, and net machine-service availability are separate constraints.
    for i in range(n):
        row.extend((n, n+2))
        col.extend((1+i, 1+n+i))
        val.extend((1., 1.))
    row.extend((n, n+1, n+2))
    col.extend((Xcol, Xcol, Xcol))
    val.extend((.05, .4, -.7))
    A = coo_matrix((val, (row, col)), shape=(n+3, Xcol+1)).tocsr()
    budgets = np.r_[np.zeros(n), eq['hours'], 6., 0.]
    objective = np.zeros(Xcol+1)
    objective[0] = -1
    result = linprog(objective, A_ub=A, b_ub=budgets, bounds=(0, None), method='highs')
    assert result.success, result.message
    output = -result.fun
    error = abs(output / eq['Y'] - 1)
    labor_shadow = -result.ineqlin.marginals[n]
    land_shadow = -result.ineqlin.marginals[n+1]
    wage_rent_ratio = labor_shadow / land_shadow
    assert error < 2e-6
    assert abs(wage_rent_ratio - eq['v']) < 1e-3
    assert abs(np.sum(result.x[1:n+1]) + .05*result.x[Xcol] - eq['hours']) < 1e-8
    return {'tasks': n, 'output': output, 'relative_output_error': error,
            'dual_wage_rent_ratio': wage_rent_ratio}


def replacement_and_interior_formula_checks():
    rng=np.random.default_rng(20260921)
    max_derivative_error=0.
    for _ in range(100):
        a=rng.uniform(.05,.5)
        b=rng.uniform(.1,1.)
        lam=rng.uniform(.01,.15)
        g=rng.uniform(.2,1.5)
        delta=1-a-lam*g
        def value(ll,gg): return b*gg/(1-a-ll*gg)
        eps=1e-6
        dlam=(value(lam+eps,g)-value(lam-eps,g))/(2*eps)
        dg=(value(lam,g+eps)-value(lam,g-eps))/(2*eps)
        expected=[b*g*g/(delta*delta),b*(1-a)/(delta*delta)]
        relative=np.abs((np.array([dlam,dg])-expected)/expected)
        max_derivative_error=max(max_derivative_error,float(max(relative)))
        assert max(relative)<1e-7
    for _ in range(100):
        gstar=rng.uniform(.2,1.5)
        human=rng.lognormal(0,.5,257)
        relative=rng.lognormal(0,.8,257)
        relative[rng.random(257)<.1]=np.inf
        machine=human/relative
        wage=rng.uniform(.3,3.)
        rental=wage/gstar
        rent=rng.uniform(.2,2.)
        direct_land=rng.uniform(0,1.)
        machine_cost=np.full(257,np.inf)
        np.divide(rental,machine,out=machine_cost,where=machine>0)
        price=rent*direct_land+np.mean(np.minimum(wage/human,machine_cost))
        effective=np.mean(np.minimum(1,relative/gstar)/human)
        assert abs(price-(wage*effective+rent*direct_land))<1e-12
        assert abs(wage/price-1/(effective+direct_land*rent/wage))<1e-12
        assert effective<=np.mean(1/human)+1e-12
    # Rent redistribution retains wage income at every tax rate.
    ownership=np.array([1.,3.,6.])
    hours=np.array([1.,.6,.2])
    wage,rent=2.,1.5
    for tax in [0.,.4,1.]:
        dividend=tax*rent*ownership.sum()/len(hours)
        income=wage*hours+(1-tax)*rent*ownership+dividend
        assert abs(income.sum()-(wage*hours.sum()+rent*ownership.sum()))<1e-12
    return {'max_derivative_relative_error':max_derivative_error,'exact_interior_prices':100,
            'rent_redistribution_with_wages':'passed'}

if __name__=='__main__':
    example=equilibrium()
    sequence=[]
    for eta in (1.,.3,.1,.03,.01):
        e=equilibrium(lam=0.,intercept=eta,slope=eta)
        assert e['v']<=2*.4*eta/.7+1e-12
        sequence.append({'eta':eta,'v':e['v'],'hours':e['hours'],'land_share':e['land_share']})
    report={'interior_algebra':replacement_and_interior_formula_checks(),
            'bounds_and_accounting':cost_and_accounting_checks(),
            'interior_equilibrium':example,
            'independent_production':independent_production_lp(example),
            'nonflat_equilibrium_sequence':sequence}
    print(json.dumps(report,indent=2))
