# [Install Quantum ESPRESSO via Conda](https://notes.chazeon.com/notes/software/install-quantum-espresso-via-conda/)

Building QE requires properly setting up a Fortran compiler and a bunch of [prebuilt libraries](https://www.quantum-espresso.org/Doc/user_guide/node12.html) such as MPI/OpenMP, BLAS, LAPACK and FFTW, this can be cumbersome at time. On a HPC, it is not likely you will enjoy the privilege to be able to use a prebuilt Docker environment. Therefore, the easiest way to get QE up and running on a HPC is probably to use the prebuilt version from [conda-forge](https://anaconda.org/conda-forge/qe).

## Install miniconda

Install miniconda. Download from its [official release](https://docs.conda.io/en/latest/miniconda.html) page and execute the installation script, e.g.,

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
sh ./Miniconda3-latest-Linux-x86_64.sh
```

Disable its automatic activation if you prefer to activate the `(base)` environment manually.

```bash
conda config --set auto_activate_base false
```

## Creating the conda environment

Prepare the following `environment.yml` file:

```yaml
name: qe
channels:
  - conda-forge
  - defaults
dependencies:
  - qe
```

In your terminal, go to the directory that contains the `environment.yml` file, and construct the conda environment based on the `environment.yml` file to the `./env` subdirectory by

```bash
conda env create \
    -f environment.yml \    # Name of the environment YAML spec
    -p $(pwd)/env           # Location for the environment to be created
```

After the environment construction is finished, you can enter the conda environment by

```bash
conda activate $(pwd)/envs/qe
```

## Test run

As of 1/27/22, the QE on conda-forge is version 7.0. It has built-in MPI and OpenMP support but [does not comes with libxc support](https://github.com/conda-forge/qe-feedstock/blob/51ec09416cbe32799c1ffd0b2b9936612e23f289/recipe/build.sh#L28).

```bash
export OMP_NUM_THREADS=1
mpirun -np 32 pw.x --npool 4 -input $INPUT > $OUTPUT
```

gives the following output:

```txt
Program PWSCF v.7.0 starts on 27Jan2022 at 14: 2: 5

     This program is part of the open-source Quantum ESPRESSO suite
     for quantum simulation of materials; please cite
         "P. Giannozzi et al., J. Phys.:Condens. Matter 21 395502 (2009);
         "P. Giannozzi et al., J. Phys.:Condens. Matter 29 465901 (2017);
         "P. Giannozzi et al., J. Chem. Phys. 152 154105 (2020);
          URL http://www.quantum-espresso.org",
     in publications or presentations arising from this work. More details at
     http://www.quantum-espresso.org/quote

     Parallel version (MPI & OpenMP), running on      32 processor cores
     Number of MPI processes:                32
     Threads/MPI process:                     1

     MPI processes distributed on     1 nodes
     R & G space division:  proc/nbgrp/npool/nimage =      32
     156314 MiB available memory on the printing compute node when the environment starts
...
```

QE with this version run successfully with 32 MPI processors on [PSC Briges-2's regular memory (RM) node](https://www.psc.edu/resources/bridges-2/) (AMD EPYC 7742 64-core CPU), but does not works with 64 processes.
