# load all mammal occurences for Rise and Fall project

#load library

library(paleobioDB)

## 1. Download fossil occurrence data 

?pbdb_occurrences
# it returns a dataframe with occurrences of the selected taxon
## *** You should really check the taxonomy of the group of interest
## first to make sure it is correct***

## be carefull with synonyms.If there are two taxa which have the same name, the function will download the one with the most records. You can also use the taxonomic ID number to avoid this. 

occ<-pbdb_occurrences(base_name="Eupantotheria",ident="latest",limit="all",show=c("coords","attr","ident","phylo","ref"),order="earlyage.desc")
#ident=latest means that only the most recently published identification of each occurence is downloaded, in case there are multiple taxonomic identifications for the same record
#if you want to download the occurrences using the taxon ID number, use the option "base_id" instead of "base_name"

str(occ)
#you got 823 records or occurrences
#an overview of the data
head(cav)

#create a vector with the midage of each occurrence
cav$mag<-(cav$eag+cav$lag)/2

# you should be critical and evaluate that the raw data you download is correct before do any analysis.

#check for instances the genera names
levels(cav$gnl)

plot(cav$mag,cav$lat)
plot(cav$lng,cav$lat)
hist(cav$mag)

#once you have checked the data, you can start with your analyses, using the tools you prefer

## 2. Generate maps

?pbdb_map
# maps the fossil occurrences. Each point represents a fossil locality (collection)

pbdb_map(cav)
pbdb_map(cav, col.int="white",col.ocean="gray",xlim=c(-85,-35),ylim=c(-55,13))

?pbdb_map_occur
# maps the total number of occurrences per cell, regardless the taxonomic identity 
# => 10 occurrences of the same taxon = 10 occurrences of different taxa 
#can be use a measure of sampling effort

pbdb_map_occur(cav,res=5)
pbdb_map_occur(cav, col.int="white",col.ocean="gray",xlim=c(-85,-35),ylim=c(-55,13),res=1)

#you can also create a dataframe with the information
samp.effort<-pbdb_map_occur(cav,res=1)
samp.effort

?pbdb_map_richness
#maps the number of different taxa per cell

pbdb_map_richness(cav,res=5,rank="species")

pbdb_map_richness(cav,res=2,rank="species",col.int="white",col.ocean="gray",xlim=c(-85,-35),ylim=c(-55,13))


## 3. Exploring the fossil data

# the functions produce a dataframe wit the raw data and a plot (which can be turn off if desire)

?pbdb_richness
#explores richness patterns over time


#e.g. look the generic richness of caviomorphs during the Miocene
pbdb_richness(cav,rank="species",temporal_extent=c(5,23.03))

?pbdb_temp_range
#plots temporal ranges, of species, genera, family, etc.

pbdb_temp_range(cav,rank="genus")

pbdb_temp_range(cav,rank="genus")


?pbdb_orig_ext
#plots the first and last appearances of taxa over time

#e.g., first and las appearance datums of genera during the Neogene
#first appearance for each 2 Ma
pbdb_orig_ext(cav,rank="genus",temporal_extent=c(0,23.03),orig_ext=1,res=2)

#last appearance
pbdb_orig_ext(cav,rank="genus",temporal_extent=c(0,23.03),orig_ext=2,res=2)


# few additional functions available
?pbdb_subtaxa
#plot the number of subtaxa (e.g., genera, family)

pbdb_subtaxa(cav)
?pbdb_temporal_resolution
#to explore the temporal resolution of the fossil record

pbdb_temporal_resolution(cav)