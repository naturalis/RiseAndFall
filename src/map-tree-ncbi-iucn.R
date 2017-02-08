## This scripts takes the mammal tree and maps the names that
## are based on NCBI taxonomy identifiers to IUCN identifiers provided
## in the file 'ncbi-iucn-mapping.tsv' in the data directory
## If species cannot be mapped, they are marked as 'Delete' and are
## thus pruned from the tree

## files used in this analysis
mapping.file <- "../data/ncbi-iucn-mapping.tsv"
treefile <- '../tree_inference/results/mammals/mammals_phylogeny/mammals_phylogeny_corrected.nex'
outfile <- 'mammals_phylogeny_corrected_iucn.nex'

## read mapping table
mapping <- read.table(mapping.file, sep="\t", header=T)

## get species names that need to be pruned
idx <- which(mapping$Suggested_IUCN_Genus=='Delete' & mapping$Suggested_IUCN_Species=='Delete')
mapping.del <- mapping[idx,]
species.to.prune <- paste(mapping.del$NBCI_TAX_Genus, mapping.del$NBCI_TAX_Species, sep="_")

## prune tree
cmd <- paste("smrt-utils prunetree -t",
             treefile,
             "-f nexus -g",
             paste0(species.to.prune, collapse=','),
             "-o", outfile)
cat("Running command", cmd, "\n")
system(cmd)

## substitute names in pruned tree

for ( i in 1:nrow(mapping) ) {
    if ( ! i %in% idx ) {
        specname.ncbi <- paste(mapping$NBCI_TAX_Genus[i], mapping$NBCI_TAX_Species[i], sep='_')
        specname.iucn <- paste(mapping$Suggested_IUCN_Genus[i], mapping$Suggested_IUCN_Species[i], sep='_')
        if ( specname.ncbi != specname.iucn ) {
            cmd <- paste0("sed -i -- s/", specname.ncbi, "/", specname.iucn, "/g ", outfile)
            cat("Running command", cmd, "\n")
            system(cmd)
        }
    }
}




