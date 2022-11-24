export PATH="${HOME}/.julia/bin:${PATH}"
export PATH="${HOME}/anaconda3/bin:${PATH}"
export PYTHON=""
export OMP_NUM_THREADS=1

alias jlupdate='julia -e "using Pkg; Pkg.update(); Pkg.gc()"'
