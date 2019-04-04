## Capstone Project: Data Collection

This python module is the dataset reduction component capstone project.

`./dataset/coco_trim_dataset.py`

The COCO dataset source can be found here:
http://cocodataset.org/#download

The function of this script is to trim the open source COCO ML datasets to an appropriate size for building a functional model with resource efficiency.  

The pertinent files within the COCO dataset are:

|Filename|Size(bytes)|
|:-------------------------|---------------:|
|captions_train2017.json|91865115|
|captions_val2017.json|3872473|
|instances_train2017.json|3872473|
|instances_val2017.json|19987840|
|person_keypoints_train2017.json|238884731|
|person_keypoints_val2017.json|10020657|

At this time we are primarily interested in reducing the *instances* files which contain the *category* and *annotation* metadata.  The structures of these files are as follows:
*Note `data = json.load(file)`

**instances_train2017.json**
|Interrogation|Response|
|:-------------------------|:---------------|
|`type(data)`|`<class 'dict'>`|
|`data.keys()`|`dict_keys(['info', 'licenses', 'images', 'annotations', 'categories'])`|
|`type(data['annotations'])`|`<class 'list'>`|
|`type(data['categories'])`|`<class 'list'>`|
|`len(data['categories'])`|`90`|
|`data['categories'][0:9]`|`[{'supercategory': 'person', 'id': 1, 'name': 'person'},`<br>`{'supercategory': 'vehicle', 'id': 2, 'name': 'bicycle'},`<br>`{'supercategory': 'vehicle', 'id': 3, 'name': 'car'},`<br>`{'supercategory': 'vehicle', 'id': 4, 'name': 'motorcycle'},`<br>`{'supercategory': 'vehicle', 'id': 5, 'name': 'airplane'},`<br>`{'supercategory': 'vehicle', 'id': 6, 'name': 'bus'},`<br>`{'supercategory': 'vehicle', 'id': 7, 'name': 'train'},`<br>`{'supercategory': 'vehicle', 'id': 8, 'name': 'truck'},`<br>`{'supercategory': 'vehicle', 'id': 9, 'name': 'boat'}]`|
|`len(data['annotations'])`|`860001`|
|`data['annotations'][0]`|                                                                                                                                                      `{'segmentation': [[312.29, 562.89, 402.25, 511.49, 400.96, 425.38, 398.39, 372.69, 388.11, 332.85,	318.71, 325.14, 295.58, 305.86, 269.88, 314.86, 258.31, 337.99, 217.19, 321.29, 182.49,	343.13, 141.37, 348.27, 132.37, 358.55, 159.36,377.83, 116.95, 421.53, 167.07, 499.92, 232.61, 560.32, 300.72, 571.89]],`<br>`'area': 54652.9556,`<br>`'iscrowd': 0,`<br>`'image_id': 480023,`<br>`'bbox': [116.95, 305.86, 285.3, 266.03],`<br>`'category_id': 58,`<br>`'id': 86}`

The *instances_val2017.json* has a nearly identical structure to *instances_train2017.json*. 
To trim both of these metadata sets we do the following:
1. load the json data
2. extract the categories and load them into a dict() called category_master
3. populate each categories annotation data into respective category master key as a list().
4. now that we have a dict() with category id as each key, we trim all categories *uniformly*  
5. compute how many image files are referenced in trimmed dataset
6. export both categorical and aggregated trimmed datasets into json files
7. when we better understand the proper magnitude and format of the metadata we can easily regenerate these files

### Current Dataset Reduction Statistics
----------
|Train Data|Original Count|Reduced Count|
|:-------------------------|:---------------|:-----------------|
|Annotations| 860001|34440 (4%)|
|Images|118000|27108 (23%)|

