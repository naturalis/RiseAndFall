import os
import csv
import re
import numpy as np

upper_cut = float(23.34) 	#max age allowed
lower_cut = float(0.10)		#min age allowed

now_fossil_file = "./data/NOW/NOW_all_mammal_fossils.csv"	#raw_input('Path to NOW fossil file: ')
pbdb_fossil_file = "./data/PBDB/downloaded_manually_from_webpage/pbdb_mammalia_all_res.csv"	#raw_input('Path to PBDB fossil file: ')
#gbif_fossil_file = "./data/GBIF/all_mammalia_occurences_gbif.csv" #raw_input('Path to GBIF fossil file: ')

workdir=os.getcwd()
outdir=os.path.join(workdir, 'merged_fossil_data_output')
if not os.path.exists(outdir):
	os.makedirs(outdir)


def clean_name(name):
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
	return name



# *********** PBDB database ***********

with open(pbdb_fossil_file, 'r') as f:
	order_dict = {}
	fam_dict = {}
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
		id = row[id_col]
		name = row[name_col]
		name = clean_name(name)
		min_age = float(row[min_age_col])
		max_age = float(row[max_age_col])
		mid_age = (min_age+max_age)/2
		order = str.lower(row[order_col])
		family = str.lower(row[family_col])

		# correct some common misspellings
		if order == "didelphimorpha":
			order = "didelphimorphia"
		elif order == "euliptyphla":
			order = "eulipotyphla"
		# take care of all unassigned records and join them under "NA"
		if order in ["","indet.","Indet.","indet","Indet","incertae sedis"]:
			undefined_ord.append(id)
		else:
			order_dict.setdefault(order,[])
			order_dict[order].append(id)

		if family in ["","indet.","Indet.","indet","Indet","incertae sedis"]:
			undefined_fam.append(id)	
		else:
			fam_dict.setdefault(family,[])
			fam_dict[family].append(id)
	order_dict.setdefault("NA",[])
	for element in undefined_ord:
		order_dict["NA"].append(element)
	fam_dict.setdefault("NA",[])
	for element2 in undefined_fam:
		fam_dict["NA"].append(element2)
	
	# Get the number of fossil occurences for each order
	occ_count_pbdb = open("%s/occurences_per_order_pbdb.txt" %outdir, "wb")
	occ_count_pbdb_log=csv.writer(occ_count_pbdb, delimiter='\t')
	# Iterate through sorted dictionary
	total_extracted_occurences_order = [] 
	for key in sorted(order_dict, key=lambda key: len(order_dict[key]), reverse=True):
		occ_count_pbdb_log.writerow([key,len(order_dict[key])])
		for value in order_dict[key]:
			total_extracted_occurences_order.append(value)

	# Get the number of fossil occurences for each family
	occ_count_pbdb_fam = open("%s/occurences_per_family_pbdb.txt" %outdir, "wb")
	occ_count_pbdb_fam_log=csv.writer(occ_count_pbdb_fam, delimiter='\t')
	# Iterate through sorted dictionary
	total_extracted_occurences_family = [] 
	for key in sorted(fam_dict, key=lambda key: len(fam_dict[key]), reverse=True):
		occ_count_pbdb_fam_log.writerow([key,len(fam_dict[key])])
		for value in fam_dict[key]:
			total_extracted_occurences_family.append(value)
	
	print "Total number of PBDB records to start with:", pbdb_records		
	print "Total number of PBDB records in order output:", len(total_extracted_occurences_order)
	print "Total number of PBDB records in family output:", len(total_extracted_occurences_family) 


# *********** NOW database ***********

with open(now_fossil_file, 'r') as f:
	order_dict = {}
	fam_dict = {}
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
			id_col = header.index(column)
		if column == 'NAME':
			name_col = header.index(column)
		if column == 'MIN_AGE':
			min_age_col = header.index(column)
		if column == 'MAX_AGE':
			max_age_col = header.index(column)
		if column == 'ORDER':
			order_col = header.index(column)
		if column == 'FAMILY':
			family_col = header.index(column)

	undefined_ord = []
	undefined_fam = []
	for row in body:
		id = row[id_col]
		name = row[name_col]
		name = clean_name(name)
		min_age = float(row[min_age_col])
		max_age = float(row[max_age_col])
		mid_age = (min_age+max_age)/2
		order = str.lower(row[order_col])
		family = str.lower(row[family_col])

		# correct some common misspellings
		if order == "didelphimorpha":
			order = "didelphimorphia"
		elif order == "euliptyphla":
			order = "eulipotyphla"
		# take care of all unassigned records and join them under "NA"		
		if order in ["","indet.","Indet.","indet","Indet","incertae sedis"]:
			undefined_ord.append(id)
		else:
			order_dict.setdefault(order,[])
			order_dict[order].append(id)

		if family in ["","indet.","Indet.","indet","Indet","incertae sedis"]:
			undefined_fam.append(id)	
		else:
			fam_dict.setdefault(family,[])
			fam_dict[family].append(id)
	order_dict.setdefault("NA",[])
	for element in undefined_ord:
		order_dict["NA"].append(element)
	fam_dict.setdefault("NA",[])
	for element2 in undefined_fam:
		fam_dict["NA"].append(element2)
	
	#extract all genera belonging to each order:
	for order in order_dict:
		print order
		id_list = []
		genus_list = []
		for id in order_dict[order]:
			id_list.append(id)

		for row in body:
			if row[id_col] in id_list:
				print row






	# Get the number of fossil occurences for each order
	occ_count_pbdb = open("%s/occurences_per_order_now.txt" %outdir, "wb")
	occ_count_pbdb_log=csv.writer(occ_count_pbdb, delimiter='\t')
	# Iterate through sorted dictionary
	total_extracted_occurences_order = []
	for key in sorted(order_dict, key=lambda key: len(order_dict[key]), reverse=True):
		occ_count_pbdb_log.writerow([key,len(order_dict[key])])
		for value in order_dict[key]:
			total_extracted_occurences_order.append(value)

	# Get the number of fossil occurences for each family
	occ_count_pbdb_fam = open("%s/occurences_per_family_now.txt" %outdir, "wb")
	occ_count_pbdb_fam_log=csv.writer(occ_count_pbdb_fam, delimiter='\t')
	# Iterate through sorted dictionary
	total_extracted_occurences_family = []
	for key in sorted(fam_dict, key=lambda key: len(fam_dict[key]), reverse=True):
		occ_count_pbdb_fam_log.writerow([key,len(fam_dict[key])])
		for value in fam_dict[key]:
			total_extracted_occurences_family.append(value)


	print "Total number of NOW records to start with:", now_records	
	print "Total number of NOW records in order output:", len(total_extracted_occurences_order)
	print "Total number of NOW records in family output:", len(total_extracted_occurences_family) 


#		
#with open(now_fossil_file, 'r') as f:
#	fossil_dict = {}
#	accepted_species = []
#	reader = csv.reader(f, delimiter='\t')
#	reader = list(reader)
#	header_index = ''
#	for row in reader:
#		if "SIDNUM" in row:
#			header_index = reader.index(row)
#	info = reader[0:header_index-1]
#	header = reader[header_index]
#	body = reader[header_index+1:]
#	for column in header:
#		if column == 'GENUS':
#			genus_col = header.index(column)
#		if column == 'SPECIES':
#			species_col = header.index(column)		
#		if column == 'MIN_AGE':
#			min_age_col = header.index(column)
#		if column == 'MAX_AGE':
#			max_age_col = header.index(column)
#		if column == 'SIDNUM':
#			id_col = header.index(column)
#		if column == 'ORDER':
#			order_col = header.index(column)
#
#	for row in body:
#		if row[genus_col] == "indet." or row[species_col] == "indet." or row[species_col] == "sp.":
#			continue
#		name = row[genus_col]+' '+row[species_col]
#		name = re.sub(" var.*","",name)
#		if len(name.split(" ")) < 2:
#			continue
#		name = clean_name(name)
#		min_age = float(row[min_age_col])
#		max_age = float(row[max_age_col])
#		mid_age = (min_age+max_age)/2
#		fossil_dict.setdefault(name,[])
#		fossil_dict[name].append(mid_age)
#
#	for element in fossil_dict:
#		species_name = element
#		species_min_age = min(fossil_dict[element])
#		species_max_age = max(fossil_dict[element])
#		column1 = 0
#		column2 = 0
#		if species_max_age > upper_cut:
#			#print species_name, "occurred before", upper_cut, "with oldest occurence at", species_max_age
#			column1 = 1
#		if species_min_age < lower_cut:
#			column2 = 1
#		if not species_min_age > upper_cut or species_max_age < lower_cut:
#			accepted_species.append(species_name)
#
#	for row in body:
#		if row[genus_col] == "indet." or row[species_col] == "indet." or row[species_col] == "sp.":
#			continue
#		name = row[genus_col]+' '+row[species_col]
#		name = re.sub(" var.*","",name)
#		if len(name.split(" ")) < 2:
#			continue
#		name = clean_name(name)
#		id = row[id_col]
#		order = row[order_col]
#		min_age = float(row[min_age_col])
#		max_age = float(row[max_age_col])	
#		if name in accepted_species:
#			outlog.writerow(["now",id,name,max_age,min_age,order,column1,column2])