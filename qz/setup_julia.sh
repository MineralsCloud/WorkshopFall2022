# Install Julia version manager
curl -fsSL https://install.julialang.org | sh
# Install Julia
juliaup add release
juliaup default release

# Install Julia packages
julia setup.jl

# Configure Julia
mkdir -p ~/.julia/config
cp startup.jl ~/.julia/config
