#!/bin/bash

#SBATCH --job-name=spy_heat
#SBATCH --output=slurm.%N.%j.out
#SBATCH --error=slurm.%N.%j.err
#SBATCH --nodes=2
###SBATCH --ntasks-per-node=8
#SBATCH --time=10:00
#SBATCH --mem-per-cpu=2000
#SBATCH --partition=general

module load anaconda/3/2021.11
conda activate heat

#module load gcc/12
module load openmpi/4
module load netcdf-mpi/4.8.1
module load mpi4py/3.0.3
module load gpytorch/gpu-cuda-11.2/pytorch-1.9.0/1.5.1

SPYTMPDIR=/ptmp ~/develop/playground/heat_cluster/syncopy_heat_script.py