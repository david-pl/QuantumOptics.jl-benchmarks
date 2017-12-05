import qutip as qt
import numpy as np
import benchmarkutils

name = "timeevolution_master_jaynescummings"

samples = 3
evals = 3
cutoffs = range(5, 81, 5)


def setup(N):
    options = qt.Options()
    options.atol = 1e-8
    options.rtol = 1e-6
    return options


def f(N, options):
    wa = 1
    wc = 1
    g = 2
    kappa = 0.5
    gamma = 0.1
    n_th = 0.75
    tspan = np.linspace(0, 1e3, 1e3 + 1)

    Ia = qt.qeye(2)
    Ic = qt.qeye(N)

    a = qt.destroy(N)
    at = qt.create(N)
    n = at * a

    sm = qt.sigmam()
    sp = qt.sigmap()
    sz = qt.sigmaz()

    H = wc*qt.tensor(n, Ia) + qt.tensor(Ic, wa/2.*sz) + g*(qt.tensor(at, sm) + qt.tensor(a, sp))
    c_ops = [
        qt.tensor(np.sqrt(kappa*(1+n_th)) * a, Ia),
        qt.tensor(np.sqrt(kappa*n_th) * at, Ia),
        qt.tensor(Ic, np.sqrt(gamma) * sm),
    ]

    psi0 = qt.tensor(qt.fock(N, 0), (qt.basis(2, 0) + qt.basis(2, 1)).unit())
    exp_n = qt.mesolve(H, psi0, tspan, c_ops, [qt.tensor(n, Ia)], options=options).expect[0]
    return exp_n


print("Benchmarking:", name)
print("Cutoff: ", end="", flush=True)
checks = {}
results = []
for N in cutoffs:
    print(N, "", end="", flush=True)
    options = setup(N)
    checks[N] = sum(f(N, options))
    t = benchmarkutils.run_benchmark(f, N, options, samples=samples, evals=evals)
    results.append({"N": 2*N, "t": t})
print()

benchmarkutils.check(name, checks)
benchmarkutils.save(name, results)
