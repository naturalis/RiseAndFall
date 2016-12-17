#!/bin/bash

#This shell script calculates the number of exemplars either from NCBI
#taxonomy or from Catalogue Of Life depending on users preference. Then, it
#compares the results with the total number of species from final_pruned.nex.
#Output is species_coverage.txt for NCBI and species_coverage_COF.txt for
#Catalogue Of Life.

#Files workflow.sh, species.tsv, final_pruned.nex, mammalia_COF.txt
#and monocots_COF.txt must exist in the working directory.

read -p "type (n) to compare with NCBI taxonomy or (c) for COF: " var

 if [ $var = n ]; then
#saves the total number of species.tsv into nosp.txt
nl species.tsv | tail -1 | awk '{ print $1 }' > nosp.txt

#save the ouput of smrt-utils command to treeinfo.txt
smrt-utils treeinfo -t final_pruned.nex -l treeinfo.txt

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
  fi

 if [ $var = c ]; then
#extract all taxonomic groups included in the phylogeny except from outgroup
cat workflow.sh | grep "smrt tax" | grep -oP "\w*[A-Z]+\w*" | sed -n '$!p' > species_sample.txt

mapfile -t array < species_sample.txt

#save the number of taxa in variable z
z=$( nl species_sample.txt | tail -1 | awk '{ print $1 }' )

     echo "searching for" $z "taxa"

x=$( cat species_sample.txt )

   for var in $x
     do

       cat mammalia_COF.txt | grep $var >> file1.txt
       cat monocots_COF.txt | grep $var >> file1.txt
     done

awk 'NF>1{print $NF}' file1.txt | awk '{s+=$1} END {print s}' > nosp.txt

#save the ouput of smrt-utils command to treeinfo.txt
smrt-utils treeinfo -t final_pruned.nex -l treeinfo.txt

#save the number of terminals into treesp.txt
cat treeinfo.txt | grep "Number of terminals" | grep -oE '[^ ]+$' > treesp.txt

#setting values to variables and calculating the percenatge of species coverage
x=$( cat nosp.txt )
y=$( cat treesp.txt )

p=$( bc <<< "scale=2; $y/$x" )

#save results to species_coverage.txt
P=$( bc <<< "$p*100" )

   echo "data sample   : $x" > species_coverage_COF.txt
   echo "data included : $y" >> species_coverage_COF.txt
   echo "coverage      : $P%" >> species_coverage_COF.txt

#delete intermadiate files
rm nosp.txt treesp.txt file1.txt species_sample.txt treeinfo.txt
fi


