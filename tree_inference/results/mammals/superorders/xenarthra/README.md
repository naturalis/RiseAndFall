Phylogenetic reconstruction of the superorder Xenarthra
--------------

This folder structure contains the results of the phylogenetic inference of the superorder Xenarthra
performed by [@dimbots](http://github.com/dimbots) using the [SUPERSMART](http://github.com/naturalis/supersmart)
pipeline. Here now follows a brief explanation of the files and the subfolders:

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
  lengths pruned out. If any pruning indeed took place, there will also be a file that contains the results before pruning.
- `final.nex` - contains the final tree before pruning. If there is not a final_pruned.nex that means that the prune command 
was not used. A comment file will also exist in the directory indicating that the prune command was not used.
- `mammalia_COF.txt` - A text file that contains mammals taxonomy 
  (Orders, Superfamilies, Families and number of species) extracted from Catalogue of Life.
- `markers-backbone.tsv` - A summary table with included markers used for the inference of the backbone phylogeny.



