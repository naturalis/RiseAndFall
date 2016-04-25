#!/bin/bash
#
#SBATCH -J Peramelemorphia
#SBATCH -t 60:00:00
#SBATCH -n 16
#SBATCH -o peramelemorphia.out

module load openmpi/1.6.2-build1

# run the workflow
sh workflow.sh
