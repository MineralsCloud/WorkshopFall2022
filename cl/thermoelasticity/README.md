# Hands on thermoelasticity calculation

In this workshop, we would like to

- Install the `cij` Python package
- Run the example distributed with the package.

## Theory

See

- Luo, C., Deng, X., Wang, W., Shukla, G., Wu, Z., & Wentzcovitch, R. M. (2021). cij: A Python code for quasiharmonic thermoelasticity. *Computer Physics Communications*, *267*, 108067. https://doi.org/10.1016/j.cpc.2021.108067
- Wu, Z., & Wentzcovitch, R. M. (2011). Quasiharmonic thermal elasticity of crystals: An analytical approach. *Physical Review B*, *83*(18), 184115. https://doi.org/10.1103/PhysRevB.83.184115

## Installation

### Install using `pip`

If you already have anaconda, just run:

```bash
python3 -m pip install -U cij
```

### Install using `conda`

Create the following environment file `cij.yaml`

```yaml
name: cij
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.10
  - matplotlib
  - scipy
  - pandas
  - yaml
  - pyyaml
  - numba
  - numpy
  - pip
  - pip:
    - git+https://github.com/MineralsCloud/qha.git@master
    - git+https://github.com/MineralsCloud/cij.git@dev

```

Then install using conda / micromamba

```bash
micromamba create -f cij.yaml

# with conda
# conda env create -f cij.yaml
```

To activate the environment, run the following

```bash
micromamba activate cij

# with conda
# conda activate cij
```

## Running the akimotoite example

```bash
git clone https://github.com/MineralsCloud/cij.git
cd cij/examples/akimotoite

# Perform thermoelasticity calculation
cij run settings.yaml
cij plot *.txt

# Perform static elasticity calculation
cij run-static input01 input02
```

