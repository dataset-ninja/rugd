The authors introduce the **RUGD: Robot Unstructured Ground Driving Dataset** with video sequences captured from a small, unmanned mobile robot traversing in unstructured environments. This data differs from existing autonomous driving benchmark data in that it contains significantly more terrain types, irregular class boundaries, minimal structured markings, and presents challenging visual properties often experienced in off road navigation, e.g., blurred frames. Over 7, 000 frames of pixel-wise annotation are included with this dataset.

## Motivation


The development of extensive, labeled visual benchmark datasets has played a pivotal role in advancing the state-of-the-art in recognition, detection, and semantic segmentation. The success of these techniques has elevated visual perception to a primary information source for making navigation decisions on autonomous vehicles. Consequently, a multitude of benchmark datasets tailored specifically for autonomous navigation have emerged, featuring real-world scenarios where vehicles navigate through urban environments, interacting with pedestrians, bicycles, and other vehicles on roadways. These datasets serve as essential tools for evaluating progress toward the release of safe and reliable autonomous products.

Despite substantial strides in autonomous driving technologies, the current state-of-the-art is primarily tailored to well-paved and clearly outlined roadways. However, applications like Humanitarian Assistance and Disaster Relief (HADR), agricultural robotics, environmental surveying in hazardous areas, and humanitarian demining present environments that lack the structured and easily identifiable features commonly found in urban cities. Operating in these unstructured, off-road driving scenarios necessitates a visual perception system capable of semantically segmenting scenes with highly irregular class boundaries. This system must precisely localize and recognize terrain, vegetation, man-made structures, debris, and other hazards to assess traversability and ensure safety.

<img src="https://github.com/dataset-ninja/rugd/assets/120389559/b0321879-dccc-4f7c-b5c9-159ef190ec35" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;">Irregular boundaries are common in unstructured environments as seen in this example image and annotation. This challenging property exists throughout all sequences in the RUGD dataset and arises because of the natural growth and pourous-like texture of vegetation and occlusion.</span>

Because existing benchmark datasets for self-driving vehicles are collected from urban cities, they seldom contain elements that may be present in unstructured environments. As such, there is a need for an entirely new dataset relevant to these driving conditions, where structured cues cannot be readily relied on by the autonomous system.

## Dataset description

Robot Unstructured Ground Driving (RUGD) dataset, is composed of a set of video sequences collected from a small unmanned ground robot performing an exploration task in a variety of natural, unstructured environments and semi-urban areas. In addition to the raw frame sequences, RUGD contains dense pixel-wise annotations for every fifth frame in a sequence, providing a total of 7, 453 labeled images for learning and evaluation in this new driving scenario.

<img src="https://github.com/dataset-ninja/rugd/assets/120389559/eb814701-55d4-40e1-8744-e3966ef31aed" alt="image" width="1000">

<span style="font-size: smaller; font-style: italic;">Example ground truth annotations provided in the RUGD dataset. Frames from the video sequences are densely annotated with pixel-wise labels from 24 different visual classes.</span>

The unique characteristics, and thus, major contributions, of the RUGD dataset can be summarized as follows: 
* The majority of scenes contain no discernible geometric edges or vanishing points, and semantic boundaries are highly irregular. 
* Robot exploration traversal creates irregular routes that do not adhere to a single terrain type; eight distinct terrains are traversed. 
* Unique frame viewpoints are encountered due to sloped terrains and vegetation occlusion. 
* Off-road traversal of rough terrain results in challenging frame focus. 

These characteristics provide realistic off-road driving scenarios that present a variety of new challenges to the research community in addition to existing ones, e.g., illumination changes and harsh shadows. The authors provide an initial semantic segmentation benchmark using several current state-of-the-art semantic segmentation architectures, originally developed for indoor and urban scene segmentation.

## Dataset collection

The robot used to collect the RUGD dataset is based on a Clearpath ‘Husky’ platform. The robot chassis is equipped with a sensor payload consisting of a Velodyne HDL-32 LiDAR, a Garmin GPS receiver, a Microstrain GX3-25 IMU, and a Prosilica GT2750C camera. The camera is capable of 6.1 megapixels at 19.8 frames per second, but most sequences are collected at half resolution and approximately 15 frames per second. This reduction in resolution and frame rate provides a compromise between file size and quality. The images are collected through an 8mm lens with a wide depth of field for outdoor lighting conditions, with exposure and gain settings for minimized motion blur. The robot typically operated at its top speed of 1.0 m/s. This platform provides a unique camera viewpoint compared to existing data. The Husky is significantly smaller than vehicles commonly used in urban environments, with external dimensions of 990 x 670 x 390 mm. The camera sensor is mounted on the front of the platform just above the external height of the robot, resulting in an environment viewpoint from less than 25 centimeters off the ground.

<img src="https://github.com/dataset-ninja/rugd/assets/120389559/7acecaa4-fb07-442e-95cd-729008368dc6" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;">Robot used to collect the RUGD dataset.</span>

RUGD is a collection of robot exploration video sequences captured as a human teleoperates the robot in the environment. The exploration task is defined such that the human operator maneuvers the robot to mimic autonomous behavior aimed at trying to visually observe different regions of the environment. Given this definition, the sequences depict the robot traversing not only on what may be commonly defined as a road, but also through vegetation, over small obstacles,
and other terrain present in the area. The average duration of a video sequence is just over 3 minutes. Exploration traversals are performed in areas that represent four general environment categories: ***creek*** - areas near a body of water with some vegetation, ***park*** - woodsy areas with buildings and paved roads, ***trail*** - areas representing non-paved, gravel terrain in woods, ***village*** - areas with buildings and limited paved roads.

<img src="https://github.com/dataset-ninja/rugd/assets/120389559/b43c3160-959d-47d2-aa1b-27fe30e75fa3" alt="image" width="1000">

<span style="font-size: smaller; font-style: italic;">Example frames from robot exploration traversal videos from each of the four environment categories.</span>

The robot's onboard camera sensor records videos of each traversal at a frame rate of 15Hz, except for the village scenario, which is captured at a lower frequency of 1Hz, featuring a frame resolution of 1376x1110. These videos not only showcase various terrain types but also capture challenging conditions such as harsh shadows, blurred frames, changes in illumination, washed-out regions, orientation shifts resulting from sloped planes, and occluded perspectives due to traversal through areas with tall vegetation. The deliberate inclusion of these diverse scenes ensures that the dataset faithfully mirrors the realistic conditions encountered in these environments.

## Dataset split

Videos from the RUGD dataset are partitioned into train/val/test splits for our benchmark experimental evaluation. ∼64% of the total annotated frames used for training, ∼10% for validation, and the remaining ∼26% for testing. While the selection of videos for each split was decided to roughly produce specific sizes of each split, two videos were specifically placed in the test split to test realistic challenges faced in many motivating applications. First, the ***creek*** sequence is the only example with significant rock bed terrain. Reserving this as a testing video demonstrates how existing architectures are able to learn from sparse label instances. This is a highly realistic scenario in unstructured environment applications as it is difficult to collect large amounts of training data for all possible terrain a priori. Second, the ***trail*** 7 sequence represents significantly more off-road jitter than others, producing many frames that appear to be quite blurry. This property is also present in training sequences, but again we reserve the difficult video to determine how well the techniques are able to perform under these harsh conditions.

|      | C | P1 | P2 | P8 | T   | T3  | T4  | T5  | T6  | T7  | T9  | T10 | T11 | T12 | T13 | T14 | T15 | V    | Total | %    |
|------|---|----|----|----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|------|-------|------|
| train|   |    | x  |    | x   | x   | x   |     | x   |     | x   | x   | x   | x   |     | x   |  x  | x    | 4759  | 63.83|
| val  |   |    |    | x  |     |     |     | x   |     |     |     |     |     |     |     |     |     |      |  33   | 9.83 |
| test | x | x  |    |    |     |     |     |     |     | x   |     |     |     |     | x   |     |     |      | 1964  | 26.34|


<span style="font-size: smaller; font-style: italic;">Training, validation and testing splits. VIDEO SEQUENCES (C: CREEK, P: PARK, T: TRAIL, V: VILLAGE) THAT FALL INTO EACH SPLIT ARE DENOTED WITH AN X. THE TOTAL NUMBER OF FRAMES AND PERCENTAGE OF EACH SPLIT WITHIN THE WHOLE DATASET ARE SEEN IN THE LAST TWO COLUMNS.</span>