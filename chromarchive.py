import cv2
import numpy as np
from optparse import OptionParser
import re
import os

def getImageFormat(image_path):
	return  "."+image_path.split('.')[-1]

def getFrameNumber(image_path):
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

if __name__ == '__main__':
	parser = OptionParser()
	parser.add_option("-i","--image",dest="image_path",help="Input Image Path")
	parser.add_option("-s","--silhouette",dest="silhouette_path",help="Input Silhouette Path")
	parser.add_option("-o","--output_directory",dest="output",help="Output Directory")
	
	(options,args) = parser.parse_args()

	single_frame_mode = True

	# Search for frame number pattern
	frame_id_size = options.image_path.count('#')

	sample_image_name = ''.join((['#']*frame_id_size)) + getImageFormat(options.image_path)
	print getImageFormat(options.image_path)
	print getFrameNumber(options.image_path)
	print getImageDirectory(options.image_path)


	# img = cv2.imread(options.image_path,1)
	# silhouette = cv2.imread(options.silhouette_path,0)