# Data-Augmentation-for-Yolo----Flipping-and-Rotating-Datasets
A simple repository to flip and rotate datasets in random angle (can set customly).
The rotating script is mainly refers to [usmanr149](https://github.com/usmanr149/Yolo_bbox_manipulation/blob/master/rotate.py). A little bit of custom modification had been made.

***Support only jpg, jpeg, and png image extensions***. Please modify the code if you wish to add more extensions.

## Flipping
For flipping images, create a folder and put in all the images datasets (images and annotation txt files) with Darknet Yolo format, where all images are followed by its bounding boxes annotation txt file, respectively.

Input as below shown to run the programme.
```
python Flip_Image.py 'path to datasets folder' 'path to folder to keep output results' 
```

In order to make sure all the bounding boxes are correctly annotated, you can preview the output result, but setting on -v flag. Note that if -v flag is set on, no output images and new annotation txt files will be generated. It is just for **visualization**.
```
python Flip_Image.py 'path to datasets folder' 'path to folder to keep output results' -v
```

## Rotating
For rotating images, the same procedure as flipping images is taken. Create a folder to allocate all the images datasets (images and annotation txt files) with Darknet Yolo format, where all images are followed by its bounding boxes annotation txt file, respectively.

This is the command to run the programme. Adding -v flag for vizualization **only**.
```
python Rotate_Image.py 'path to datasets folder' 'path to folder to keep output results' -v
```

By default, the angle of rotation for each image is random, from -90°(clockwise) to 90°(anticlockwise). You can change the range of random rotation by input -min and -max flags, such as command shown below.
```
python Rotate_Image.py 'path to datasets folder' 'path to folder to keep output results' -min -45 -max 45
```
## Addition Info
After running the scripts, a txt file containing the list of path to output images will be generated. By default, 'data/obj_train_data/...jpg' is the default path. 

If you wish to change the path 'data/obj_train_data/...jpg' ---> data/new_train_data/...jpg, you can change the path by adding -p flag. 

Example is shown as below. This is applicable to both scripts
```
python Rotate_Image.py 'path to datasets folder' 'path to folder to keep output results' -min -45 -max 45 -p data/new_train_data
```

## Conclusion
Thank you for spending time here! I hope this repo does help you!
