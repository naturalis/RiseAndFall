import os
import csv
import re
import numpy as np

now_fossil_file = "./data/NOW/NOW_all_mammal_fossils.csv"	#raw_input('Path to NOW fossil file: ')
pbdb_fossil_file = "./data/PBDB/downloaded_manually_from_webpage/pbdb_mammalia_all_res.csv"	#raw_input('Path to PBDB fossil file: ')
#gbif_fossil_file = "./data/GBIF/all_mammalia_occurences_gbif.csv" #raw_input('Path to GBIF fossil file: ')
iucn_file = './data/IUCN/IUCN_Mammal_Categories.csv'
iucn_pbdb_dictionary = './data/IUCN/paleobiodb_iucn_dictionary.csv'


workdir=os.getcwd()
outdir=os.path.join(workdir, 'merged_fossil_data_output')
if not os.path.exists(outdir):
	os.makedirs(outdir)
genus_list_out = os.path.join(outdir, 'genus_lists')
if not os.path.exists(genus_list_out):
	os.makedirs(genus_list_out)
occ_list_output = os.path.join(outdir,'occ_files_pyrate_formatted')
if not os.path.exists(occ_list_output):
	os.makedirs(occ_list_output)


def clean_name(name):
	# input: name in the format "genus species", returns cleaned species name as list in the format "[genus,species]"
	name = str.lower(name)
	name = name.replace(" n. sp.", "")
	name = name.replace(" n. gen.", "")
	name = name.replace(" aff.", "")
	name = name.replace(" cf.", "")
	name = name.replace(" ex gr.", "")
	name = name.replace(" sensu lato", "")
	name = name.replace(" informal", "")
	name = name.replace(" ?", "")
	name = name.replace(" \"", "")
	name = re.sub(" \(.*\)","",name)
	name = name.split(" ")
	if name[0] in ["","indet.","Indet.","indet","Indet","incertae sedis","gen.","gen"]:
		name[0] = "NA"
	if len(name) > 1:
		if name[1] in ["","indet.","Indet.","indet","Indet","incertae sedis"]:
			name[1] = "NA"
	return name


def get_iucn_dictionary(iucn_pbdb_dictionary):
	with open(iucn_pbdb_dictionary, 'r') as f:
		reader = csv.reader(f, delimiter=',')
		reader = list(reader)
		header = reader[0]
		body = reader[1:]
		pbdb_iucn_dict = {}
		all_names_dict = {}
		for line in body:
			paleobiodb_species = line[0]
			iucn_species = line[1]
			pbdb_iucn_dict.setdefault(paleobiodb_species,iucn_species)
	return pbdb_iucn_dict


def read_iucn_file(iucn_file):
	extant_species_iucn = []
	extinct_species_iucn = []
	with open(iucn_file, 'r') as f:
		reader = csv.reader(f, delimiter=',')
		reader = list(reader)
		header_iucn = reader[0]
		body = reader[1:]
		for line in body:
			name = line[6] + ' ' + line[7]
			if line[17] in ['EX','EW']:
				extinct_species_iucn.append(name)
			elif line[17] in ['DD','LC','NT','CR','EN','VU']:
				extant_species_iucn.append(name)
			else:
				print "Invalid status (%s) for" %line[17], name
	return extant_species_iucn, extinct_species_iucn



def summarize_pbdb(pbdb_fossil_file):
	with open(pbdb_fossil_file, 'r') as f:
		pbdb_order_dict = {}
		pbdb_fam_dict = {}
		pbdb_genus_id_dict = {}
		pbdb_id_min_max = {}
		pbdb_species_dict = {}
		reader = csv.reader(f, delimiter=',')
		reader = list(reader)
		header_index = ''
		for row in reader:
			if "occurrence_no" in row:
				header_index = reader.index(row)
		info = reader[0:header_index-1]
		header = reader[header_index]
		body = reader[header_index+1:]
		pbdb_records = len(body)
		for column in header:
			if column == 'occurrence_no':
				id_col = header.index(column)
			if column == 'accepted_name':
				name_col = header.index(column)
			if column == 'min_ma':
				min_age_col = header.index(column)
			if column == 'max_ma':
				max_age_col = header.index(column)
			if column == 'order':
				order_col = header.index(column)
			if column == 'family':
				family_col = header.index(column)
		undefined_ord = []
		undefined_fam = []
		for row in body:
			id = "pbdb_%s" %row[id_col]
			name = row[name_col]
			name = clean_name(name)
			min_age = float(row[min_age_col])
			max_age = float(row[max_age_col])
			mid_age = (min_age+max_age)/2
			order = str.lower(row[order_col])
			family = str.lower(row[family_col])

			# use the cleaned genus name
			genus = name[0]
			pbdb_genus_id_dict.setdefault(id,genus)

			pbdb_id_min_max.setdefault(id,[])
			pbdb_id_min_max[id].append([min_age,max_age])

			pbdb_species_dict.setdefault(id,name)

			# correct some common misspellings
			if order == "didelphimorpha":
				order = "didelphimorphia"
			elif order == "euliptyphla":
				order = "eulipotyphla"
			# take care of all unassigned records and join them under "NA"
			if order in ["","indet.","Indet.","indet","Indet","incertae sedis"]:
				undefined_ord.append(id)
			else:
				pbdb_order_dict.setdefault(order,[])
				pbdb_order_dict[order].append(id)

			if family in ["","indet.","Indet.","indet","Indet","incertae sedis"]:
				undefined_fam.append(id)	
			else:
				pbdb_fam_dict.setdefault(family,[])
				pbdb_fam_dict[family].append(id)

		pbdb_order_dict.setdefault("NA",[])
		for element in undefined_ord:
			pbdb_order_dict["NA"].append(element)
		pbdb_fam_dict.setdefault("NA",[])
		for element2 in undefined_fam:
			pbdb_fam_dict["NA"].append(element2)
		
	return pbdb_order_dict, pbdb_fam_dict, pbdb_genus_id_dict, pbdb_id_min_max, pbdb_species_dict


def summarize_now(now_fossil_file):
	with open(now_fossil_file, 'r') as f:
		now_order_dict = {}
		now_fam_dict = {}
		now_genus_id_dict = {}
		now_id_min_max = {}
		now_species_dict = {}
		reader = csv.reader(f, delimiter='\t')
		reader = list(reader)
		header_index = ''
		for row in reader:
			if "LIDNUM" in row:
				header_index = reader.index(row)
		info = reader[0:header_index-1]
		header = reader[header_index]
		body = reader[header_index+1:]
		now_records = len(body)
		for column in header:
			if column == 'SIDNUM':
				species_id_col = header.index(column)
			if column == 'LIDNUM':
				location_id_col = header.index(column)
			if column == 'MIN_AGE':
				min_age_col = header.index(column)
			if column == 'MAX_AGE':
				max_age_col = header.index(column)
			if column == 'ORDER':
				order_col = header.index(column)
			if column == 'FAMILY':
				family_col = header.index(column)
			if column == 'GENUS':
				genus_col = header.index(column)
			if column == 'SPECIES':
				epithet_col = header.index(column)
		undefined_ord = []
		undefined_fam = []
		for row in body:
			id = "now_%s_%s" %(row[location_id_col],row[species_id_col])
			genus = str.lower(row[genus_col])
			epithet = str.lower(row[epithet_col])
			name = "%s %s" %(genus,epithet)
			name = clean_name(name)
			min_age = float(row[min_age_col])
			max_age = float(row[max_age_col])
			mid_age = (min_age+max_age)/2
			order = str.lower(row[order_col])
			family = str.lower(row[family_col])
			# use the cleaned genus name
			genus = name[0]
			now_genus_id_dict.setdefault(id,genus)

			now_id_min_max.setdefault(id,[])
			now_id_min_max[id].append([min_age,max_age])

			now_species_dict.setdefault(id,name)

			# correct some common misspellings
			if order == "didelphimorpha":
				order = "didelphimorphia"
			elif order == "euliptyphla":
				order = "eulipotyphla"
			# take care of all unassigned records and join them under "NA"		
			if order in ["","indet.","Indet.","indet","Indet","incertae sedis"]:
				undefined_ord.append(id)
			else:
				now_order_dict.setdefault(order,[])
				now_order_dict[order].append(id)

			if family in ["","indet.","Indet.","indet","Indet","incertae sedis"]:
				undefined_fam.append(id)	
			else:
				now_fam_dict.setdefault(family,[])
				now_fam_dict[family].append(id)
		now_order_dict.setdefault("NA",[])
		for element in undefined_ord:
			now_order_dict["NA"].append(element)
		now_fam_dict.setdefault("NA",[])
		for element2 in undefined_fam:
			now_fam_dict["NA"].append(element2)

	return now_order_dict, now_fam_dict, now_genus_id_dict, now_id_min_max, now_species_dict

def print_no_occurences_now():
	# Get the number of fossil occurences for each order
	occ_count_pbdb = open("%s/occurences_per_order_now.txt" %outdir, "wb")
	occ_count_pbdb_log=csv.writer(occ_count_pbdb, delimiter='\t')
	# Iterate through sorted dictionary
	total_extracted_occurences_order = []
	for key in sorted(now_order_dict, key=lambda key: len(now_order_dict[key]), reverse=True):
		occ_count_pbdb_log.writerow([key,len(now_order_dict[key])])
		for value in now_order_dict[key]:
			total_extracted_occurences_order.append(value)
	# Get the number of fossil occurences for each family
	occ_count_pbdb_fam = open("%s/occurences_per_family_now.txt" %outdir, "wb")
	occ_count_pbdb_fam_log=csv.writer(occ_count_pbdb_fam, delimiter='\t')
	# Iterate through sorted dictionary
	total_extracted_occurences_family = []
	for key in sorted(now_fam_dict, key=lambda key: len(now_fam_dict[key]), reverse=True):
		occ_count_pbdb_fam_log.writerow([key,len(now_fam_dict[key])])
		for value in now_fam_dict[key]:
			total_extracted_occurences_family.append(value)


def print_no_occurences_pbdb():
	# Get the number of fossil occurences for each order
	occ_count_pbdb = open("%s/occurences_per_order_pbdb.txt" %outdir, "wb")
	occ_count_pbdb_log=csv.writer(occ_count_pbdb, delimiter='\t')
	# Iterate through sorted dictionary
	total_extracted_occurences_order = [] 
	for key in sorted(pbdb_order_dict, key=lambda key: len(pbdb_order_dict[key]), reverse=True):
		occ_count_pbdb_log.writerow([key,len(pbdb_order_dict[key])])
		for value in pbdb_order_dict[key]:
			total_extracted_occurences_order.append(value)

	# Get the number of fossil occurences for each family
	occ_count_pbdb_fam = open("%s/occurences_per_family_pbdb.txt" %outdir, "wb")
	occ_count_pbdb_fam_log=csv.writer(occ_count_pbdb_fam, delimiter='\t')
	# Iterate through sorted dictionary
	total_extracted_occurences_family = [] 
	for key in sorted(pbdb_fam_dict, key=lambda key: len(pbdb_fam_dict[key]), reverse=True):
		occ_count_pbdb_fam_log.writerow([key,len(pbdb_fam_dict[key])])
		for value in pbdb_fam_dict[key]:
			total_extracted_occurences_family.append(value)

# the values of both dicts have to be lists
def join_dictionaries(dict1,dict2):
	joined = dict1
	for key in dict2:
		if not key in dict1:
			joined.setdefault(key,dict2[key])
		else:
			for value in dict2[key]:
				joined[key].append(value)
	return joined

#########################################################################################


pbdb_iucn_dict = get_iucn_dictionary(iucn_pbdb_dictionary)
extant_species_iucn, extinct_species_iucn = read_iucn_file(iucn_file)

pbdb_order_dict, pbdb_fam_dict, pbdb_genus_id_dict, pbdb_id_min_max, pbdb_species_dict = summarize_pbdb(pbdb_fossil_file)
now_order_dict, now_fam_dict, now_genus_id_dict, now_id_min_max, now_species_dict = summarize_now(now_fossil_file)

print_no_occurences_pbdb()
print_no_occurences_now()




#extract all genera belonging to each order:
genus_dict = {}
for order in now_order_dict:
	genus_dict.setdefault(order,[])
# add all orders that are found in pbdb to genus_dict
for order in pbdb_order_dict:
	genus_dict.setdefault(order,[])
# iterate through complete dict
for order in genus_dict:
	if order in now_order_dict:
		for id in now_order_dict[order]:
			match_genus = now_genus_id_dict[id]
			# if this genus doesn't exist in the dictionary yet, add it. We also want no "NA" in that dict'
			if not match_genus in genus_dict[order]:
				if not match_genus == "NA":
					genus_dict[order].append(match_genus)
	if order in pbdb_order_dict:
		for id in pbdb_order_dict[order]:
			match_genus = pbdb_genus_id_dict[id]
			if not match_genus in genus_dict[order]:
				if not match_genus == "NA":
					genus_dict[order].append(match_genus)
	write_order_genus_list = open("%s/genus_lists/%s_genus_list.csv" %(outdir,order), "wb")
	for genera in sorted(genus_dict[order]):
		write_order_genus_list.write("%s\n" %genera)    #STILL NEED TO WORK ON NAME-CLEANING, there are several very similar names


joined_order_dict = join_dictionaries(now_order_dict,pbdb_order_dict)

#for order in joined_dict:
#	id_list = []
#	for id_item in joined_dict[order]:
#		id_tuple = id_item.split("_")
#		if id_tuple == "now":
#			print 
#

# checking if all id_s are unique
for key in now_id_min_max:
	if len(now_id_min_max[key])>1:
		print key, now_id_min_max[key]
for key in pbdb_id_min_max:
	if len(pbdb_id_min_max[key])>1:
		print key, pbdb_id_min_max[key]

joined_min_max_dict = join_dictionaries(now_id_min_max,pbdb_id_min_max)
joined_species_dict = join_dictionaries(now_species_dict, pbdb_species_dict)


for order in joined_order_dict:
	write_order_occ_file = open("%s/occ_files_pyrate_formatted/%s_fossil_occurrences.csv" %(outdir,order), "wb")
	for id in joined_order_dict[order]:
		source_database = id.split("_")[0]
		name = joined_species_dict[id]
		status = 'extinct'
		mint = joined_min_max_dict[id][0][0]
		maxt = joined_min_max_dict[id][0][1]
		if len(name) > 1 and not name[0] in ['NA','na'] and not name[1] in ['NA','na']:
			genus = name[0].title()
			epithet = name[1]
			species = '%s_%s' %(genus,epithet)
			# there was one strange case in the output with a '/' in the species name, followed by another epithet (for Felis silvestris)
			species = species.split('/')[0]
			spec2 = species.replace('_', ' ')
			if spec2 in extant_species_iucn:
				status = 'extant'
			elif spec2 in pbdb_iucn_dict:
				if pbdb_iucn_dict[spec2] in extant_species_iucn:
					status = 'extant'
				elif pbdb_iucn_dict[spec2] == 'extant':
					status = 'extant'
			order_occ_log = csv.writer(write_order_occ_file, delimiter='\t')
			order_occ_log.writerow([species, status, mint, maxt, source_database])
#for order in joined_dict:
#	id = chop off string_
#	if id in 
# make a list of ids for each order:
# first iterate through order dict and print all id's into list
# then iterate through each genus name that is assigned to the order and find the matching id's and add those to list (unless they already exist)