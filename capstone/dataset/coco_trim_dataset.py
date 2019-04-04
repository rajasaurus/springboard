"""
coco_trim_dataset.py

	-this module is a component of the springboard AI/ML career track capstone project.  
	-COCO data set can be found here:
		 	http://cocodataset.org/#download
 	-function of this script is to trim the open source COCO ML datasets to appropriate size.
 	-instances_train2017.json contains segmented annotations
	 	len(data['annotations'])
	 	original size:	860001
		reduced to:		34440 (4%)
	-train2017 images
		image count:	118000
		reduced to:		27108 (23%)

	* After discussion with mentor the actual reduced size of annotations and/or images isn't 
	critical at this time.  We can revisit once we begin building the model and empirically 
	assess the performance.
		
"""

import json
import pprint as pp
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s %(levelname)s | %(message)s')

fh = logging.FileHandler('coco_trim_dataset_log.txt')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)


## COCO 2014 source
DATA_PATH_2014 = '/mnt/projects/springboard/source/COCO/annotations/'

## COC 2017 source
DATA_PATH_2017 = '/mnt/projects/springboard/source/COCO/2017/annotations_2/'
TRIM_PATH_2017 = '/mnt/projects/springboard/source/COCO/2017/annotations_trimmed/'

PRUNE_PERCENTAGE = 0.04


def create_output_file_name(input_file):
	"""
	example input: 	instances_train2017.json
	example output:	instances_train2017_trim_categorized.json
					instances_train2017_trim_aggregated.json
	"""
	file_name_split = input_file.split('.')	## ['instances_train2017', 'json']
	file_name_categorized = file_name_split[0] + "_trim_categorized." + file_name_split[1]
	file_name_aggregated = file_name_split[0] + "_trim_aggregated." + file_name_split[1]

	return ( file_name_categorized, file_name_aggregated )


def load_json_data_from_file(input_file):
	"""
	open input_file and load json content into data
	"""
	f = open(input_file, 'r')
	data = json.load(f)
	f.close()

	return data


def create_category_table(data):
	"""
	load category list of dicts into category.id index form
	input: 
		data['categories'][0:5]                                                                                                                                                                                                                      
			[{'supercategory': 'person', 'id': 1, 'name': 'person'},
			 {'supercategory': 'vehicle', 'id': 2, 'name': 'bicycle'},
			 {'supercategory': 'vehicle', 'id': 3, 'name': 'car'},
			 {'supercategory': 'vehicle', 'id': 4, 'name': 'motorcycle'},
			 {'supercategory': 'vehicle', 'id': 5, 'name': 'airplane'}]
	output:
		{1: ['person', 'person'],
		 2: ['bicycle', 'vehicle'],
		 3: ['car', 'vehicle'],
		 4: ['motorcycle', 'vehicle'],
		 5: ['airplane', 'vehicle'],
		 ...
	"""
	category_list = dict()

	for item in data['categories']:
		entry = list()
		id_num = int()
		name = str()
		supercat = str()

		for k,v in item.items():
			if k == 'id':
				id_num = v
			if k == 'name':
				name = v
			if k == 'supercategory':
				supercat = v

		category_list[id_num] = [name,supercat]

	pp.pprint (category_list)

	return category_list


def tabulate_annotation_categories(data):
	"""
	DEPRECATED:
	compute the count of annotation elements in each category
	tabulate count of data['annotations']['id']
	data['annotations'][0]['category_id'] --> 58
	"""
	tabulate_category_id = dict()

	for i in range(len(data['annotations'])):
		cat_id = data['annotations'][i]['category_id']
		if cat_id in tabulate_category_id.keys():
			tabulate_category_id[cat_id] += 1
		else:
			tabulate_category_id[cat_id] = 1

	pp.pprint (tabulate_category_id)

	return tabulate_category_id


def create_category_master(category_list):
	"""
	create category_master from data['annotations']['id'] with category id as key
		{1: [],
		 2: [],
		 3: [],
		 4: [],
		 5: [],
		 ...
	"""
	category_master = dict()

	for id_num in sorted(category_list.keys()):
		category_name = str(category_list[id_num][0])

		## NEW category indexed dict() 
		## {1:[], 2:[], 3:[], 4:[], ...
		category_master[id_num] = list()
		#pp.pprint (category_master)

	return category_master



def compute_category_stride(length, prune_percentage):
	target_count = length * prune_percentage
	stride = int(length + target_count // 2) // target_count 	## round to nearest int
	return stride


def populate_category_master(data, category_master):
	"""
	separate aggregated category list entries from data['annotations']
	into category_master dict()
	"""

	for i in range(len(data['annotations'])):
		cat_id = data['annotations'][i]['category_id']
		category_master[cat_id].append(data['annotations'][i]) 

	## peek into category master
	logging.debug('Category Master')
	for k, v in category_master.items():
		logging.debug('%s  %s', k, len(v))

	## category_master
	## key  len(list)
	## 1 	262465
	## 2 	7113
	## 3 	43867
	## 4 	8725
	## 5 	5135

	## ----------------------------------------------------------------------
	## stride through each category_master key list to reduce list size
	## by prune percentage. 
	## example: prune % = 0.04 (4%)
	## 			person = 262465 list items
	## 			262465 * 0.04 = 10499
	##			262465 / 10499 = 25
	## 			stride = 25
	## keep every 25th item, delete the remaining

	## first we need to determine the stride, which will be uniform over each category
	## just choose category = 1
	stride = compute_category_stride(len(category_master[1]), PRUNE_PERCENTAGE)

	categorized_master = dict()
	aggregated_master = list()

	## using the computed stride, filter down annotations uniformly by category
	## create one categorized and one aggregated version of the dataset
	## use a comprehension to filter the list
	for key, value in category_master.items():
		## category_master[key] = [ category_master[key][index] for index in range(len(value)) if index % stride == 0 ]
		categorized_master[key] = [ category_master[key][index] for index in range(len(value)) if index % stride == 0 ]
		aggregated_master	   += [ category_master[key][index] for index in range(len(value)) if index % stride == 0 ]

	## peek into category master
	logging.debug('TRIM Categorized Master')

	categorized_total_element_count = int()
	for k, v in categorized_master.items():
		categorized_total_element_count += len(v)
		logging.debug('%s  %s', k, len(v))

	logging.debug('TRIM Categorized Master Length %s', categorized_total_element_count)
	logging.debug('TRIM Aggregated Master Length %s', len(aggregated_master))

	return (categorized_master, aggregated_master)


def compute_annotation_image_references(aggregated_dataset):
	"""
	given a list of coco data annotations, determine how many images are referenced
	each annotation is a dict with one key value pair as such 
		'image_id': 480023,
	"""
	image_references = dict()

	for element in aggregated_dataset:
		image_id = element['image_id']

		if image_id in image_references.keys():
			image_references[image_id] += 1
		else:
			image_references[image_id] = 1

	logging.debug('Image References: %s', len(image_references.keys())) 



if __name__=='__main__':
	"""
	create a list of pertinent json files to be processed/trimmed.  
	iterate through each json file
		load the data
		extract the categories and create its data structure
		populate then trim the annotation data into the category master struct
		compute how many image files are referenced in trimmed dataset
		export both categorical and aggregated trimmed datasets into json files
	"""	
	#input_files = ['instances_train2017.json','instances_val2017.json','captions_train2017.json','captions_val2017.json','person_keypoints_train2017.json','person_keypoints_val2017.json']
	input_files = ['instances_train2017.json','instances_val2017.json']

	for input_file in input_files:

		logging.debug('MAIN Processing %s', input_file)
		
		data = load_json_data_from_file(DATA_PATH_2017 + input_file)
		category_list = create_category_table(data)
		#tabulate_category_id = tabulate_annotation_categories(data)
		category_master = create_category_master(category_list)

		(categorized_master, aggregated_master) = populate_category_master(data, category_master)

		compute_annotation_image_references(aggregated_master)

		(file_name_categorized, file_name_aggregated) = create_output_file_name(input_file)

		with open(TRIM_PATH_2017 + file_name_categorized, 'w') as outfile:  
		    json.dump(categorized_master, outfile)

		with open(TRIM_PATH_2017 + file_name_aggregated, 'w') as outfile:  
		    json.dump(aggregated_master, outfile)
















