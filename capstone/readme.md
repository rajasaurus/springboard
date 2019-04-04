## Springboard AI/Machine Learning Career Track Capstone Project

**Problem Statement**
As primary component for video surveillance is motion detection. Basic motion detection can result in significant false positives. Movement from pets, vehicle, insects, shadows, and camera image sensor switching from day to night commonly trigger the motion sensor. The primary use case for video surveillance is to identify human activity. Eliminating false positives would reduce unnecessary event storage, faster incident review, and confidence in setting notification alarms.
 
The solution is to incorporate to detect instances of semantic objects which can then be classified. The model could be extended to whitelist specific individuals. The user could then configure their surveillance system to motion record only suspect activity.

Since many video cameras provide for both day and night sensors, the model should produce similar results with both full-spectrum and IR images.

**Dataset**
I believe the Common Objects in Context (COCO) dataset to be an ideal source. This dataset has been cited as source by many papers in the object detection space, including Papers with Code.

[http://cocodataset.org](http://cocodataset.org/#home)

[https://paperswithcode.com/task/object-detection](https://paperswithcode.com/task/object-detection)

Additionally the dataset images and annotation are pre-organized into training, validation, and test sets. This will further facilitate the development of a performant model.

|COCO 2017 Dataset|Percentage(%)|
|:-------------------------:|---------------:|
|Train images [118K/18GB]|	72|
|Val images [5K/1GB]|3|
|Test images [41K/6GB]|25|


For the purposes of this project such a large dataset is not necessary and would consume significantly more computation resources. For this reason, I have agreed to uniformly reduce the dataset size by an order of magnitude. The new Train dataset size will be reduced from 118k to roughly 10k. The Val and Test sets will also be pruned similarly.  

**Computational Resources**
I have have researched how best to assess the computational resources necessary to build this model. For now it seems that the empirical approach may be best. Perhaps once the number of hidden layers, parameters, and associated weights and biases are better understood we can compute this concretely. I have received guidance to consider the following as a great starting point:

-   PaperSpace GPU Instance K80
-   $0.25/ hour
-   12GB GDDR5 DEDICATED
-   12GB RAM
-   2 vCPU
-   480 GB/s memory bandwidth
-   2,496 CUDA cores   

The time estimate to build the model with this resource is twelve(12) hours.
