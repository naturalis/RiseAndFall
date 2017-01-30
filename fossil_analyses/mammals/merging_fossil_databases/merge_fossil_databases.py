import os
import csv
import re
import numpy as np

#import all fossil and IUCN files
now_fossil_file = "./data/NOW/NOW_all_mammal_fossils.csv"	#raw_input('Path to NOW fossil file: ')
pbdb_fossil_file = "./data/PBDB/downloaded_manually_from_webpage/pbdb_mammalia_species_res.csv"	#raw_input('Path to PBDB fossil file: ')
#gbif_fossil_file = "./data/GBIF/all_mammalia_occurences_gbif.csv" #raw_input('Path to GBIF fossil file: ')
iucn_file = './data/IUCN/IUCN_Mammal_Categories.csv'
iucn_pbdb_translation_file = './data/IUCN/paleobiodb_iucn_dictionary.csv'

#set the variables of the input data
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

# function to clean a species name from all pollution and return as list [genus,species]
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
		if name[1] in ["","indet.","Indet.","indet","Indet","incertae sedis","sp.","ssp.","sp"]:
			name[1] = "NA"
	return name

# read in the IUCN dictionary and store it as a dictionary with the PBDB species name as key and the equivalent IUCN species name as value
def get_iucn_dictionary(iucn_pbdb_translation_file,extant_list):
	print "reading PBDB-IUCN species name dictionary..."
	with open(iucn_pbdb_translation_file, 'r') as f:
		reader = csv.reader(f, delimiter=',')
		reader = list(reader)
		header = reader[0]
		body = reader[1:]
		iucn_pbdb_dict = {}
		for line in body:
			paleobiodb_species = line[0]
			iucn_species = line[1]
			iucn_pbdb_dict.setdefault(iucn_species,paleobiodb_species)
			if iucn_species == 'extant':
				extant_list.append(paleobiodb_species)
	return iucn_pbdb_dict, extant_list

# function to retrieve a list of extant and another of extinct mammals, based on the information in the IUCN redlist 
def read_iucn_file(iucn_file):
	print "reading IUCN category file..."
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



def clean_identification(id,ident):
	unidentified = []
	# correct some common misspellings
	if ident == "didelphimorpha":
		ident = "didelphimorphia"
	elif ident == "euliptyphla":
		ident = "eulipotyphla"
	# take care of all unassigned records and join them under "NA"
	if ident in ["","indet.","Indet.","indet","Indet","incertae sedis"]:
		unidentified.append(id)
	return unidentified, ident


# this function reads the PBDB fossil file and creates several dictionaries, which include lists of all ids belonging to each order and family, and dictionaries with the min and max time and the species name for each ID (record)
def summarize_pbdb(pbdb_fossil_file):
	print "reading PBDB database..."
	with open(pbdb_fossil_file, 'r') as f:
		#these lists serve the purpose to later run a clustering algorithm over them and see which groups of names are sufficiently similar
		pbdb_order_list = []
		pbdb_fam_list = []
		pbdb_genus_list = []
		pbdb_species_list = []

		pbdb_species_order_family_genus_epithet_ids_dict = {}
		pbdb_all_in_one_dict = {}
		pbdb_order_id_dict = {}
		pbdb_fam_id_dict = {}
		pbdb_id_min_max = {}
		pbdb_id_genus_species_dict = {}
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
			epithet = name[1]
			# determine if the taxon is identified to species level
			species_level = ''
			if name[1] != '' and name[1] != 'NA':
				species_level='TRUE'
			else:
				species_level='FALSE'

			# add all info into the all_in_one_dict
			capital_genus = 'NA'
			if name[0] != 'NA':
				capital_genus = name[0].capitalize()
			
			species2 = ' '.join([capital_genus,name[1]])
			pbdb_all_in_one_dict.setdefault(id,[])
			pbdb_all_in_one_dict[id].append(['pbdb',species2,min_age,max_age,genus,family,order,species_level])


			# output as requested by Soren
			if not [capital_genus,epithet] == ['NA','NA']:	
				if species2 not in pbdb_species_order_family_genus_epithet_ids_dict:
					pbdb_species_order_family_genus_epithet_ids_dict.setdefault(species2,[order,family,genus,epithet,[id]])
				elif species2 in pbdb_species_order_family_genus_epithet_ids_dict:
					pbdb_species_order_family_genus_epithet_ids_dict[species2][4].append(id)

			# setting up the min max age dict this way (list in a list) is done, so that in case there are ids that are non unique they will show by having more than one list item (more than one min,max-age pair)
			pbdb_id_min_max.setdefault(id,[])
			pbdb_id_min_max[id].append([min_age,max_age])

			#create another dict where each ID is assigned to the species name as a list [genus,species]
			pbdb_id_genus_species_dict.setdefault(id,name)

			undefined_ord, order = clean_identification(id,order)
			undefined_fam, family = clean_identification(id,family)
			if id not in undefined_ord:
				pbdb_order_id_dict.setdefault(order,[])
				pbdb_order_id_dict[order].append(id)
			if id not in undefined_fam:
				pbdb_fam_id_dict.setdefault(family,[])
				pbdb_fam_id_dict[family].append(id)

			# add new records to the lists
			species = '_'.join(name)
			if order not in pbdb_order_list:
				pbdb_order_list.append(order)
			if family not in pbdb_fam_list:
				pbdb_fam_list.append(family)
			if genus not in pbdb_genus_list:
				pbdb_genus_list.append(genus)
			if species not in pbdb_species_list:
				if name[0] != 'NA' and name[1] != 'NA':
					pbdb_species_list.append(species)

		#summarize all unidentified records under 'NA' in the dicitonaries
		pbdb_order_id_dict.setdefault("NA",[])
		for element in undefined_ord:
			pbdb_order_id_dict["NA"].append(element)
		pbdb_fam_id_dict.setdefault("NA",[])
		for element2 in undefined_fam:
			pbdb_fam_id_dict["NA"].append(element2)
		
	return pbdb_species_order_family_genus_epithet_ids_dict, pbdb_all_in_one_dict, pbdb_order_id_dict, pbdb_fam_id_dict, pbdb_id_genus_species_dict, pbdb_id_min_max, pbdb_order_list, pbdb_fam_list, pbdb_genus_list, pbdb_species_list



def summarize_now(now_fossil_file):
	print "reading NOW database..."
	with open(now_fossil_file, 'r') as f:
		
		#these lists serve the purpose to later run a clustering algorithm over them and see which groups of names are sufficiently similar
		now_order_list = []
		now_fam_list = []
		now_genus_list = []
		now_species_list = []

		now_all_in_one_dict = {}
		now_species_order_family_genus_epithet_ids_dict = {}
		now_order_id_dict = {}
		now_fam_id_dict = {}
		now_id_min_max = {}
		now_id_genus_species_dict = {}
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
			# in the now database the unique id for each occurrence derives fromt he combination of the species and the location id 
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
			epithet = name[1]
			# determine if the taxon is identified to species level
			species_level = ''
			if name[1] != '' and name[1] != 'NA':
				species_level='TRUE'
			else:
				species_level='FALSE'

			# add all info into the all_in_one_dict
			capital_genus = 'NA'
			if name[0] != 'NA':
				capital_genus = name[0].capitalize()
			
			species2 = ' '.join([capital_genus,name[1]])
			now_all_in_one_dict.setdefault(id,[])
			now_all_in_one_dict[id].append(['now',species2,min_age,max_age,genus,family,order,species_level])

			# output as requested by Soren
			if not [capital_genus,epithet] == ['NA','NA']:
				if species2 not in now_species_order_family_genus_epithet_ids_dict:
					now_species_order_family_genus_epithet_ids_dict.setdefault(species2,[order,family,genus,epithet,[id]])
				elif species2 in now_species_order_family_genus_epithet_ids_dict:
					now_species_order_family_genus_epithet_ids_dict[species2][4].append(id)

			# setting up the min max age dict this way (list in a list) is done, so that in case there are ids that are non unique they will show (this is tested for later) by having more than one list item (more than one min,max-age pair)
			now_id_min_max.setdefault(id,[])
			now_id_min_max[id].append([min_age,max_age])

			#create another dict where each ID is assigned to the species name as a list [genus,species]
			now_id_genus_species_dict.setdefault(id,name)

			undefined_ord, order = clean_identification(id,order)
			undefined_fam, family = clean_identification(id,family)
			if id not in undefined_ord:
				now_order_id_dict.setdefault(order,[])
				now_order_id_dict[order].append(id)
			if id not in undefined_fam:
				now_fam_id_dict.setdefault(family,[])
				now_fam_id_dict[family].append(id)

			# add new records to the lists
			species = '_'.join(name)
			if order not in now_order_list:
				now_order_list.append(order)
			if family not in now_fam_list:
				now_fam_list.append(family)
			if genus not in now_genus_list:
				now_genus_list.append(genus)
			if species not in now_species_list:
				if name[0] != 'NA' and name[1] != 'NA':
					now_species_list.append(species)

		#summarize all unidentified records under 'NA' in the dicitonaries
		now_order_id_dict.setdefault("NA",[])
		for element in undefined_ord:
			now_order_id_dict["NA"].append(element)
		now_fam_id_dict.setdefault("NA",[])
		for element2 in undefined_fam:
			now_fam_id_dict["NA"].append(element2)

	return now_species_order_family_genus_epithet_ids_dict, now_all_in_one_dict, now_order_id_dict, now_fam_id_dict, now_id_genus_species_dict, now_id_min_max, now_order_list, now_fam_list, now_genus_list, now_species_list

def join_lists(list1,list2):
	joined = list1[:]
	for element in list2:
		if element not in joined:
			joined.append(element)
	return joined

# Get the number of fossil occurences for each order
def print_no_occurences_pbdb():
	occ_count_pbdb = open("%s/occurences_per_order_pbdb.txt" %outdir, "wb")
	occ_count_pbdb_log=csv.writer(occ_count_pbdb, delimiter='\t')
	# Iterate through sorted dictionary
	total_extracted_occurences_order = [] 
	for key in sorted(pbdb_order_id_dict, key=lambda key: len(pbdb_order_id_dict[key]), reverse=True):
		occ_count_pbdb_log.writerow([key,len(pbdb_order_id_dict[key])])
		for value in pbdb_order_id_dict[key]:
			total_extracted_occurences_order.append(value)

	# Get the number of fossil occurences for each family
	occ_count_pbdb_fam = open("%s/occurences_per_family_pbdb.txt" %outdir, "wb")
	occ_count_pbdb_fam_log=csv.writer(occ_count_pbdb_fam, delimiter='\t')
	# Iterate through sorted dictionary
	total_extracted_occurences_family = [] 
	for key in sorted(pbdb_fam_id_dict, key=lambda key: len(pbdb_fam_id_dict[key]), reverse=True):
		occ_count_pbdb_fam_log.writerow([key,len(pbdb_fam_id_dict[key])])
		for value in pbdb_fam_id_dict[key]:
			total_extracted_occurences_family.append(value)

def print_no_occurences_now():
	# Get the number of fossil occurences for each order
	occ_count_pbdb = open("%s/occurences_per_order_now.txt" %outdir, "wb")
	occ_count_pbdb_log=csv.writer(occ_count_pbdb, delimiter='\t')
	# Iterate through sorted dictionary
	total_extracted_occurences_order = []
	for key in sorted(now_order_id_dict, key=lambda key: len(now_order_id_dict[key]), reverse=True):
		occ_count_pbdb_log.writerow([key,len(now_order_id_dict[key])])
		for value in now_order_id_dict[key]:
			total_extracted_occurences_order.append(value)

	# Get the number of fossil occurences for each family
	occ_count_pbdb_fam = open("%s/occurences_per_family_now.txt" %outdir, "wb")
	occ_count_pbdb_fam_log=csv.writer(occ_count_pbdb_fam, delimiter='\t')
	# Iterate through sorted dictionary
	total_extracted_occurences_family = []
	for key in sorted(now_fam_id_dict, key=lambda key: len(now_fam_id_dict[key]), reverse=True):
		occ_count_pbdb_fam_log.writerow([key,len(now_fam_id_dict[key])])
		for value in now_fam_id_dict[key]:
			total_extracted_occurences_family.append(value)

def check_unique_ids(dict):
	# checking if all id_s are unique, by assessing if there are multiple values in a dictionary where the keys are the unique occurrence ids
	for key in dict:
		if len(dict[key])>1:
			print 'ERROR: There are problems with the following fossil record (non unique ID):'
			print 'ID:', key.split("_")[1:]
			quit()

# summarize all genera in different dicts that are assigned to an order and output a list as textfile for each order
def write_order_genus_lists(*dicts):
	#create a dictionary with all genera belonging to each order (order:[list,of,genera])
	genus_dict = {}
	for dict in dicts:
		# add all orders that are found in the dict to genus_dict
		for order in dict:
			genus_dict.setdefault(order,[])
		# iterate through the order:genus dict
		for order in genus_dict:
			if order in dict:
				for id in dict[order]:
					match_genus = joined_id_genus_species_dicts[id][0]
					# if this genus doesn't exist in the dictionary yet, add it. We also want no "NA" in that dict'
					if not match_genus in genus_dict[order]:
						if not match_genus == "NA":
							genus_dict[order].append(match_genus)
			write_order_genus_list = open("%s/genus_lists/%s_genus_list.csv" %(outdir,order), "wb")
			for genera in sorted(genus_dict[order]):
				write_order_genus_list.write("%s\n" %genera)    #STILL NEED TO WORK ON NAME-CLEANING, there are several very similar names !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	return genus_dict

def join_dictionaries_with_unique_keys(*dicts):
	z = dicts[0].copy()
	for dict in dicts[1:]:
		z.update(dict)
	return z

# the values of all dicts have to be lists
def join_overlapping_dictionaries(*dicts):
	joined = dicts[0].copy()
	for dict in dicts:
		for key in dict:
			if not key in joined:
				joined.setdefault(key,dict[key])
			else:
				joined[key].extend(dict[key])
	return joined

#use the pbdb_iucn dict to find the equivalent name of each IUCN species in the PBDB database and append to the list based on IUCN taxonomy (to make sure to have all both versions of names in the list, which will be used to code pyrate output)
def complete_extant_list(iucn_list,name_translation_dict):
	extant_species = iucn_list[:]
	for species in iucn_list:
		if species in name_translation_dict:
			species_name_match = name_translation_dict[species]
			species_name_match = clean_name(species_name_match)
			# check if all names have genus and species epithet, as supposed to
			if len(species_name_match) == 2:
				species_name_match = " ".join([species_name_match[0].capitalize(),species_name_match[1]])
			else:
				print species_name_match
				exit()
			extant_species.append(species_name_match)
	return extant_species

# this function creates a pyrate formated fossil occurrence file for each key in a dict (can be order, family or genus level)
def create_pyrate_input_files(key_id,id_species,id_date,extant_list):
	print "writing pyrate files..."
	for key in key_id:
		write_key_occ_file = open("%s/occ_files_pyrate_formatted/%s_fossil_occurrences.csv" %(outdir,key), "wb")
		for id in key_id[key]:
			source_database = id.split("_")[0]
			name = id_species[id]
			status = 'extinct'
			mint = id_date[id][0][0]
			maxt = id_date[id][0][1]
			# This filter makes sure that we only export occurrences that are identified to species level
			if len(name) > 1 and not name[0] in ['NA','na'] and not name[1] in ['NA','na']:
				genus = name[0].title()
				epithet = name[1]
				species = '%s_%s' %(genus,epithet)
				# there was one strange case in the output with a '/' in the species name, followed by another epithet (for Felis silvestris)
				species = species.split('/')[0]
				spec2 = species.replace('_', ' ')
				if spec2 in extant_list:
					status = 'extant'
				elif spec2 in iucn_pbdb_dict:
					if iucn_pbdb_dict[spec2] in extant_species_iucn:
						status = 'extant'
					elif iucn_pbdb_dict[spec2] == 'extant':
						status = 'extant'
				key_occ_log = csv.writer(write_key_occ_file, delimiter='\t')
				key_occ_log.writerow([species, status, mint, maxt, source_database])


def output_merged_database():
	merged_database = open("%s/merged_databases.csv" %outdir, "wb")
	merged_database_log=csv.writer(merged_database, delimiter='\t')
	merged_database_log.writerow(['id','source','species','min_age','max_age','genus','family','order','identified_to_species','extant'])
	for id in joined_all_in_one_dict:
		proper_id = id.replace("pbdb_", "")
		proper_id = proper_id.replace("now_", "")
		source = joined_all_in_one_dict[id][0][0]
		species = joined_all_in_one_dict[id][0][1]
		min_age = joined_all_in_one_dict[id][0][2]
		max_age = joined_all_in_one_dict[id][0][3]
		genus = joined_all_in_one_dict[id][0][4]
		family = joined_all_in_one_dict[id][0][5]
		order = joined_all_in_one_dict[id][0][6]
		species_ident = joined_all_in_one_dict[id][0][7]
		extant = 'FALSE'
		
		if species in extant_species:
			extant = 'TRUE'
		merged_database_log.writerow([proper_id,source,species,min_age,max_age,genus,family,order,species_ident,extant])

#########################################################################################

#return all data dictionaries and check if all IDs are unique
pbdb_sorens_dict, pbdb_all_in_one_dict, pbdb_order_id_dict, pbdb_fam_id_dict, pbdb_id_genus_species_dict, pbdb_id_min_max, pbdb_order_list, pbdb_fam_list, pbdb_genus_list, pbdb_species_list = summarize_pbdb(pbdb_fossil_file)
check_unique_ids(pbdb_id_min_max)
now_sorens_dict, now_all_in_one_dict, now_order_id_dict, now_fam_id_dict, now_id_genus_species_dict, now_id_min_max, now_order_list, now_fam_list, now_genus_list, now_species_list = summarize_now(now_fossil_file)
check_unique_ids(now_id_min_max)

joined_order_list = join_lists(pbdb_order_list,now_order_list)
joined_fam_list = join_lists(pbdb_fam_list,now_fam_list)
joined_genus_list = join_lists(pbdb_genus_list,now_genus_list)
joined_species_list = join_lists(pbdb_species_list,now_species_list)

# join some of the dicts with unique ids
joined_id_genus_species_dicts = join_dictionaries_with_unique_keys(pbdb_id_genus_species_dict,now_id_genus_species_dict)
joined_all_in_one_dict = join_dictionaries_with_unique_keys(pbdb_all_in_one_dict,now_all_in_one_dict)

#get two lists, one with all extant species and one with all recently extinct species (IUCN taxonomy)
extant_species_iucn, extinct_species_iucn = read_iucn_file(iucn_file)
#make a dictionary with the names from iucn and the equivalent name in pbdb for name_cleaning (manual) and add those records to the extant_list that are coded as extant in the pbdb_iucn_translation_file
iucn_pbdb_dict,extant_species_iucn = get_iucn_dictionary(iucn_pbdb_translation_file,extant_species_iucn)
#complete the list with the pbdb name equivalents
extant_species = complete_extant_list(extant_species_iucn,iucn_pbdb_dict)

# BY THIS POINT WE SHOULD ALREADY HAVE CLEANED NAMES FOR ALL TAXA !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# print number of occurrences for each order and family, separately for the two databases
print_no_occurences_pbdb()
print_no_occurences_now()

# create a list text file for each order, containing all genera assigned to that order from all databases
order_genus_dict = write_order_genus_lists(pbdb_order_id_dict,now_order_id_dict)

# join some of the dicts from NOW and PBDB dicts
joined_order_id_dicts = join_overlapping_dictionaries(now_order_id_dict,pbdb_order_id_dict)
joined_id_genus_species_dict = join_overlapping_dictionaries(now_id_genus_species_dict, pbdb_id_genus_species_dict)
joined_id_min_max_dict = join_overlapping_dictionaries(now_id_min_max,pbdb_id_min_max)

# create pyrate input files
create_pyrate_input_files(joined_order_id_dicts,joined_id_genus_species_dict,joined_id_min_max_dict,extant_species)

# write an output file that joins the input databases
output_merged_database()

final_sorens_dict = {}
for species in pbdb_sorens_dict:
	pbdb_order = pbdb_sorens_dict[species][0]
	pbdb_fam = pbdb_sorens_dict[species][1]
	genus = pbdb_sorens_dict[species][2]
	epithet = pbdb_sorens_dict[species][3]
	pbdb_count = len(pbdb_sorens_dict[species][4])
	if species in now_sorens_dict:
		now_order = now_sorens_dict[species][0]
		now_fam = now_sorens_dict[species][1]
		now_count = len(now_sorens_dict[species][4])
		final_sorens_dict.setdefault(species,[pbdb_order,now_order,pbdb_fam,now_fam,genus,epithet,pbdb_count,now_count])
	else:
		final_sorens_dict.setdefault(species,[pbdb_order,'NA',pbdb_fam,'NA',genus,epithet,pbdb_count,'NA'])


for species in now_sorens_dict:
	epithet = species.split(" ")[1]
	now_order = now_sorens_dict[species][0]
	now_fam = now_sorens_dict[species][1]
	genus = now_sorens_dict[species][2]
	epithet = now_sorens_dict[species][3]
	now_count = len(now_sorens_dict[species][4])
	if not species in final_sorens_dict:
		final_sorens_dict.setdefault(species,['NA',now_order,'NA',now_fam,genus,epithet,'NA',now_count])


sorens_output = open("%s/output_for_soren.csv" %outdir, "wb")
sorens_output_log=csv.writer(sorens_output, delimiter='\t')
sorens_output_log.writerow(['species','order_pbdb','order_now','fam_pbdb','fam_now','genus','species','occ_pbdb','occ_now'])
for species in final_sorens_dict:
	a = final_sorens_dict[species][0]
	if a == '':
		a = 'NA'
	b = final_sorens_dict[species][1]
	if b == '':
		b = 'NA'
	c = final_sorens_dict[species][2]
	if c == '':
		c = 'NA'	
	d = final_sorens_dict[species][3]
	if d == '':
		d = 'NA'
	e = final_sorens_dict[species][4]
	if e == '':
		e = 'NA'
	f = final_sorens_dict[species][5]
	if f == '':
		f = 'NA'
	g = final_sorens_dict[species][6]
	if g == '':
		g = 'NA'
	h = final_sorens_dict[species][7]
	if h == '':
		h = 'NA'
	sorens_output_log.writerow([species,a,b,c,d,e,f,g,h])