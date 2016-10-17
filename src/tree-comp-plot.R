## This script plots two trees side-by-side and connects matching species.
## Both trees are pruned to the terminals that are present in both trees.
## The trees are then visualized using ape's 'cophyloplot'

require('ape')

## Caution, hard-coded paths.
## Change the file names to the trees to be plotted
supersmart.treefile <- '../tree_inference/results/mammals/backbone_mammals/consensus.nex'
benchmark.treefile <- '../tree_inference/benchmark_trees/external_data/faurby_mammal_tree/Fully_resolved_phylogeny-consensus.nex'

supersmart.pruned <- "supersmart-pruned.nex"
benchmark.pruned <- "benchmark-pruned.nex"

## prune and align tips with supersmart
cmd <- paste('smrt-utils aligntips -t', supersmart.treefile,  ' -u', benchmark.treefile,  '-f nexus -o', supersmart.pruned, '-q', benchmark.pruned,  '-p')
system(cmd)

## load trees
tree.supersmart <- read.nexus(supersmart.pruned)
tree.benchmark <- read.nexus(benchmark.pruned)

## make cophyloplot of benchmark and supersmart tree
assoc <- cbind(specs.intersect, specs.intersect)
pdf('tree-comp.pdf', width=20, height=40)
cophyloplot(tree.supersmart, tree.benchmark, cex=0.1, assoc=assoc, use.edge.length=T, space=300)
dev.off()
