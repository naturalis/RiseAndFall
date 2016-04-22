#!/bin/bash
#
#SBATCH -J
#SBATCH -t 10:00:00
#SBATCH -n 16
#SBATCH -o .out

module load openmpi/1.6.2-build1

# run the workflow
sh workflow.sh
