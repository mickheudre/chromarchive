import cv2
import numpy as np
from optparse import OptionParser
import re
import os

def exploreCamerasPath(cameras_path):
	#Check if the cameras path we guessed exists
	if os.path.isdir(cameras_path):
		print os.listdir(cameras_path)

	return cameras_path

def getImageFormat(image_path):
	return  "."+image_path.split('.')[-1]

def getFrameNumber(image_path):
	print re.findall(r'(\d+)'+getImageFormat(image_path),image_path)
	return re.findall(r'(\d+)'+getImageFormat(image_path),image_path)[0]

def getFirstLastFrame(images_path):
	firstFrame = 0
	lastFrame = 0

	if os.path.isdir(images_path):
		dlist = os.listdir(images_path)
		print dlist
	# 	idir = seqroot+"/Images/"+dlist[0]
	# 	if os.path.isdir(idir):
	# 		ilist = os.listdir(idir)
	# 		intlist = map(getFrameNumber,ilist)
	# 		firstFrame = min(intlist)
	# 		lastFrame = max(intlist)	
	# return (firstFrame,lastFrame)
def getImageDirectory(image_path):
	return options.image_path.split(getFrameNumber(image_path)+getImageFormat(image_path))[0]

def silhouetteMask(img,silhouette,dilate=2):
	if dilate > 0:
		kernel = np.ones((dilate,dilate),np.uint8)
		silhouette = cv2.erode(silhouette,kernel,iterations = 1)
	return cv2.bitwise_and(img,	silhouette)

class RunMode:
	def __init__(self):
		self.multiple_frames = False
		self.multiple_cameras = False

if __name__ == '__main__':
	parser = OptionParser()
	parser.add_option("-i","--image",dest="image_path",help="Input Image Path")
	parser.add_option("-s","--silhouette",dest="silhouette_path",help="Input Silhouette Path")
	parser.add_option("-o","--output_directory",dest="output",help="Output Directory")
	
	(options,args) = parser.parse_args()
	image_path = options.image_path

	run_mode = RunMode()
	# Search for frame number pattern
	path_analysis = re.findall('([\w]*)([#]+)',image_path)
	print path_analysis
	if len(path_analysis) == 0:
		run_mode.multiple_frames = False
		run_mode.multiple_cameras = False
		print "Single Frame mode"

	elif len(path_analysis) == 1:
		if image_path.find(path_analysis[0]+getImageFormat(image_path)) != -1:
			run_mode.multiple_frames = True
			run_mode.multiple_cameras = False
			print "Multiple Frame Mode"
		else:
			run_mode.multiple_frames = False
			run_mode.multiple_cameras = True
			print "Multiple Camera Mode"
	elif len(path_analysis) == 2:
		run_mode.multiple_frames = True
		run_mode.multiple_cameras = True
		print "Multiple Cameras & Frames mode"

		print exploreCamerasPath(image_path.split(path_analysis[0])[0])

	# sample_image_name = ''.join((['#']*frame_id_size)) + getImageFormat(options.image_path)
	# print getImageFormat(options.image_path)

	
	# print getFrameNumber(options.image_path)
	# print getImageDirectory(options.image_path)


	# img = cv2.imread(options.image_path,1)
	# silhouette = cv2.imread(options.silhouette_path,0)