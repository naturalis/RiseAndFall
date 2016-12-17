The complete order Artiodactyla
--------------

This folder structure contains the results of the complete Artiodactyla phylogeny
performed by [@dimbots](http://github.com/dimbots) using the [SUPERSMART](http://github.com/naturalis/supersmart)
pipeline. Here now follows a brief explanation of the files and the subfolders:

File description:

- `artiodactyla_clade.nex` - The complete mammalian phylogeny in nexus format.
- `artiodactyla_bacbone.nex` - The backbone phylogeny of order Artiodactyla in nexus format.
- `species.tsv` - contains the results of the TNRS step, i.e. the maximum possible
  number of species that could be included in the analysis (because they get
  expanded out of the NCBI taxonomy). This will have both the ingroup as well as
  the outgroup in it. As such the final result will be fewer species than the 
  ones in this file.
- `species_coverage.txt` - a text file that contains the number of exemplars 
  from NCBI taxonomy, the number of species included in the phylogeny and the coverage 
  percentage.
- `species_coverage_COF.txt` - another text file that contains the number of exemplars from
  Catalogue Of Life taxonomy, the number of species included in the phylogeny and the 
  coverage percentage.
- `xxx_idmapped.nex`  - A tree that mapped between taxon names and NCBI taxonomy taxon IDs.
- `clade_xxx` - Each directory contains the phylogeny of an Artiodactyla suborder.
