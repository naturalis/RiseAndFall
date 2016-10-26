## This script plots two trees side-by-side and connects matching species.
## Both trees are pruned to the terminals that are present in both trees.
## The trees are then visualized using ape's 'cophyloplot'.
## Provided trees must be in nexus format

## USAGE:
## Rscript tree-comp-plot.R [tree1] [tree2] [oufilename]

require('ape')

args <- commandArgs(trailingOnly=TRUE)

if (length(args) < 3) {
    stop("Need three arguments: [tree1] [tree2] [oufilename]")
}

treefile1 <- args[1]
treefile2 <- args[2]
plotfile <- args[3]

treefile1.pruned <- tempfile()
treefile2.pruned <- tempfile()

## Prune and align tips
## we use supersmart because the arrangement is much nicer than
## with ape's ladderize
cmd <- paste('smrt-utils aligntips -t', treefile1,  ' -u', treefile2,  '-f nexus -o', treefile1.pruned, '-q', treefile2.pruned,  '-p')
system(cmd)

## load pruned and sorted trees
tree1 <- read.nexus(treefile1.pruned)
tree2 <- read.nexus(treefile2.pruned)

## make cophyloplot of tree2 and tree1 tree
assoc <- cbind(tree1$tip.label, tree1$tip.label)
pdf(plotfile, width=20, height=40)
cophyloplot(tree1, tree2, cex=0.1, assoc=assoc, space=200, gap=10, use.edge.length=T)
dev.off()
