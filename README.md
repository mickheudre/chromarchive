**Copyright 2016 INRIA**

*Author : Mickaël Heudre mickael.heudre@inria.fr/mickheudre@gmail.com*

***

ChromArchive is a small software intended to archive chroma key image sequences intented to be used for 3D reconstruction.

ChromArchive works with images/silhouettes pairs. It will save the multiplication of both, in order to save the useless space.

The core is feature of this software is that it automaticaly explore the cameras and images directory following some hints given by the user.

To lauch ChromArchive, simply run:
```
python chomarchive.py -i image_file -s silhouette_file -o output_directory
```
It deals with 3 different cases :
- a single image/silhouette pair is provided
```
	python chromarchive.py -i frame.png -s silhouette.png -o output_dir/
```

- two folders containing a sequence of image and a sequence silhouette is provided
```
	python chromarchive.py -i frame####.png -s silhouette####.png - output_dir/
```
The program will scan the directories to find images and silhouettes matching the given pattern, where # replaces a number.
To load frame01.png, frame02.png, ..., frame15.png, simply type frame##.png
To load frame00001.png, frame00002.png, ..., frame00015.png, simply type frame#####.png

- a list of folders containing images and silhouettes for several cameras is provided
```
	python chromarchive.py -i cam_##/frame####.png -s cam_##/silhouette####.png - output_dir/
```
Note that the camera name has to be set before image name.