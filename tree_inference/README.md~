Tree inference
--------------

This folder structure contains the results of the phylogenetic inference steps
performed by [@dimbots](http://github.com/dimbots) using the [SUPERSMART](http://github.com/naturalis/supersmart)
pipeline. Here now follows a brief explanation of the subfolders:


#### results

Contains trees (and other results) where this "ultrametricize" step was not applied.
Hence, these results are more useable. The subfolders below this level each contain
the summarized results of a SUPERSMART run. Specifically, they contain the following
files:

- `workflow.sh` - a shell script that has all the steps taken to arrive at the 
  final result in it. Useful to recover parameter settings and INGROUP and
  OUTGROUP selection.
- `scpcover.sh` - another shell script that used to calculate the percentage
   of species coverage included in the phylogeny compared to the whole data sample.
- `species.tsv` - contains the results of the TNRS step, i.e. the maximum possible
  number of species that could be included in the analysis (because they get
  expanded out of the NCBI taxonomy). This will have both the ingroup as well as
  the outgroup in it. As such the final result will be fewer species than the 
  ones in this file.
- `species_coverage.txt` - a text file that contains the number of exemplars 
   from species.tsv, the number of species included in the phylogeny and the overall 
   percentage.
- `fossils.tsv` - contains the calibration points that were used.
- `fossil_reference` - describes where the calibration points came from.
- `final_pruned.nex` - contains the final tree, with any taxa causing negative branch
  lengths pruned out. If any pruning indeed took place, there will also be a file
  `final.nex` that contains the results before pruning.

