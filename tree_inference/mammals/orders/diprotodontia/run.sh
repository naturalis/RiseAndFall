#!/bin/bash
#
#SBATCH -J Diprotodontia
#SBATCH -t 100:00:00
#SBATCH -n 16
#SBATCH -o diprotodontia.out

module load openmpi/1.6.2-build1

# run the workflow
sh workflow.sh
