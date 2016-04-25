#!/bin/bash
#
#SBATCH -J Cetacea
#SBATCH -t 20:00:00
#SBATCH -n 16
#SBATCH -o cetacea.out

module load openmpi/1.6.2-build1

# run the workflow
sh workflow.sh
