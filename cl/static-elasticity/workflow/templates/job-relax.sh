#!/bin/bash
#SBATCH --partition=shared
#SBATCH -A col146
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=32
#SBATCH --export=ALL
#SBATCH -t 06:00:00

date

module purge
module load slurm
module load cpu
module load gcc/9.2.0
module load openmpi
module load quantum-espresso/6.7.0-openblas

### Run QE
mpirun --map-by core --mca btl_openib_if_include "mlx5_2:1" --mca btl openib,self,vader pw.x -input relax.in 1> relax.out 2> relax.err