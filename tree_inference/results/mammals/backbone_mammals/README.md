Reconstruction of the backbone phylogeny 
--------------

This folder structure contains the results of the backbone phylogenetic inference
performed by [@dimbots](http://github.com/dimbots) using the [SUPERSMART](http://github.com/naturalis/supersmart)
pipeline. Here now follows a brief explanation of the files:

File description:

- `workflow.sh` - a shell script that has all the steps taken to arrive at the 
  final result in it. Useful to recover parameter settings and INGROUP and
  OUTGROUP selection.
- `species.tsv` - contains the results of the TNRS step, i.e. the maximum possible
  number of species that could be included in the analysis (because they get
  expanded out of the NCBI taxonomy). This will have both the ingroup as well as
  the outgroup in it. As such the final result will be fewer species than the 
  ones in this file.
- `fossils.tsv` - A file that contains the calibration points.
- `fossil_reference` - describes where the calibration points came from. 
- `names_backbone.tsv` - A file that contains all the species that were chosen for the reconstruction of the backbone phylogeny.
- `consensus.nex` - the backbone tree in nexus format.
- `consensus_pruned.nex` - the pruned backbone tree in nexus format. Specific species were pruned in order to achieve monophyly in the tree.
- `final_backbone_tree.png` - A visual representation of the backbone phylogeny.
- `markers-backbone.tsv` - A summary table with included markers used for the inference of the backbone phylogeny.
