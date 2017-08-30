#!/bin/bash

## In this script, we create comparison plots between a supersmart tree 
## and several benchmark trees

## locations of tree files
SUPERSMART_BACKBONE_TREE='../tree_inference/results/mammals/backbone_mammals/chronogram.nex'
SUPERSMART_TREE='../tree_inference/results/mammals/mammals_phylogeny/supersmart-tree.nex'
NATURE_TREE='../tree_inference/benchmark_trees/mammals/mammals_phylogeny/nature05634-best-tree.nex'
FAURBY_TREE='../tree_inference/benchmark_trees/external_data/faurby_mammal_tree/Fully_resolved_phylogeny-consensus.nex'

## generate the plots
Rscript tree-comp-plot.R $SUPERSMART_TREE $NATURE_TREE supersmart-vs-bininda-emons.pdf
Rscript tree-comp-plot.R $SUPERSMART_TREE $FAURBY_TREE supersmart-vs-faurby.pdf
