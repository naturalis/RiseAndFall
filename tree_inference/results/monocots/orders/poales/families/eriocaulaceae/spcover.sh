#!/bin/bash

#This shell script calculates the number of exemplars from species.tsv
#and compare it to the total number of species from final_pruned.nex.
#Output is species_coverage.txt which represents the
#coverage percentage from the whole data sample.

#saves the number of species.tsv into nosp.txt
nl species.tsv | tail -1 | awk '{ print $1 }' > nosp.txt

#save the ouput of smrt-utils command into treeinfo.txt
smrt-utils treeinfo -t consensus.nex -l treeinfo.txt

#save the number of terminals into treesp.txt
cat treeinfo.txt | grep "Number of terminals" | grep -oE '[^ ]+$' > treesp.txt

#setting values to variables and calculating the percenatge of species coverage
x=$( cat nosp.txt )
y=$( cat treesp.txt )

p=$( bc <<< "scale=2; $y/$x" )

#save results to species_coverage.txt
P=$( bc <<< "$p*100" )

echo "data sample   : $x" > species_coverage.txt
echo "data included : $y" >> species_coverage.txt
echo "coverage      : $P%" >> species_coverage.txt

#delete intermediate files
rm nosp.txt treeinfo.txt treesp.txt




