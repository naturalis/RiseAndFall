Tree inference
--------------

This folder structure contains the results of the phylogenetic inference steps
performed by [@dimbots](http://github.com/dimbots) using the [SUPERSMART](http://github.com/naturalis/supersmart)
pipeline. Here now follows a brief explanation of the subfolders:


#### results

Contains trees (and other results). The subfolders below this level each contain
the summarized results of a SUPERSMART run. 

File description:

- `workflow.sh` - a shell script that has all the steps taken to arrive at the 
  final result in it. Useful to recover parameter settings and INGROUP and
  OUTGROUP selection.
- `scpcover.sh` - another shell script that used to calculate the percentage of species 
  coverage included in the phylogeny compared to NCBI and Catalogue Of Life (COF) taxonomy.
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
- `fossils.tsv` - contains the calibration points that were used.
- `fossil_reference` - describes where the calibration points came from.
- `final_pruned.nex` - contains the final tree, with any taxa causing negative branch
  lengths pruned out. If any pruning indeed took place, there will also be a file
  `final.nex` that contains the results before pruning.
- `mammalia_COF.txt` - A text file that contains mammals taxonomy 
  (Orders, Superfamilies, Families and number of species) extracted from Catalogue of Life.
- `monocots_COF.txt` - A text file that contains monocots taxonomy
  (Orders, Superfamilies, Families and number of species) extracted from Catalogue of Life.
- `xxxidmapped.nex`  - A tree that mapped between taxon names and NCBI taxonomy taxon IDs.
- `tree-comp-plot.R` - An R script used for tree comparison
- `Fossils_table.tsv`- A table representing the fossil data used in the calibration step.
- `names_backbone.tsv` - A file that contains all the species that were chosen for the reconstruction of the backbone phylogeny.
- `consensus.nex` - the backbone tree in nexus format.
- `consensus_pruned.nex` - the pruned backbone tree in nexus format. Specific species were pruned in order to achieve monophyly in the tree.
- `final_backbone_tree.png` - A visual representation of the backbone phylogeny.
- `markers-backbone.tsv` - A summary table with included markers used for the inference of the backbone phylogeny.

#### benchmark_trees

Contains in every subdirectory a published paper describing the phylogeny of the related
taxonomic group.These benchmark trees shall be compared with the results from SUPERSMART pipeline. 
