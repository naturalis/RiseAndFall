#!/bin/bash
#
#SBATCH -J Pholidota
#SBATCH -t 02:00:00
#SBATCH -n 16
#SBATCH -o pholidota.out

module load openmpi/1.6.2-build1

# run the workflow
sh workflow.sh
