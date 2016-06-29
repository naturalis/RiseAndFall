import csv

fossil_file = '/Users/tobias/Desktop/pbdb_data(1).csv'
trait_file = '/Users/tobias/Desktop/traits_smith_etal.csv'

output = open("/Users/tobias/Desktop/all_mammals_bm_python_input.csv", "wb")
outlog=csv.writer(output, delimiter='\t')
outlog.writerow(["Species","Status","MinT","MaxT","Trait"])

species_list = []
min_age_list = []
max_age_list = []
with open(fossil_file, 'r') as f:
	reader = csv.reader(f, delimiter=',')
	reader = list(reader)
	info = reader[0:18]
	header = reader[19]
	body = reader[20:]
	for row in body:
		row[5] = row[5].replace(" n. sp.", "")
		row[5] = row[5].replace(" n. gen.", "")
		row[5] = row[5].replace(" aff.", "")
		row[5] = row[5].replace(" cf.", "")
		row[5] = row[5].replace(" ?", "")
		row[5] = row[5].replace(" \"", "")
		# skip any unclean taxa-names that contain more than 2 words
		if len(row[5].split()) > 2:
			continue
		name = row[5]
		species_list.append(name)
		max_age = row[14]
		max_age_list.append(max_age)
		min_age = row[15]
		min_age_list.append(min_age)

f = open(trait_file, "rw")
content = [x.strip('\r\n') for x in f.readlines()]
lines = content[0].split('\r')
header = lines[0].split(';')
body = lines[1:]
for line in body:
	elements = line.split(';')
	ref_species = elements[4] + ' ' + elements[5]
	if ref_species in species_list:
		# get the position in the list of the matching string
		index = species_list.index(ref_species)
		outlog.writerow([species_list[index], elements[1], min_age_list[index], max_age_list[index], elements[7]])
quit()
