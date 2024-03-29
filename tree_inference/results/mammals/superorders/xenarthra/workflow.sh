

#!/bin/bash

# this shell script demonstrates the steps of the SUPERSMART pipeline
# from start to finish INGROUP and OUTGROUP have to be filled in


INGROUP=Xenarthra
OUTGROUP=Manis

# perform taxonomic name reconciliation on an input list of names.
# creates a table of NCBI taxonomy identifiers (the taxa table).

if [ ! -e species.tsv ]; then
    smrt taxize -r Xenarthra,Manis -b
  fi 

# align all phylota clusters for the species in the taxa table.
# produces many aligned fasta files and a file listing these

 if [ ! -e aligned.txt ]; then
    smrt align
  fi

# assign orthology among the aligned clusters by reciprocal BLAST
export SUPERSMART_BACKBONE_MAX_DISTANCE="0.1"

if [ ! -e merged.txt ]; then
    smrt orthologize
  fi

# merge the orthologous clusters into a supermatrix with exemplar
# species, two per genus
export SUPERSMART_BACKBONE_MIN_COVERAGE="1"
export SUPERSMART_BACKBONE_MAX_COVERAGE="5"
 if [ ! -e supermatrix.phy ]; then
     smrt bbmerge
   fi

# run an exabayes search on the supermatrix, resulting in a backbone
# posterior sample
export SUPERSMART_EXABAYES_NUMGENS="100000"

if [ ! -e backbone.dnd ]; then
     smrt bbinfer --inferencetool=exabayes --cleanup
   fi

# root the backbone sample  on the outgroup
 if [ ! -e backbone-rerooted.dnd ]; then
    smrt bbreroot -g $OUTGROUP --smooth
  fi

# calibrate the re-rooted backbone tree using treePL
if [ ! -e chronogram.dnd ]; then
     smrt bbcalibrate --tree backbone-rerooted.dnd --supermatrix supermatrix.phy -f fossils.tsv
   fi

# build a consensus
if [ ! -e consensus.nex ]; then
      smrt consense -b 0.2 -i chronogram.dnd --prob 
   fi


# decompose the backbone tree into monophyletic clades. writes a directory
# with suitable alignments for each clade
export SUPERSMART_CLADE_MAX_DISTANCE="0.4"
export SUPERSMART_CLADE_MIN_DENSITY="0.2"
export SUPERSMART_CLADE_MIN_COVERAGE="1"
export SUPERSMART_CLADE_MAX_COVERAGE="10"
smrt bbdecompose -b

# merge all the alignments for each clades into a nexml file
smrt clademerge --enrich

# run *BEAST for each clade
smrt cladeinfer --ngens=15000000 --sfreq=1000 --lfreq=1000

# graft the *BEAST results on the backbone
smrt cladegraft


