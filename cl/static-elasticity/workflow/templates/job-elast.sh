#!/bin/bash
#SBATCH --job-name="q-point"
## Change partition if needed
#SBATCH --partition=shared
#SBATCH -A col146
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16
#SBATCH --mem-per-cpu=1800M
#SBATCH --export=ALL
#SBATCH -t 00:40:00

date

module purge
module load slurm
module load cpu
module load gcc/9.2.0
module load openmpi
module load quantum-espresso/6.7.0-openblas

### Run QE
mpirun --map-by core --mca btl_openib_if_include "mlx5_2:1" --mca btl openib,self,vader pw.x -input elast.in -npool 4 1> elast.out 2> elast.err