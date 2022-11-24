# Install Julia version manager
curl -fsSL https://install.julialang.org | sh
# Install Julia
juliaup add release
juliaup default release

# Install Julia packages
julia setup.jl

FILE=~/.julia/bin/qe
if test -f "$FILE"; then
    echo "$FILE is installed."
fi

FILE=~/.julia/bin/xps
if test -f "$FILE"; then
    echo "$FILE is installed."
fi

# Configure Julia
mkdir -p ~/.julia/config
cp startup.jl ~/.julia/config
