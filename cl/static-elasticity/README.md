# Static EoS & elasticity workflow

## Basics

See also

- Luo, C., Tromp, J., & Wentzcovitch, R. M. (2022). *Ab initio calculations of third-order elastic coefficients* (arXiv:2204.07608). arXiv. http://arxiv.org/abs/2204.07608

## Instruction

### Setup workflow environment

```
module load anaconda3/2020.11
conda env create -f mphys.yml
cp xxx .
tar -xvf .
```

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

See also

- [pw.x: input description](https://www.quantum-espresso.org/Doc/INPUT_PW.html)

### Run workflow

#### Enter debug node

```bash
# enter debug node
srun --partition=debug --pty --account=col146 --ntasks-per-node=2 --nodes=1 --mem=96G -t 00:30:00 --wait=0 --export=ALL /bin/zsh

# enter the environment
conda activate mphys
```

### Structure optimization / static equation of states

```bash

# create input files
snakemake -j8 vc_target

# submit jobs
cd relax
CWD=$(pwd) ; for j in $(find | grep job.sh) ; do ; cd $CWD/$(dirname $j) ; pwd ; sbatch job.sh ; done ; cd $CWD

# collect results
snakemake -j8 eos
```

Check results in `PVE.dat`, `VxP.png`, `FxV.png`.

#### Structure optimization / static equation of states

For cubic system, we only need

```yaml
elast:
  strain_keys: [e1, e4]
  strain_values: [0.0050, -0.0050]
  template: "templates/elast.in"
  job_sh: "templates/job-elast.sh"
```

Then run the following command, 

```bash
# enter debug node
srun --partition=debug --pty --account=col146 --ntasks-per-node=2 --nodes=1 --mem=96G -t 00:30:00 --wait=0 --export=ALL /bin/zsh

# enter the environment
conda activate mphys

# create input files
snakemake -j8 elast_target

# submit jobs
cd elast
CWD=$(pwd) ; for j in $(find | grep job.sh) ; do ; cd $CWD/$(dirname $j) ; pwd ; sbatch job.sh ; done ; cd $CWD
```

After jobs are finished, collect results:

```bash
# collect results
snakemake -j8 elast_dat
```

Check results in `elast.dat`.