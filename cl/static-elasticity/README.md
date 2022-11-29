# Static EoS & elasticity workflow



## Theory

We use the basic stress vs strain method to obtain the elastic coefficients.

See also

- da Silveira, P. R. C., Gunathilake, L., Holiday, A., Yuen, D. A., Valdez, M. N., & Wentzcovitch, R. M. (2013). Ab initio elasticity workflow in the VLab science gateway. *Proceedings of the Conference on Extreme Science and Engineering Discovery Environment Gateway to Discovery - XSEDE ’13*, 1. https://doi.org/10.1145/2484762.2484823
- Luo, C., Tromp, J., & Wentzcovitch, R. M. (2022). *Ab initio calculations of third-order elastic coefficients* (arXiv:2204.07608). arXiv. http://arxiv.org/abs/2204.07608

## Workflow structure

```
tree
.
├── Snakefile
├── config.yml 	<- workflow configuration file
├── init.qe			<- inital crystal structure
├── submit.sh		<- submit job in subscripts
├── scripts			<- workflow scripts
│   ├── check-done.sh
│   ├── check-ph-final.sh
│   ├── check-rlx-final.sh
│   ├── ...
│   └── vasp2qe.py
├── templates		<- template files
│   ├── elast.in
│   ├── job-conv.sh
│   ├── job-elast.sh
│   ├── job-relax.sh
│   ├── matdyn-qha.in
│   ├── ph.in
│   ├── q2r.in
│   ├── relax.in
│   ├── scf.in
│   └── scf_conv.in
└── workflows 	<- Snakemake workflow definition (don't worry) 
    ├── conv
    │   └── Snakefile
    ├── elast
    │   └── Snakefile
    ├── eos
    │   └── Snakefile
    └── ph
        └── Snakefile
```

See also

- [Snakemake — Snakemake 7.18.2.1 documentation](https://snakemake.readthedocs.io/en/stable/)

## Workflow Instruction

### Setup workflow environment

Create a `mphys.yaml`:

```yaml
name: mphys2
channels:
- conda-forge
- bioconda
dependencies:
- python=3.9
- setuptools
- ase
- pandas
- scipy
- pip
- jinja2
- tqdm
- snakemake
- numpy
- click
- matplotlib
- pip
```

Then run the following to create the environment:

```bash
module load anaconda3/2020.11
conda env create -f mphys.yaml
```

Then download the provided workflow files from `/home/chazeon/PROJECT/20221128-NaCl-LDA-uspp-template`.

### Get pseudopotentials

Here we use LDA ultrasoft potentials, download from [GBRV pseudopotentials](http://www.physics.rutgers.edu/gbrv/):

```bash
wget -qO- http://www.physics.rutgers.edu/gbrv/all_lda_UPF_v1.5.tar.gz | tar -xzv
```

See

- [GBRV pseudopotentials](http://www.physics.rutgers.edu/gbrv/)
- [Vanderbilt Ultra-Soft Pseudopotential Site](http://www.physics.rutgers.edu/~dhv/uspp/index.html)

### Prepare input

- [ ] Modify `init.qe`
- [ ] Modify `config.yml`
  - [ ] Modify `ntyp`, `nat`
  - [ ] Modify `volumes`
- [ ] Modify `template/relax.in`, `template/elast.in`
  - [ ] Set `pseudo_dir`
  - [ ] Set `nat` and `ntyp`
  - [ ] Modify `ATOMIC_SPECIES`
  - [ ] Modify `K_POINTS`, some convergence test might be necessary
  - [ ] Make sure other parameters are correct ...
- [ ] Modify `templates/job-relax.sh`, `templates/job-elast.sh`.

See also

- [pw.x: input description](https://www.quantum-espresso.org/Doc/INPUT_PW.html)

### Run workflow

#### Enter debug node

```bash
# enter interactive debug node
srun --partition=debug --pty --account=col146 --ntasks-per-node=2 --nodes=1 --mem=96G -t 00:30:00 --wait=0 --export=ALL /bin/bash

# enter the environment
module load anaconda3/2020.11
conda activate mphys
```

### Structure optimization / static equation of states

For NaCl, we change the `volume` under `eos` section in `config.yml`:

```yaml
eos:
  init_structure: "init.qe"
  volumes:  # volumes in angstrom
  - 32.0

  - 34.0

  - 36.0
  - 37.0
  - 38.0
  - 39.0
  - 40.0
  - 41.0
  - 42.0
  job_sh: "templates/job-relax.sh"
  template: "templates/relax.in"
```



```bash
# create input files
snakemake -j8 vc_target

# submit jobs
bash submit.sh relax

# collect results
snakemake -j8 eos
```

Check results in `PVE.dat`, `VxP.png`, `FxV.png`.

#### Structure optimization / static equation of states

For cubic system, we only need `e1` and `e4`, we change the `elast` section in `config.yml`:

```yaml
elast:
  strain_keys: [e1, e4] # <- change this
  strain_values: [0.0050, -0.0050]
  template: "templates/elast.in"
  job_sh: "templates/job-elast.sh"
```

Then run the following command, 

```bash
# create input files
snakemake -j8 elast_target

# go submit jobs
bash submit.sh elast
```

After jobs are finished, collect results:

```bash
# collect results
snakemake -j8 elast_dat
```

Check results in `elast.dat`.