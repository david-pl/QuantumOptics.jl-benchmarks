using QuantumOptics
using BenchmarkTools
include("benchmarkutils.jl")

using Random; Random.seed!(0)

name = "multiplication_dense_ket"

samples = 2
evals = 5
cutoffs = [50:50:500;]

function setup(N)
    b = GenericBasis(N)
    op1 = randoperator(b)
    psi = randstate(b)
    result = copy(psi)
    op1, psi, result
end

function f(op1, psi, result)
    QuantumOpticsBase.mul!(result,op1,psi)
end

println("Benchmarking: ", name)
print("Cutoff: ")
results = []
for N in cutoffs
    print(N, " ")
    op1, psi, result = setup(N)
    t = @belapsed f($op1, $psi, $result) samples=samples evals=evals
    push!(results, Dict("N"=>N, "t"=>t))
end
println()
benchmarkutils.save(name, results)
