using Express.EquationOfStateWorkflow.Recipes
using QuantumESPRESSOExpress

w = buildworkflow("eos.yaml");
run!(w)
