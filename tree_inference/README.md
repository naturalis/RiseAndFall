Tree inference
--------------

This folder structure contains the results of the phylogenetic inference steps
performed by [@dimbots](http://github.com/dimbots) using the [SUPERSMART](http://github.com/naturalis/supersmart)
pipeline. Here now follows a brief explanation of the subfolders:

#### ULTR

Contains trees that were artificially "ultrametricized" during the re-rooting
step of the backbone topology `smrt bbreroot -u [args]`. This process simply
adds additional length to the terminal branches until they all line up. As such,
this creates a distribution of branch lengths that, when reconciled with a
plausible substitution process implies a drastic slowdown along terminal branches.
When you subsequently try to recalibrate such a tree using fossils, the interior
nodes will be pulled towards the present to attempt to compensate for this rate
shift. As such, the final result will deviate a lot from the expectation and so
these results are not going to be used for subsequent analysis.

#### results

Contains trees (and other results) where this "ultrametricize" step was not applied.
Hence, these results are more useable. The subfolders below this level each contain
the summarized results of a SUPERSMART run. Specifically, they contain the following
files:

- `workflow.sh` - a shell script that has all the steps taken to arrive at the 
  final result in it. Useful to recover parameter settings and INGROUP and
  OUTGROUP selection.
- `species.tsv` - contains the results of the TNRS step, i.e. the maximum possible
  number of species that could be included in the analysis (because they get
  expanded out of the NCBI taxonomy). This will have both the ingroup as well as
  the outgroup in it. As such the final result will be fewer species than the 
  ones in this file.
- `fossils.tsv` - contains the calibration points that were used.
- `fossil_reference` - describes where the calibration points came from.
- `final_(.*).nex` - contains the final tree, with the outgroup pruned off.
