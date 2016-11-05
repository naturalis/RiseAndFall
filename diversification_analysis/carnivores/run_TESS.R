# Diversification rates using TESS
library(tools)
library(optparse)
library(TESS)

option_list <- list(

    make_option("--i", type="integer", default=200000,
        help=("Number of MCMC iterations to run [default %default]."),
        metavar="Iterations"),

    make_option("--rho", type="double", default=1,
        help="Sampling fraction [default %default]",
        metavar="rho"),
 
    make_option("--E_shifts", type="integer", default=2,
        help="Expected numebr of rate shifts [default %default]",
        metavar="E_shifts"),

    make_option("--E_me", type="integer", default=2,
        help="Expected number of mass extinctions [default %default]",
        metavar="E_me")

    )

parser_object <- OptionParser(usage = "Usage: %prog [Options] [TREE]\n\n [TREE] Tree file with full path \n", 
option_list=option_list, description="")
opt <- parse_args(parser_object, args = commandArgs(trailingOnly = TRUE), positional_arguments=TRUE)





setwd(dirname(basename(opt$args[1])))

tree <- read.nexus(opt$args[1]) 
times  <- as.numeric( branching.times(tree) )
#plot(tree,show.tip.label=FALSE)
#ltt.plot(tree,log="y")

# Sampling fraction
samplingFraction <- opt$options$rho


print( opt$options$i)

out_dir = sprintf("tess_empirical_hp_%s", file_path_sans_ext(basename(opt$args[1])))
out_file = sprintf("%s_RTT.pdf",  file_path_sans_ext(basename(opt$args[1])))

pdf(file=out_file,width=0.6*20, height=0.6*20)

# Estimated hyper-priors
tess.analysis(tree,
              empiricalHyperPriors       = TRUE,
              samplingProbability        = samplingFraction,
              numExpectedRateChanges     = opt$options$E_shifts,
              numExpectedMassExtinctions = opt$options$E_me,
              pMassExtinctionPriorShape1 = 1,
              pMassExtinctionPriorShape2 = 1,
              MAX_ITERATIONS             = opt$options$i,
              dir                        = out_dir)


# Plot output
library(TESS)
output <- tess.process.output(out_dir,
              numExpectedRateChanges = opt$options$E_shifts,
              numExpectedMassExtinctions = opt$options$E_me)

layout.mat <- matrix(1:6,nrow=3,ncol=2,byrow=TRUE)
layout(layout.mat)
tess.plot.output(output,las=2,
               fig.types = c("speciation rates",
                             "speciation shift times",
                             "extinction rates",
                             "extinction shift times",
                             "mass extinction Bayes factors",
                             "mass extinction times"))

n<- dev.off()
