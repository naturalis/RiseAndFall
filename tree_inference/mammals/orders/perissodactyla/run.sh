#!/bin/bash
#
#SBATCH -J Perissodactyla
#SBATCH -t 04:00:00
#SBATCH -n 16
#SBATCH -o perissodactyla.out

module load openmpi/1.6.2-build1

# run the workflow
sh workflow.sh
