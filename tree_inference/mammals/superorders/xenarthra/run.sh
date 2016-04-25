#!/bin/bash
#
#SBATCH -J Xenarthra
#SBATCH -t 20:00:00
#SBATCH -n 16
#SBATCH -o xenarthra.out

module load openmpi/1.6.2-build1

# run the workflow
sh workflow.sh
