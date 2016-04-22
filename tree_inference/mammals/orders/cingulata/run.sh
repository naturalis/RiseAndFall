#!/bin/bash
#
#SBATCH -J Cingulata
#SBATCH -t 00:20:00
#SBATCH -n 16
#SBATCH -o Cingulata.out

module load openmpi/1.6.2-build1

# run the workflow
sh workflow.sh
